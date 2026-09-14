"""Gold-blind assertion reconstruction and deterministic M2 cell promotion."""
import copy
from decimal import Decimal
import hashlib
import json
import re

VERSION='evidence-record-2.2'

# Load the sibling from the same frozen producer snapshot.
import importlib.util
from pathlib import Path
_spec=importlib.util.spec_from_file_location('assertion_candidates',Path(__file__).with_name('assertion_candidates.py'))
candidates=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(candidates)
ACTORS={'REGULATOR':'FCHLPM','VENDOR':'RMS','REVIEW_TEAM':'Professional Team','UNKNOWN':'Other/Unknown'}


def canonical(x): return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def norm(x): return ' '.join(x.split())


def tokens(text): return list(re.finditer(r'\S+',text))


def prepare_unit(unit,blocks,document_roles=None):
    """Attach source-only metadata without changing the persisted M2/unit input."""
    unit=copy.deepcopy(unit)
    roles=document_roles or {unit['document_id']:unit['document_type']}
    standard_docs={doc for doc,role in roles.items() if role=='standard'}
    standard_text=' '.join(norm(b['text']) for b in sorted(blocks.values(),key=lambda b:(b['document_id'],b['reading_order']))
                           if b['document_id'] in standard_docs and b['is_searchable'])
    carry=False;vendor_list=False
    for index,item in enumerate(unit['items']):
        bs=[blocks[bid] for bid in item['source_block_ids']]
        item['block_type']=bs[0]['block_type'] if len(bs)==1 else 'mixed'
        text=item['text'];heading=item['block_type']=='heading'
        provision=heading and not item['is_context'] and bool(re.match(r'^(?:[A-Z]\.\s|[A-Z]+-\d+\.\d+(?:\.[A-Z])?\s)',text))
        following=unit['items'][index+1] if index+1<len(unit['items']) else None
        unfinished=bool(text.strip()) and text.rstrip()[-1] not in '.!?;:'
        continuation=provision and unfinished and following is not None and not following['is_context'] and blocks[following['source_block_ids'][0]]['block_type']!='heading'
        item['assertion_eligible']=not item['is_context'] and item['kind']=='text' and (not heading or continuation)
        actor=None;basis='AMBIGUOUS_SOURCE_ROLE';doc=unit['document_type'];label=unit['source_context_label']
        if doc=='standard': actor='FCHLPM';basis='STANDARD_DOCUMENT'
        elif doc=='professional_team_report':
            copied=label=='Audit' or (label is None and any(p.startswith('subsection: ') for p in unit['section_path']))
            verified=bool(re.match(r'^Verified\s*:',text))
            actor='FCHLPM' if copied and not verified else 'Professional Team'
            basis='COPIED_REGULATORY_SECTION' if copied and not verified else 'REVIEW_REPORT_CONTEXT'
            if vendor_list and item['block_type']=='list': actor=ACTORS['VENDOR'];basis='EXPLICIT_VENDOR_UPDATE_LIST'
        elif doc=='vendor_submission':
            stripped=re.sub(r'^(?:[A-Z]+-\d+(?:\.\w+)*|[A-Z]|\d+)[.)]?\s+','',norm(text))
            copied=len(stripped.split())>=8 and stripped in standard_text
            actor='FCHLPM' if provision or carry or copied else 'RMS'
            basis='NUMBERED_REGULATORY_PROVISION' if provision or carry else ('EXACT_STANDARD_TEXT' if copied else 'VENDOR_DOCUMENT')
        item['source_actor']=actor;item['actor_basis']=basis
        carry=continuation or (carry and unfinished and not heading)
        introduced=doc=='professional_team_report' and bool(re.search(r'\b'+re.escape(ACTORS['VENDOR'])+r'\b.{0,120}\b(?:provided|presented|described|outlined)\b.{0,160}\b(?:updates|changes)\b',text,re.I))
        vendor_list=introduced or (vendor_list and item['block_type']=='list')
    unit['heading_only']=not any(i['kind']=='text' and not i['is_context'] and i['block_type']!='heading' for i in unit['items'])
    unit['candidate_catalog']=candidates.build(unit)
    return unit


