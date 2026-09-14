"""Single-GPU offline vLLM extraction from persisted semantic units. Gold is not an input."""
import argparse
import copy
import datetime
import hashlib
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import socket
import subprocess
import sys
import time

os.environ['VLLM_ENABLE_V1_MULTIPROCESSING']='0'

import jsonschema
import pyarrow as pa
import pyarrow.parquet as pq


def canonical(x):
    return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))


def sha(x):
    return hashlib.sha256(x.encode() if isinstance(x,str) else x).hexdigest()


def norm(x):
    return ' '.join(x.split())


ACTOR_ROLES={'REGULATOR':'FCHLPM','VENDOR':'RMS','REVIEW_TEAM':'Professional Team','UNKNOWN':'Other/Unknown'}
_V2=None


def evidence_v2():
    global _V2
    if _V2 is None:
        spec=importlib.util.spec_from_file_location('evidence_v2',Path(__file__).with_name('evidence_v2.py'))
        _V2=importlib.util.module_from_spec(spec);spec.loader.exec_module(_V2)
    return _V2


def source_schema(unit,schema):
    """Constrain reference choices using this input unit only, never annotations."""
    if 'assertion_ids' in schema['properties']['records']['items']['properties']:
        return evidence_v2().request_schema(unit,schema)
    result=copy.deepcopy(schema)
    props=result['properties']['records']['items']['properties']
    refs=[i['ref'] for i in unit['items']]
    props['citations']['items']={'type':'string','enum':refs}
    for key in ['action_spans','target_spans']:
        if key in props:
            eligible=refs if key=='action_spans' else [i['ref'] for i in unit['items'] if not i['is_context']]
            if not eligible:
                raise ValueError('No body source exists for target selection')
            props[key]['items']['properties']['ref']={'type':'string','enum':eligible}
    return result


def complete_assertion_refs(unit,refs):
    """Retain adjacent unfinished source sentences; do not join new provisions."""
    items=unit['items'];edges=[]
    new_item=re.compile(r'^(?:[•▪●\-–]\s|\d+[.)]\s|[A-Z]\.\s|[A-Z]+-\d+(?:\.\w+)*\s)')
    for left,right in zip(items,items[1:]):
        if left['is_context'] or right['is_context'] or left['kind']!='text' or right['kind']!='text':
            continue
        text=left['text'].rstrip().rstrip('"\'”’)]}')
        if text and text[-1] not in '.!?;:' and not new_item.match(right['text'].lstrip()):
            edges.append((left['ref'],right['ref']))
    refs=set(refs)
    while True:
        before=len(refs)
        for a,b in edges:
            if a in refs or b in refs:
                refs.update([a,b])
        if len(refs)==before:
            return refs


def words(text):
    return list(re.finditer(r'\S+',text))


def decode_spans(unit,rec):
    if len(rec['citations'])!=len(set(rec['citations'])):
        raise ValueError('Repeated source ref')
    sources={i['ref']:i for i in unit['items']};refs=set(rec['citations']);fields={}
    for field,limit in [('action',8),('target',24)]:
        pieces=[];count=0
        for span in rec[field+'_spans']:
            if span['ref'] not in sources:
                raise ValueError('Unknown span source: '+span['ref'])
            if field=='target' and sources[span['ref']]['is_context']:
                raise ValueError('Target span must select body evidence, not an ancestor heading')
            text=sources[span['ref']]['text'];tokens=words(text)
            start,end=span['start'],span['end']
            if not 0<=start<end<=len(tokens):
                raise ValueError(f'Invalid {field} span range in {span["ref"]}: [{start},{end}) with {len(tokens)} tokens')
            count+=end-start
            pieces.append(text[tokens[start].start():tokens[end-1].end()]);refs.add(span['ref'])
        if count>limit or (field=='target' and not pieces):
            raise ValueError(f'{field} span must contain '+('1-' if field=='target' else '0-')+str(limit)+' source tokens')
        fields[field]=' '.join(pieces)
    unknown=refs-sources.keys()
    if unknown:
        raise ValueError('Unknown citation refs: '+repr(sorted(unknown)))
    result={k:rec[k] for k in ['evidence_type','post_review_response','review_induced_change']}
    refs=complete_assertion_refs(unit,refs)
    result.update(fields,actor=ACTOR_ROLES[rec['actor_role']],
                  citations=[i['ref'] for i in unit['items'] if i['ref'] in refs])
    return result


