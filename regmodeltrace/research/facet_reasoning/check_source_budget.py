"""CPU-only tokenizer diagnostic; no weights, inference, decisions, or truth reads."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from regmodeltrace.research.facet_reasoning.token_budget import count_chat_tokens


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--pilot', type=Path, required=True)
    p.add_argument('--model-config', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    if a.output.exists():
        raise ValueError('Refusing to overwrite a source budget diagnostic')
    config = json.loads(a.model_config.read_text())
    cases = json.loads(a.pilot.read_text())
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(config['model_path'], local_files_only=True)
    rows = []
    # Upper-bound navigation prototype, not actual B/C requests: facets and scope
    # must first be finalized by real humans. Long proposed subsections inflate it.
    system = ('You classify documentary support for atomic regulatory facets. '
              'Use only bounded evidence. Reviewer verification is not vendor demonstration.')
    for c in cases:
        payload = {'requirement':c['requirement_text'],
                   'proposed_facets':[{'facet_id':f['facet_id'],'text':f['text']} for f in c['facets']],
                   'evidence':[{'handle':f'E{i:02d}','role':e['actor_role'],'text':e['text']}
                               for i,e in enumerate(c['evidence'],1)]}
        messages = [{'role':'system','content':system},
                    {'role':'user','content':json.dumps(payload,ensure_ascii=False,sort_keys=True)}]
        count = count_chat_tokens(tokenizer, messages)
        rows.append({'case_id':c['case_id'],'navigation_prototype_input_tokens':count,
                     'reserved_output_tokens':config['max_output_tokens'],
                     'prototype_fits':count + config['max_output_tokens'] <= config['max_model_len']})
    a.output.write_text(json.dumps({
        'status':'TOKENIZATION_ONLY_NOT_INFERENCE_NOT_FINAL_MODEL_REQUESTS',
        'model_inference_runs':0,'model_weights_loaded':False,
        'pilot_sha256':hashlib.sha256(a.pilot.read_bytes()).hexdigest(),
        'max_model_len':config['max_model_len'],
        'prototype_over_budget_count':sum(not r['prototype_fits'] for r in rows),
        'note':'Navigation scope is not a frozen model context. Final verified human scope requires exact B/C template counting again, without truncation.',
        'cases':rows},indent=2,sort_keys=True)+'\n')


if __name__ == '__main__':
    main()