def identify(record):
    record['record_id']=hashlib.sha256(canonical(record).encode()).hexdigest()[:24]
    return record


def metadata(unit,source_ids,blocks):
    bs=[blocks[b] for b in sorted(source_ids)]
    if not bs or any(b['document_id']!=unit['document_id'] for b in bs):
        raise ValueError('Missing or wrong-document M2 blocks')
    hashes={b['document_sha256'] for b in bs}
    if len(hashes)!=1: raise ValueError('Inconsistent PDF identity')
    forms={p.removeprefix('form: ') for p in unit['section_path'] if p.startswith('form: ')}
    return dict(record_schema_version=VERSION,unit_id=unit['unit_id'],document_id=unit['document_id'],
                document_sha256=next(iter(hashes)),section_path=unit['section_path'],standard_id=unit['standard_id'],
                form_ids=sorted(forms),source_context_label=unit['source_context_label'],
                source_block_ids=sorted(source_ids),source_parse_warnings=unit['parse_warnings'],
                value_decimal=None,raw_value=None,row_path=None,column_path=None,row_key=None,column_key=None,
                bbox=None,category=None,region=None,series=None,measure=None,actor_resolution=None,actor_basis=None,assertion_ids=[],causal_assessment='NOT_APPLICABLE')


def context(unit,refs):
    wanted=set(refs);available={i['ref'] for i in unit['items']}
    if wanted-available: raise ValueError('Unknown context ref')
    return [dict(ref=i['ref'],quote=i['text'],source_block_ids=i['source_block_ids'],pages=i['pages'],
                 is_ancestor=i['is_context']) for i in unit['items'] if i['is_context'] or i['ref'] in wanted]


def materialize(unit,response,blocks):
    if unit['unit_kind']=='table': raise ValueError('Table units must bypass LLM materialization')
    records=[];errors=[];primary_roles={}
    for index,choice in enumerate(response['records']):
        try:
            selected=candidates.select(unit['candidate_catalog'],choice['assertion_ids'])
            if choice['evidence_type'] in {'QUANTITATIVE_OBSERVATION','OTHER'}:
                raise ValueError('Type is not a narrative evidence role')
            if any(cid in primary_roles and primary_roles[cid]!=choice['evidence_type'] for cid in choice['assertion_ids']):
                raise ValueError('A candidate cannot have competing primary narrative roles')
            spans=[copy.deepcopy(s) for c in selected for s in c['source_spans']]
            actors={c['source_actor'] for c in selected}
            if len(actors)>1: raise ValueError('Conflicting source actors')
            actor=selected[0]['source_actor']
            ids={b for s in spans for b in s['source_block_ids']}
            record=metadata(unit,ids,blocks)
            record.update(record_kind='NARRATIVE',producer='LLM_CLASSIFICATION',
                          evidence_type=choice['evidence_type'],actor=actor or ACTORS['UNKNOWN'],
                          actor_role=None,actor_resolution='SOURCE_PROVENANCE' if actor else 'UNRESOLVED_SOURCE_ROLE',
                          actor_basis='; '.join(sorted({basis for c in selected for basis in c['actor_basis'].split('; ')})),
                          assertion_ids=choice['assertion_ids'],
                          assertion_text=' '.join(s['quote'] for s in spans),
                          source_spans=spans,context=context(unit,[]),
                          pages=sorted({p for s in spans for p in s['pages']}),
                          post_review_response=None,review_induced_change=None,
                          causal_assessment='NOT_ASSESSED_AT_EXTRACTION',table_cell_ids=[],table_cell=None)
            records.append(identify(record))
            primary_roles.update({cid:choice['evidence_type'] for cid in choice['assertion_ids']})
        except (KeyError,ValueError) as exc:
            errors.append(f'record {index}: {exc}')
    return records,errors