def decode_quotes(unit,rec):
    """Locate literal model-selected phrases; never infer or repair their meaning."""
    if len(rec['citations'])!=len(set(rec['citations'])):
        raise ValueError('Repeated source ref')
    sources={i['ref']:i for i in unit['items']};refs=set(rec['citations']);fields={}
    selection=dict(actor_role=rec['actor_role'],coordinate_system='CHARACTER',
                   declared_citation_refs=list(rec['citations']))
    for field,limit in [('action',8),('target',24)]:
        spans=rec[field+'_spans'];resolved=[];pieces=[]
        selection[field+'_quotes']=copy.deepcopy(spans)
        for selected in spans:
            ref=selected['ref'];quote=selected['quote']
            if ref not in sources:
                raise ValueError('Unknown quote source: '+ref)
            item=sources[ref]
            if field=='target' and item['is_context']:
                raise ValueError('Target quote must select body evidence')
            tokens=quote.split()
            if not 1<=len(tokens)<=limit:
                raise ValueError(f'{field} quote requires 1-{limit} words')
            pattern=r'(?<!\w)'+r'\s+'.join(re.escape(t) for t in tokens)+r'(?!\w)'
            matches=list(re.finditer(pattern,item['text']))
            if len(matches)!=1:
                raise ValueError(f'{field} quote in {ref} has {len(matches)} exact occurrences; select one unique contiguous source phrase')
            match=matches[0];pieces.append(match.group())
            resolved.append(dict(ref=ref,start=match.start(),end=match.end()));refs.add(ref)
        fields[field]=' '.join(pieces);selection[field+'_spans']=resolved
    if refs-sources.keys():
        raise ValueError('Unknown citation refs: '+repr(sorted(refs-sources.keys())))
    refs=complete_assertion_refs(unit,refs)
    result={k:rec[k] for k in ['evidence_type','post_review_response','review_induced_change']}
    result.update(fields,actor=ACTOR_ROLES[rec['actor_role']],
                  citations=[i['ref'] for i in unit['items'] if i['ref'] in refs])
    return result,selection


def write(path,obj):
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')


def deny_annotation_reads():
    def guard(event,args):
        if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
            path=os.path.abspath(os.fsdecode(args[0]))
            if '/data/gold/' in path or '/data/evaluation/' in path:
                raise PermissionError('Extractor annotation/evaluation access denied: '+path)
    sys.addaudithook(guard)


