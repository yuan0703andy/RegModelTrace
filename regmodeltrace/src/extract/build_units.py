"""Deterministic M2-to-semantic-unit construction. No gold or model inputs."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sys

import pyarrow as pa
import pyarrow.parquet as pq


def canonical(x):
    return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))


def sha(x):
    return hashlib.sha256(x.encode() if isinstance(x,str) else x).hexdigest()


def load(path):
    return json.loads(path.read_text())


def write(path,obj):
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')


def build(source,manifest,config,out):
    cfg=load(config);docs={d['document_id']:d for d in load(manifest)}
    names=['parsed_blocks.parquet','units.json','continuations.json','tables.json','parser_run_manifest.json']
    input_hashes={n:sha((source/n).read_bytes()) for n in names}
    if (source/'fatal_error.json').exists():
        raise ValueError('Failed M2 run cannot be a semantic input')
    blocks=pq.read_table(source/'parsed_blocks.parquet').to_pylist();bm={b['block_id']:b for b in blocks}
    nodes={u['unit_id']:u for u in load(source/'units.json')};edges=load(source/'continuations.json');tables=load(source/'tables.json')
    heading={b['parent_unit_id']:b for b in blocks if b['block_type']=='heading'}
    dispositions={b['block_id']:dict(block_id=b['block_id'],document_id=b['document_id'],
        page=b['page_start'],disposition='MARGIN_NOT_SEARCHABLE' if not b['is_searchable'] else 'PENDING',unit_ids=[])
        for b in blocks}
    def path_for(b):
        path=[];at=b['parent_unit_id'];seen=set()
        while at:
            if at in seen or at not in nodes:
                raise ValueError('Invalid M2 ancestor graph')
            seen.add(at);u=nodes[at];path.append(u);at=u['parent_unit_id']
        return list(reversed(path))
    results=[]
    def append_unit(body,kind='text',table=None):
        if not body:
            return
        first=body[0];path=path_for(first);bodyids={b['block_id'] for b in body};context=[];size=0
        for u in reversed(path):
            b=heading.get(u['unit_id'])
            if b and b['block_id'] not in bodyids and size+len(b['text'])<=cfg['max_context_chars']:
                context.insert(0,b);size+=len(b['text'])
        # Maintain exact source blocks; short references are local to this unit only.
        items=[]
        for b in context+body:
            if any(b['block_id'] in x['source_block_ids'] for x in items):
                continue
            items.append(dict(ref='b'+str(len(items)),kind='text',text=b['text'],
                source_block_ids=[b['block_id']],pages=[b['page_start']],table_cell_ids=[],
                is_context=b['block_id'] not in bodyids,parse_status=b['parse_status']))
        if table:
            rows=defaultdict(list)
            for c in table['cells']:
                rows[tuple(c['row_path'])].append(c)
            for ri,(row,cs) in enumerate(rows.items()):
                text=' / '.join(row)+' | '+'; '.join(' / '.join(c['column_path'])+' = '+c['raw_value'] for c in cs)
                wids={w for c in cs for w in c['source_word_ids']}|{c['row_label_word_id'] for c in cs}
                relevant=[b['block_id'] for b in body if any(wids.intersection(l['word_ids']) for l in b['line_geometry'])]
                if not relevant:
                    raise ValueError('A table row lacks M2 source blocks')
                items.append(dict(ref='r'+str(ri),kind='table_row',text=text,source_block_ids=relevant,
                    pages=[table['page']],table_cell_ids=[c['cell_id'] for c in cs],is_context=False,parse_status='OK'))
            # Keep raw source prose/footnotes as well as structured rows. Numeric interpretation uses rows.
            promptitems=items
        else:
            promptitems=items
        ids=[b['block_id'] for b in body];uid=sha(canonical([first['document_id'],kind,ids,table['table_id'] if table else None]))[:24]
        doc=docs[first['document_id']]
        result=dict(unit_id=uid,document_id=first['document_id'],document_type=doc['document_type'],
            author=doc['author'],document_title=doc['title'],section_path=[u['kind']+': '+u['label'] for u in path],
            standard_id=first['standard_id'],source_context_label=first['source_context_label'],
            source_block_ids=ids,context_block_ids=[b['block_id'] for b in context],
            pages=sorted({b['page_start'] for b in body}),unit_kind=kind,
            text='\n'.join(i['text'] for i in promptitems),items=promptitems,
            table_id=table['table_id'] if table else None,table_cells=table['cells'] if table else [],
            parse_warnings=sorted({b['parse_status'] for b in body if b['parse_status']!='OK'}),
            builder_version=cfg['version'],reading_order=min(b['reading_order'] for b in body))
        results.append(result)
        for b in body:
            d=dispositions[b['block_id']];d['disposition']='INCLUDED';d['unit_ids'].append(uid)
    assigned=set()
    for t in tables:
        wordids=set(t['numeric_word_ids'])|{w for level in t['header_levels'] for h in level for w in h['word_ids']}
        body=[b for b in blocks if b['is_searchable'] and b['document_id']==t['document_id'] and b['page_start']==t['page']
              and any(wordids.intersection(l['word_ids']) for l in b['line_geometry'])]
        append_unit(body,'table',t);assigned.update(b['block_id'] for b in body)
    # Connected continuation components must not be split by the length bound.
    parent={b['block_id']:b['block_id'] for b in blocks}
    def find(x):
        while parent[x]!=x:
            x=parent[x]
        return x
    for e in edges:
        a,b=e['from_block_id'],e['to_block_id']
        if a not in assigned and b not in assigned and bm[a]['is_searchable'] and bm[b]['is_searchable']:
            parent[find(b)]=find(a)
    grouped=defaultdict(list)
    for b in blocks:
        if b['is_searchable'] and b['block_id'] not in assigned:
            grouped[(b['document_id'],b['parent_unit_id'])].append(b)
    for members in grouped.values():
        components=defaultdict(list)
        for b in members:
            components[find(b['block_id'])].append(b)
        chunks=sorted(components.values(),key=lambda xs:xs[0]['reading_order'])
        pending=[];size=0
        for component in chunks:
            n=sum(len(b['text'])+1 for b in component)
            if pending and size+n>cfg['max_body_chars']:
                append_unit(sorted(pending,key=lambda b:b['reading_order']));pending=[];size=0
            pending.extend(component);size+=n
        append_unit(sorted(pending,key=lambda b:b['reading_order']))
    results.sort(key=lambda x:(x['reading_order'],x['unit_id']))
    missing=[d for d in dispositions.values() if d['disposition']=='PENDING']
    if missing:
        raise ValueError('Unaccounted body blocks')
    continuation_failures=[];cross_kind_links=[]
    for e in edges:
        a,b=e['from_block_id'],e['to_block_id']
        if bm[a]['is_searchable'] and bm[b]['is_searchable'] and not (set(dispositions[a]['unit_ids'])&set(dispositions[b]['unit_ids'])):
            if a in assigned or b in assigned:
                cross_kind_links.append(dict(source_edge=e,from_unit_ids=dispositions[a]['unit_ids'],
                    to_unit_ids=dispositions[b]['unit_ids'],resolution='SEPARATE_TABLE_AND_TEXT_UNITS',
                    note='Retained M2 connection crosses a numeric-panel boundary; no prose continuation is inferred.'))
            else:
                continuation_failures.append(e)
    if continuation_failures:
        raise ValueError('Continuation was split across semantic units: '+canonical(continuation_failures[:5]))
    out.mkdir(parents=True,exist_ok=True)
    pq.write_table(pa.Table.from_pylist(results),out/'semantic_units.parquet',compression='zstd')
    write(out/'block_dispositions.json',list(dispositions.values()))
    write(out/'continuation_unit_links.json',cross_kind_links)
    receipt=dict(version=cfg['version'],input_sha256=input_hashes,config_sha256=sha(config.read_bytes()),
        code_sha256=sha(Path(__file__).read_bytes()),logical_units_sha256=sha(canonical(results)),
        output_sha256=sha((out/'semantic_units.parquet').read_bytes()),units=len(results),
        body_blocks=sum(d['disposition']=='INCLUDED' for d in dispositions.values()),
        excluded_margin_blocks=sum(d['disposition']=='MARGIN_NOT_SEARCHABLE' for d in dispositions.values()),
        max_unit_chars=max(len(u['text']) for u in results),continuations_preserved=len(edges),
        continuations_within_unit=len(edges)-len(cross_kind_links),cross_kind_continuation_links=len(cross_kind_links),
        gold_inputs=[],semantic_labels_assigned=False,status='COMPLETE')
    write(out/'semantic_units_manifest.json',receipt)
    print(canonical(receipt))


if __name__=='__main__':
    cli=argparse.ArgumentParser(description=__doc__)
    for k in ['source','manifest','config','output']:
        cli.add_argument('--'+k,type=Path,required=True)
    args=cli.parse_args();build(args.source,args.manifest,args.config,args.output)