def promote_table(unit,blocks):
    if unit['unit_kind']!='table' or not unit['table_cells']:
        raise ValueError('Expected a structured M2 table unit')
    rows={};columns={};keys=set();ids=set();by_cell={}
    for row in unit['items']:
        if row['kind']!='table_row': continue
        if row['parse_status']!='OK': raise ValueError('Unvalidated M2 table row')
        for cid in row['table_cell_ids']:
            if cid in by_cell: raise ValueError('Cell belongs to multiple rows')
            by_cell[cid]=row
    if set(by_cell)!={c['cell_id'] for c in unit['table_cells']}:
        raise ValueError('Table cell inventory differs from row inventory')
    result=[]
    for cell in unit['table_cells']:
        cid=cell['cell_id'];key=(cell['row_key'],cell['column_key'])
        if cid in ids or key in keys: raise ValueError('Duplicate table cell or row/column identity')
        if cell['table_id']!=unit['table_id']: raise ValueError('Wrong table identity')
        ids.add(cid);keys.add(key)
        for registry,k,path in [(rows,cell['row_key'],cell['row_path']),(columns,cell['column_key'],cell['column_path'])]:
            if not path or (k in registry and registry[k]!=path): raise ValueError('Ambiguous table header identity')
            registry[k]=path
        if len(cell['bbox'])!=4 or not cell['source_word_ids']: raise ValueError('Missing numeric-cell provenance')
        number=Decimal(cell['value'])
        if not number.is_finite(): raise ValueError('Nonfinite table value')
        row=by_cell[cid];record=metadata(unit,row['source_block_ids'],blocks)
        actor={'vendor_submission':'RMS','standard':'FCHLPM','professional_team_report':'Professional Team'}.get(unit['document_type'],'Other/Unknown')
        record.update(record_kind='TABLE_CELL',producer='DETERMINISTIC_M2',evidence_type='QUANTITATIVE_OBSERVATION',
                      actor=actor,actor_role=None,actor_resolution='SOURCE_PROVENANCE',actor_basis='M2_TABLE_DOCUMENT',assertion_text=None,source_spans=[],context=context(unit,[]),
                      pages=row['pages'],post_review_response=False,review_induced_change=False,
                      table_cell_ids=[cid],table_cell=copy.deepcopy(cell),value_decimal=cell['value'],raw_value=cell['raw_value'],
                      row_path=cell['row_path'],column_path=cell['column_path'],row_key=cell['row_key'],column_key=cell['column_key'],
                      bbox=cell['bbox'])
        if len(cell['row_path'])==2 and cell['row_path'][0]=='Category': record['category']=cell['row_path'][1]
        if len(cell['column_path'])==3 and cell['column_path'][1] in {'Historical','Modeled'} and cell['column_path'][2] in {'Number','Rate'}:
            record.update(region=cell['column_path'][0],series=cell['column_path'][1],measure=cell['column_path'][2])
        result.append(identify(record))
    return result


def request_payload(unit,ontology):
    if unit['unit_kind']=='table' or unit['heading_only']:
        raise ValueError('Tables and heading-only units bypass LLM requests')
    return canonical(dict(ontology={k:v for k,v in ontology['types'].items() if k not in {'QUANTITATIVE_OBSERVATION','OTHER'}},
        document={k:unit[k] for k in ['document_type','author','section_path','standard_id','source_context_label','pages']},
        context=[dict(ref=i['ref'],text=i['text']) for i in unit['items'] if not i['assertion_eligible']],
        assertions=[dict(assertion_id=c['candidate_id'],kind=c['kind'],source_actor=c['source_actor'],text=c['text'])
                    for c in unit['candidate_catalog']['candidates']]))


def request_schema(unit,schema):
    if unit['unit_kind']=='table': raise ValueError('No LLM schema for a table unit')
    schema=copy.deepcopy(schema)
    schema['properties']['records']['items']['properties']['assertion_ids']['items']['enum']=[c['candidate_id'] for c in unit['candidate_catalog']['candidates']]
    return schema