def materialize(unit,response,schema,blocks=None):
    jsonschema.validate(response,schema)
    if 'assertion_ids' in schema['properties']['records']['items']['properties']:
        if blocks is None: raise ValueError('M2 blocks required for assertion reconstruction')
        return evidence_v2().materialize(unit,response,blocks)
    sources={i['ref']:i for i in unit['items']};records=[];errors=[]
    for i,rec in enumerate(response['records']):
        selection=None
        if 'action_spans' in rec:
            try:
                if 'quote' in schema['properties']['records']['items']['properties']['target_spans']['items']['properties']:
                    rec,selection=decode_quotes(unit,rec)
                else:
                    selection={k:rec[k] for k in ['action_spans','target_spans','actor_role']}
                    selection['declared_citation_refs']=rec['citations']
                    rec=decode_spans(unit,rec)
            except ValueError as exc:
                errors.append(f'record {i}: {exc}');continue
        refs=rec['citations'];citations=[]
        if len(refs)!=len(set(refs)):
            errors.append(f'record {i}: repeated source ref')
        unknown=[ref for ref in refs if ref not in sources]
        if unknown:
            errors.append(f'record {i}: unknown refs {unknown}');continue
        items=[sources[ref] for ref in refs]
        if all(x['is_context'] for x in items):
            errors.append(f'record {i}: cites only contextual headings')
        text=norm(' '.join(x['text'] for x in items))
        for k in ['action','target']:
            if (k=='target' and not rec[k].strip()) or norm(rec[k]) not in text:
                errors.append(f'record {i}: {k} must be copied exactly from its cited source')
        for ref,item in zip(refs,items):
            citations.append(dict(ref=ref,quote=item['text'],source_kind=item['kind'],
                source_block_ids=item['source_block_ids'],pages=item['pages'],table_cell_ids=item['table_cell_ids']))
        payload={k:rec[k] for k in ['evidence_type','actor','action','target','post_review_response','review_induced_change']}
        payload.update(unit_id=unit['unit_id'],document_id=unit['document_id'],
            source_block_ids=sorted({b for x in items for b in x['source_block_ids']}),
            pages=sorted({p for x in items for p in x['pages']}),citations=citations,
            table_cell_ids=sorted({c for x in items for c in x['table_cell_ids']}),
            source_parse_warnings=unit['parse_warnings'])
        if selection is not None:
            payload['span_selection']=selection
        payload['record_id']=sha(canonical(payload))[:24];records.append(payload)
    return records,errors


def user_payload(unit,ontology,span_selection=False,quote_selection=False,assertion_selection=False):
    if assertion_selection: return evidence_v2().request_payload(unit,ontology)
    meta={k:unit[k] for k in ['document_type','author','section_path','standard_id','source_context_label','unit_kind','pages']}
    if quote_selection:
        return canonical(dict(ontology=ontology['types'],actor_registry=ACTOR_ROLES,document=meta,
            sources=[{k:i[k] for k in ['ref','kind','is_context','text']} for i in unit['items']]))
    if span_selection:
        return canonical(dict(ontology=ontology['types'],actor_registry=ACTOR_ROLES,document=meta,
            sources=[dict(ref=i['ref'],kind=i['kind'],is_context=i['is_context'],
                          word_count=len(words(i['text'])),
                          indexed_words=' '.join(f'{j}:{m.group()}' for j,m in enumerate(words(i['text']))))
                     for i in unit['items']]))
    return canonical(dict(ontology=ontology['types'],document=meta,
        sources=[{k:i[k] for k in ['ref','kind','is_context','text']} for i in unit['items']]))


