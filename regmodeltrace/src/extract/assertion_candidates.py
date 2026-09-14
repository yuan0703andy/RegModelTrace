"""Source-only sentence/proposition candidates; no annotations or model output."""
import hashlib
import json
import re

VERSION = 'assertion-candidates-1.0'


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def candidate_id(unit_id, spans):
    return 'A' + hashlib.sha256(canonical([unit_id, spans]).encode()).hexdigest()[:20]


def sentence_intervals(text):
    """Sentence punctuation, with decimal, identifier and abbreviation protection."""
    start = 0
    for match in re.finditer(r'[.!?](?:[\"\u201d\u2019)]*)(?=\s|$)', text):
        end = match.end()
        prefix = text[:match.start()+1]
        if text[match.start()] == '.':
            # No whitespace inside model versions/decimals, so they never match.
            if re.search(r'\b(?:Mr|Mrs|Ms|Dr|Prof|vs|etc|al|Fig|Eq|No|St)\.$', prefix, re.I):
                continue
            if re.search(r'\b(?:[A-Za-z]\.){2,}$', prefix):
                continue
            # Numbered/list identifiers at the beginning are not sentences.
            if re.fullmatch(r'\s*(?:[A-Z]|\d+|[A-Z]+-\d+(?:\.\w+)*)\.', text[start:end]):
                continue
        a = start
        while a < end and text[a].isspace():
            a += 1
        if a < end:
            yield a, end, 'SENTENCE'
        start = end
    a = start
    while a < len(text) and text[a].isspace():
        a += 1
    b = len(text.rstrip())
    if a < b:
        yield a, b, 'LOCAL_PROPOSITION'


def build(unit):
    """Account for every item; only eligible items can create evidence candidates."""
    if unit['unit_kind'] == 'table':
        return dict(unit_id=unit['unit_id'], version=VERSION, candidates=[], dispositions=[dict(reason='DETERMINISTIC_TABLE_ROUTE')])
    runs = []
    dispositions = []
    for position, item in enumerate(unit['items']):
        if not item['assertion_eligible']:
            dispositions.append(dict(ref=item['ref'], reason='CONTEXT_OR_HEADING', source_block_ids=item['source_block_ids']))
            continue
        previous = runs[-1][-1][1] if runs else None
        adjacent = bool(runs and runs[-1][-1][0] + 1 == position)
        unfinished = previous and previous['text'].rstrip() and previous['text'].rstrip()[-1] not in '.!?;:'
        # List entries usually stand alone. A paragraph ending mid-sentence can
        # continue into a block M2 called a list (e.g. a citation year).
        continuation_signal = previous and (previous['block_type'] == 'heading' or
            bool(re.match(r'^(?:[a-z]|\d{4}\))', item['text'].lstrip())) or previous['text'].rstrip().endswith('-'))
        caption = previous and bool(re.match(r'^(?:Figure|Table)\s+\d+\s*:', previous['text']))
        join = adjacent and unfinished and continuation_signal and not caption and previous['block_type'] != 'list' and item['block_type'] != 'heading' and previous['source_actor'] == item['source_actor']
        if join:
            runs[-1].append((position, item))
        else:
            runs.append([(position, item)])
    candidates = []
    for run in runs:
        text = ''; mapping = []
        for position, item in run:
            if text:
                text += ' '
            a = len(text); text += item['text']
            mapping.append((a, len(text), position, item))
        for start, end, kind in sentence_intervals(text):
            spans = []; positions = []; origins = []
            for a, b, position, item in mapping:
                left, right = max(a, start), min(b, end)
                if left >= right or not text[left:right].strip():
                    continue
                spans.append(dict(ref=item['ref'], quote=item['text'][left-a:right-a],
                    block_char_start=left-a, block_char_end=right-a,
                    coordinate_system='M2_CHARACTER_HALF_OPEN',
                    source_block_ids=item['source_block_ids'], pages=item['pages']))
                positions.append(position); origins.append(item)
            if not spans:
                continue
            # An eligible requirement heading must be attached to its body.
            if all(i['block_type'] == 'heading' for i in origins):
                dispositions.append(dict(reason='UNRESOLVED_HEADING_FRAGMENT', source_spans=spans))
                continue
            candidates.append(dict(candidate_id=candidate_id(unit['unit_id'], spans),
                ordinal=len(candidates), kind=kind, text=' '.join(s['quote'] for s in spans),
                source_spans=spans, first_item_position=min(positions), last_item_position=max(positions),
                source_actor=origins[0]['source_actor'],
                actor_basis='; '.join(sorted({i['actor_basis'] for i in origins}))))
            if kind == 'LOCAL_PROPOSITION':
                dispositions.append(dict(candidate_id=candidates[-1]['candidate_id'], reason='NO_TERMINAL_SENTENCE_PUNCTUATION'))
    return dict(unit_id=unit['unit_id'], version=VERSION, candidates=candidates, dispositions=dispositions)


def select(catalog, ids):
    lookup = {c['candidate_id']: c for c in catalog['candidates']}
    if not ids or len(ids) != len(set(ids)) or any(i not in lookup for i in ids):
        raise ValueError('Select distinct existing assertion IDs')
    selected = [lookup[i] for i in ids]
    for left, right in zip(selected, selected[1:]):
        if right['ordinal'] != left['ordinal'] + 1 or right['first_item_position'] > left['last_item_position'] + 1:
            raise ValueError('Assertion candidates must be adjacent and in reading order')
        if left['source_actor'] != right['source_actor']:
            raise ValueError('Assertion crosses conflicting source actors')
    return selected
