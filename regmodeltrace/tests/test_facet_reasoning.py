from __future__ import annotations

import pytest

from regmodeltrace.research.facet_reasoning.adjudication import agreement
from regmodeltrace.research.facet_reasoning.aggregate import aggregate_relation
from regmodeltrace.research.facet_reasoning.baselines import build_request
from regmodeltrace.research.facet_reasoning.schema import (
    EvidenceSufficiency,
    FacetCase,
    FacetDefinition,
    FacetState,
    Relation,
)


def test_aggregation_separates_missing_proof_from_conflict() -> None:
    assert aggregate_relation(
        constraint_status="PRESCRIBED",
        evidence_sufficiency=EvidenceSufficiency.SUFFICIENT,
        facet_states=[FacetState.DEMONSTRATED, FacetState.NOT_DEMONSTRATED],
    ) == Relation.PARTIALLY_ALIGNED
    assert aggregate_relation(
        constraint_status="PRESCRIBED",
        evidence_sufficiency=EvidenceSufficiency.SUFFICIENT,
        facet_states=[FacetState.DEMONSTRATED, FacetState.CONTRADICTED],
    ) == Relation.CONFLICT


def test_insufficient_has_no_relation() -> None:
    assert aggregate_relation(
        constraint_status="PRESCRIBED",
        evidence_sufficiency=EvidenceSufficiency.INSUFFICIENT,
        facet_states=[FacetState.DEMONSTRATED],
    ) is None


def test_condition_c_output_excludes_relation_and_host_identity() -> None:
    case = FacetCase(
        case_id="C1",
        comparison_id="CMP1",
        corpus_id="corpus",
        requirement_id="G-1",
        requirement_text="A requirement",
        constraint_status="PRESCRIBED",
        facets=[FacetDefinition(facet_id="F1", text="A facet")],
        evidence=[],
        vendor_group="vendor",
        model_version_group="version",
        requirement_family="G",
        regulator_text_group="hash",
        source_group_ids=[],
        revision_ancestry="revision",
        review_ancestry="review",
    )
    request = build_request(case, "C")
    properties = request["output_schema"]["properties"]
    assert set(properties) == {"facets"}
    assert properties["facets"]["additionalProperties"] is False
    assert request["request_id"] == "FT1-C-C1"


def test_agreement_rejects_unsigned_machine_like_returns() -> None:
    value = {"adjudicator_name": None, "adjudication_date": None, "attestation": None, "cases": []}
    with pytest.raises(ValueError, match="unsigned"):
        agreement(value, value)


def test_source_scope_audit_denies_truth_before_opening(tmp_path) -> None:
    from regmodeltrace.research.facet_reasoning.audit_source_scope import read_json

    reads = []
    with pytest.raises(PermissionError, match='cannot read truth'):
        read_json(tmp_path / 'comparison_truth.json', reads)
    assert reads == []


def test_builder_cannot_overwrite_retired_audited_pack(tmp_path, monkeypatch) -> None:
    import sys
    from regmodeltrace.research.facet_reasoning import build_dataset

    report = tmp_path / 'source_scope_audit' / 'eligibility_report.json'
    report.parent.mkdir()
    report.write_text('{}')
    monkeypatch.setattr(sys, 'argv', ['builder', '--input-root', str(tmp_path / 'absent'),
                                    '--output-root', str(tmp_path)])
    with pytest.raises(ValueError, match='cannot be overwritten'):
        build_dataset.main()
    assert report.read_text() == '{}'


def simple_source_case():
    from regmodeltrace.research.facet_reasoning.schema import EvidenceProposition
    return FacetCase(
        case_id='fresh', comparison_id='fresh', corpus_id='new', requirement_id='G-1',
        requirement_text='The vendor shall document a process.', constraint_status='PRESCRIBED',
        facets=[FacetDefinition(facet_id='f', text='Document a process.')],
        evidence=[EvidenceProposition(proposition_id='p', actor_role='VENDOR_SUBMISSION',
                                     text='Our documented process is implemented.',
                                     document_id='source', pages=[2])],
        vendor_group='v', model_version_group='y', requirement_family='G',
        regulator_text_group='r', source_group_ids=['s'], revision_ancestry='a', review_ancestry='b')


def test_document_roles_reach_model_context_and_unknown_roles_fail():
    from regmodeltrace.research.facet_reasoning.baselines import model_payload
    case = simple_source_case()
    payload, bindings = model_payload(case)
    assert payload['vendor_evidence'][0]['text'] == case.evidence[0].text
    assert bindings == {'E01': 'p'}
    case.evidence[0].actor_role = 'AMBIGUOUS'
    with pytest.raises(ValueError, match='Unknown provenance'):
        model_payload(case)


def test_signed_empty_return_is_not_a_human_gate():
    from regmodeltrace.research.facet_reasoning.adjudication import validate_return
    with pytest.raises(ValueError, match='nonempty'):
        validate_return({'adjudicator_name':'Human A', 'adjudication_date':'2026-09-15',
                         'attestation':'Independent annotation', 'cases':[]})


def test_source_reconstruction_does_not_accept_copy_errors():
    import hashlib
    from regmodeltrace.research.facet_reasoning.prepare_source_only import verify_block
    text = 'Complete source sentence.'
    h = hashlib.sha256(text.encode()).hexdigest()
    pages = {('d',1): {'text':text,'page_text_sha256':h}}
    block = {'block_id':'b','document_id':'d','text':text,'text_sha256':h,
             'source_spans':[{'page':1,'start':0,'end':len(text),'page_text_sha256':h}]}
    verify_block(block,pages)
    block['source_spans'][0]['start'] = 3
    with pytest.raises(ValueError, match='reconstruction failed'):
        verify_block(block,pages)


def test_token_budget_counts_mapping_token_ids_not_fields():
    from regmodeltrace.research.facet_reasoning.token_budget import count_chat_tokens
    class Tokenizer:
        def apply_chat_template(self, *args, **kwargs):
            return {'input_ids':list(range(13000)), 'attention_mask':[1]*13000}
    assert count_chat_tokens(Tokenizer(), []) == 13000


def test_unmatched_a_cannot_support_adaptation_or_representation_decision():
    from regmodeltrace.research.facet_reasoning.score_phase1 import decide
    assert decide({}, {}, [], {}, 0) == 'EVIDENCE_INCONCLUSIVE'