def input_token_count(tokenizer,messages):
    # Transformers versions differ in apply_chat_template's tokenized return type.
    # Count the explicit token IDs, never the keys of a BatchEncoding mapping.
    rendered=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
    if not isinstance(rendered,str):
        raise TypeError('Expected one rendered chat string')
    return len(tokenizer.encode(rendered,add_special_tokens=False))


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    for name in ['units','config','prompt','schema','ontology','output']:
        cli.add_argument('--'+name,type=Path,required=True)
    cli.add_argument('--limit',type=int)
    cli.add_argument('--blocks',type=Path,help='Immutable M2 block input required by evidence record v2')
    cli.add_argument('--scope',choices=['FULL','CORE_REGRESSION'],default='FULL')
    args=cli.parse_args();cfg=json.loads(args.config.read_text());schema=json.loads(args.schema.read_text())
    span_selection='action_spans' in schema['properties']['records']['items']['properties']
    assertion_selection='assertion_ids' in schema['properties']['records']['items']['properties']
    quote_selection=span_selection and 'quote' in schema['properties']['records']['items']['properties']['target_spans']['items']['properties']
    ontology=json.loads(args.ontology.read_text());prompt=args.prompt.read_text();out=args.output
    if 'login' in socket.gethostname():
        raise RuntimeError('Inference is prohibited on a login node')
    deny_annotation_reads()
    units=pq.read_table(args.units).to_pylist()
    if args.limit is not None:
        units=units[:args.limit]
    identities={k:sha(getattr(args,k).read_bytes()) for k in ['units','config','prompt','schema','ontology']}
    identities['extractor_code']=sha(Path(__file__).read_bytes())
    blocks=None
    if assertion_selection:
        if args.blocks is None: raise ValueError('Assertion extraction requires --blocks')
        blocks={b['block_id']:b for b in pq.read_table(args.blocks).to_pylist()}
        identities['blocks']=sha(args.blocks.read_bytes())
        identities['evidence_v2_code']=sha(Path(__file__).with_name('evidence_v2.py').read_bytes())
        roles={u['document_id']:u['document_type'] for u in units}
        units=[evidence_v2().prepare_unit(u,blocks,roles) for u in units]
        identities['candidate_builder']=sha(Path(evidence_v2().candidates.__file__).read_bytes())
    fingerprint=sha(canonical(identities))
    versions={p:importlib.metadata.version(p) for p in ['vllm','torch','transformers','pyarrow','jsonschema']}
    if versions['vllm']!=cfg['vllm_version']:
        raise ValueError('Installed vLLM version differs from the pinned configuration')
    gpu=subprocess.check_output(['nvidia-smi','--query-gpu=name,uuid,memory.total,driver_version','--format=csv,noheader'],text=True).strip()
    run=dict(status='RUNNING',input_sha256=identities,fingerprint=fingerprint,config=cfg,versions=versions,
        field_construction='ASSERTION_CANDIDATES_AND_M2_CELLS' if assertion_selection else ('EXACT_SOURCE_QUOTES' if quote_selection else ('SOURCE_TOKEN_SPANS' if span_selection else 'VERBATIM_MODEL_TEXT')),
        hostname=socket.gethostname(),gpu=gpu,python=platform.python_version(),
        semantic_gold_access=False,annotation_read_guard='ENFORCED_DENY_GOLD_AND_EVALUATION_PATHS',
        unit_count=len(units),unit_ids=[u['unit_id'] for u in units],
        full_unit_count=pq.read_metadata(args.units).num_rows,scope=args.scope if args.limit is None else 'SMOKE',
        started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    out.mkdir(parents=True,exist_ok=True)
    prior=out/'run_manifest.json'
    if prior.exists():
        old=json.loads(prior.read_text())
        for k in ['fingerprint','unit_ids','versions','gpu','scope']:
            if old.get(k)!=run[k]:
                raise ValueError('Refusing to resume under changed '+k)
    if assertion_selection:
        catalog_text=''.join(canonical(u['candidate_catalog'])+'\n' for u in units)
        catalog_path=out/'assertion_candidates.jsonl'
        if catalog_path.exists() and catalog_path.read_text()!=catalog_text:
            raise ValueError('Refusing to resume with changed candidate catalog')
        if not catalog_path.exists(): catalog_path.write_text(catalog_text)
        run['candidate_catalog_sha256']=sha(catalog_text)
        run['candidates_persisted_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        run['candidate_count']=sum(len(u['candidate_catalog']['candidates']) for u in units)
    write(prior,run)
    done={} 
    journal=out/'unit_results.jsonl'
    if journal.exists():
        for line in journal.read_text().splitlines():
            rec=json.loads(line)
            if rec['unit_id'] in done:
                raise ValueError('Duplicate checkpoint unit')
            done[rec['unit_id']]=rec
    if assertion_selection:
        cell_ids=set()
        for unit in units:
            if unit['unit_kind']!='table': continue
            if unit['unit_id'] in done:
                cell_ids.update(c for r in done[unit['unit_id']]['records'] for c in r['table_cell_ids'])
                continue
            try:
                promoted=evidence_v2().promote_table(unit,blocks);errors=[]
                found={c for r in promoted for c in r['table_cell_ids']}
                if cell_ids&found: errors.append('Duplicate M2 cell across table units')
                cell_ids.update(found)
            except (KeyError,ValueError) as exc:
                promoted=[];errors=[str(exc)]
            item=dict(unit_id=unit['unit_id'],status='FAILED' if errors else 'PROMOTED',errors=errors,
                      records=promoted,attempts=[],batch_unit_ids=[])
            with journal.open('a') as f:
                f.write(canonical(item)+'\n');f.flush();os.fsync(f.fileno())
            done[unit['unit_id']]=item
        for unit in units:
            if unit['unit_kind']=='table' or not unit['heading_only'] or unit['unit_id'] in done: continue
            item=dict(unit_id=unit['unit_id'],status='ABSTAINED',errors=[],records=[],attempts=[],batch_unit_ids=[],reason='M2_HEADING_ONLY')
            with journal.open('a') as f:
                f.write(canonical(item)+'\n');f.flush();os.fsync(f.fileno())
            done[unit['unit_id']]=item
    inference_units=[u for u in units if not assertion_selection or (u['unit_kind']!='table' and not u['heading_only'])]
    from vllm import LLM,SamplingParams
    from vllm.sampling_params import StructuredOutputsParams
    run['inference_started_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write(prior,run)
    llm=LLM(model=cfg['model_path'],tokenizer=cfg['model_path'],dtype=cfg['dtype'],
        max_model_len=cfg['max_model_len'],gpu_memory_utilization=cfg['gpu_memory_utilization'],
        tensor_parallel_size=1,seed=cfg['seed'],enforce_eager=True,max_num_seqs=cfg['max_num_seqs'],
        enable_prefix_caching=False,disable_log_stats=True)
    tokenizer=llm.get_tokenizer()
    write(out/'tokenizer_identity.json',dict(chat_template_sha256=sha(tokenizer.chat_template or ''),
        tokenizer_class=type(tokenizer).__name__,model_revision=cfg['model_revision']))
    batch_size=cfg.get('batch_size',4)
    for base in range(0,len(inference_units),batch_size):
        batch=inference_units[base:base+batch_size]
        if all(u['unit_id'] in done for u in batch):
            continue
        requests=[];token_counts=[]
        for unit in batch:
            messages=[dict(role='system',content=prompt),dict(role='user',content=user_payload(unit,ontology,span_selection,quote_selection,assertion_selection))]
            count=input_token_count(tokenizer,messages)
            if count+cfg['max_output_tokens']>cfg['max_model_len']:
                raise ValueError('Input exceeds context budget for '+unit['unit_id']+'; source was not truncated')
            requests.append(messages);token_counts.append(count)
        states=[dict(attempts=[],records=[],errors=[]) for _ in batch]
        schemas=[source_schema(u,schema) for u in batch]
        pending=list(range(len(batch)))
        for attempt in range(cfg['max_validation_attempts']):
            start=time.monotonic()
            params=[SamplingParams(temperature=0,seed=cfg['seed'],max_tokens=cfg['max_output_tokens'],
                    structured_outputs=StructuredOutputsParams(json=schemas[k])) for k in pending]
            outputs=llm.chat(requests,params,use_tqdm=False)
            elapsed=time.monotonic()-start
            if len(outputs)!=len(pending):
                raise ValueError('Inference returned a different number of responses than requests')
            next_pending=[];next_requests=[];next_counts=[]
            for j,generated,current_input_count in zip(pending,outputs,token_counts):
                unit=batch[j];state=states[j];output=generated.outputs[0]
                raw=output.text;parsed=None
                try:
                    parsed=json.loads(raw);records,errors=materialize(unit,parsed,schemas[j],blocks)
                except (ValueError,jsonschema.ValidationError) as exc:
                    errors=[str(exc)[:500]];records=[]
                count=len(parsed['records']) if isinstance(parsed,dict) and isinstance(parsed.get('records'),list) else None
                if attempt==0:
                    state['attempted_record_count']=count
                elif state.get('attempted_record_count') and count==0:
                    errors.append('Source-format repair cannot erase previously attempted evidence claims')
                if output.finish_reason=='length':
                    errors.append('Model output hit token limit')
                state.update(records=records,errors=errors)
                state['attempts'].append(dict(raw_output=raw,finish_reason=output.finish_reason,
                    response_schema_sha256=sha(canonical(schemas[j])),
                    output_tokens=len(output.token_ids),input_tokens=current_input_count,batch_elapsed_seconds=elapsed,
                    generation_batch_unit_ids=[batch[k]['unit_id'] for k in pending],validation_errors=list(errors)))
                if not errors or attempt+1==cfg['max_validation_attempts']:
                    continue
                messages=[dict(role='system',content=prompt),dict(role='user',content=user_payload(unit,ontology,span_selection,quote_selection,assertion_selection)+
                    '\nPrevious answer requiring source-format repair: '+raw+
                    '\nThe preceding format/source validation failed: '+canonical(errors)+
                    ('\nReturn a complete corrected answer. Repair only the assertion IDs named in the errors. Select adjacent candidates in source order and preserve valid records and semantic labels. Do not generate quotations, action, target or known actors.' if assertion_selection else
                     '\nReturn a complete corrected answer. Repair only the cited source refs, selected span ranges or exact action/target substrings named in the errors. Preserve valid records and semantic labels. Do not change a semantic claim merely to satisfy format validation.'))]
                current_input_count=input_token_count(tokenizer,messages)
                if current_input_count+cfg['max_output_tokens']>cfg['max_model_len']:
                    errors.append('Repair input exceeds context budget; source was not truncated')
                    continue
                next_pending.append(j);next_requests.append(messages);next_counts.append(current_input_count)
            if not next_pending:
                break
            pending=next_pending;requests=next_requests;token_counts=next_counts
        for j,(unit,state) in enumerate(zip(batch,states)):
            records=state['records'];errors=state['errors']
            item=dict(unit_id=unit['unit_id'],status='FAILED' if errors else ('OK' if records else 'ABSTAINED'),errors=errors,records=records,attempts=state['attempts'],
                      batch_unit_ids=[u['unit_id'] for u in batch])
            if unit['unit_id'] in done:
                if canonical(done[unit['unit_id']]['records'])!=canonical(records):
                    raise ValueError('Resumed batch changed previously persisted evidence')
                continue
            with journal.open('a') as f:
                f.write(canonical(item)+'\n');f.flush();os.fsync(f.fileno())
            done[unit['unit_id']]=item
            print(f"{base+j+1}/{len(units)} {item['status']} {len(records)} records",flush=True)
    ordered=[done[u['unit_id']] for u in units]
    evidence=[r for item in ordered for r in item['records']]
    pq.write_table(pa.Table.from_pylist(evidence),out/'evidence_records.parquet',compression='zstd')
    failures=[dict(unit_id=x['unit_id'],errors=x['errors']) for x in ordered if x['status']=='FAILED']
    write(out/'failures.json',failures)
    run.update(status='FAILED' if failures else 'COMPLETE',processed_units=len(ordered),failed_units=len(failures),
        promoted_units=sum(x['status']=='PROMOTED' for x in ordered),llm_eligible_units=len(inference_units),
        deterministic_abstained_units=sum(x.get('reason')=='M2_HEADING_ONLY' for x in ordered),
        records=len(evidence),abstained_units=sum(x['status']=='ABSTAINED' for x in ordered),
        evidence_sha256=sha((out/'evidence_records.parquet').read_bytes()),
        canonical_evidence_sha256=sha(canonical(evidence)),
        completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    write(prior,run)
    print(canonical(run),flush=True)
    return 1 if failures else 0


if __name__=='__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        if '--output' in sys.argv:
            out=Path(sys.argv[sys.argv.index('--output')+1]);out.mkdir(parents=True,exist_ok=True)
            failure=dict(status='FAILED',error_type=type(exc).__name__,message=str(exc))
            write(out/'fatal_error.json',failure)
            if (out/'run_manifest.json').exists():
                run=json.loads((out/'run_manifest.json').read_text());run.update(status='FAILED',fatal_error=failure)
                write(out/'run_manifest.json',run)
        raise
