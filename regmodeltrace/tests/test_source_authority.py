import json
from pathlib import Path

from regmodeltrace.source_authority import FrozenCorpusAuthority, build_task1_source_authority


ROOT = Path(__file__).resolve().parents[2]


def test_snapshot_and_index_build_are_separate_and_deterministic(tmp_path):
    first = build_task1_source_authority(ROOT, tmp_path / "first", created_at="time-one")
    second = build_task1_source_authority(ROOT, tmp_path / "second", created_at="time-two")
    assert first["corpus_snapshot"]["corpus_snapshot_id"] == second["corpus_snapshot"]["corpus_snapshot_id"]
    assert first["index_build_manifest"]["index_build_id"] == second["index_build_manifest"]["index_build_id"]
    assert "retrieval_artifact_manifest_sha256" not in first["corpus_snapshot"]
    assert first["index_build_manifest"]["corpus_snapshot_id"] == first["corpus_snapshot"]["corpus_snapshot_id"]


def test_retrieval_config_changes_only_index_identity(tmp_path):
    first = build_task1_source_authority(ROOT, tmp_path / "first", created_at="time-one")
    changed_config = {
        "retrieval": {
            "document_role_order": ["STANDARDS", "PROFESSIONAL_TEAM_REPORT", "VENDOR_SUBMISSION"],
            "passages_per_role": 4,
            "rrf_k": 60,
            "query": "unchanged_user_question",
            "planner": None,
        },
        "embedding": {
            "model": "sentence-transformers/all-MiniLM-L6-v2",
            "model_revision": "1110a243fdf4706b3f48f1d95db1a4f5529b4d41",
            "maximum_sequence_length": 256,
            "device": "cpu",
        },
    }
    second = build_task1_source_authority(
        ROOT,
        tmp_path / "second",
        created_at="time-two",
        retrieval_config_override=changed_config,
    )
    assert first["corpus_snapshot"]["corpus_snapshot_id"] == second["corpus_snapshot"]["corpus_snapshot_id"]
    assert first["index_build_manifest"]["index_build_id"] != second["index_build_manifest"]["index_build_id"]


def test_real_m3b_passage_round_trip(tmp_path):
    output = tmp_path / "authority"
    build_task1_source_authority(ROOT, output)
    resolver = FrozenCorpusAuthority(ROOT, output)
    receipt = resolver.resolve_source("Pb842ca0167c52c4b9ccd")
    assert receipt["status"] == "RESOLVED"
    assert receipt["document_role"] == "STANDARDS"
    assert receipt["pages"] == [120]
    assert "each coastal segment" in receipt["quote"]
    assertion = receipt["assertions"][0]
    assert assertion["source_file_hash_verified"] is True
    assert assertion["document_sha256"] == "6532900dd1394149fecaf3bacf13e5dc24b080b056e51da014a46ee964d0b0a4"
    assert assertion["location_precision"] == "EXACT_GEOMETRY"
    assert all(span["page_text_sha256"] for span in assertion["source_spans"])
    assert all(span["bbox"] for span in assertion["source_spans"])


def test_multi_assertion_passage_preserves_canonical_separator(tmp_path):
    output = tmp_path / "authority"
    build_task1_source_authority(ROOT, output)
    resolver = FrozenCorpusAuthority(ROOT, output)
    receipt = resolver.resolve_source("P235e3ad6e158b368201a")
    assert receipt["status"] == "RESOLVED"
    assert len(receipt["assertions"]) == 4
    assert receipt["quote"] == "\n".join(row["quote"] for row in receipt["assertions"])


def test_direct_source_span_round_trip_and_unknown_fails_closed(tmp_path):
    output = tmp_path / "authority"
    build_task1_source_authority(ROOT, output)
    resolver = FrozenCorpusAuthority(ROOT, output)
    passage = resolver.resolve_source("Pb842ca0167c52c4b9ccd")
    source_span_id = passage["assertions"][0]["source_spans"][0]["source_span_id"]
    span = resolver.resolve_source(source_span_id)
    assert span["status"] == "RESOLVED"
    assert span["requested_type"] == "SOURCE_SPAN"
    assert {item["source_span_id"] for item in span["source_spans"]} == {source_span_id}
    failed = resolver.resolve_source("A_UNKNOWN")
    assert failed["status"] == "FAILED"
    assert failed["error"] == "ID_NOT_IN_SNAPSHOT"
    assert failed["fuzzy_substitution_used"] is False


def test_source_hash_mismatch_fails_closed(tmp_path):
    output = tmp_path / "authority"
    build_task1_source_authority(ROOT, output)
    resolver = FrozenCorpusAuthority(ROOT, output)
    document_id = "fchlpm_2019_hurricane_standards"
    resolver._document_hash_cache[document_id] = "0" * 64
    failed = resolver.resolve_source("Pb842ca0167c52c4b9ccd")
    assert failed["status"] == "FAILED"
    assert failed["error"] == "SOURCE_HASH_MISMATCH"
    assert failed["fuzzy_substitution_used"] is False


def test_real_geometry_failure_is_resolved_with_warning(tmp_path):
    output = tmp_path / "authority"
    build_task1_source_authority(ROOT, output)
    resolver = FrozenCorpusAuthority(ROOT, output)
    for passage in resolver.passages.values():
        if any(
            resolver.blocks.get(block_id, {}).get("parse_status") == "ALIGNMENT_FAILED"
            for block_id in passage.get("source_block_ids", [])
        ):
            receipt = resolver.resolve_source(passage["passage_id"])
            if receipt["status"] == "RESOLVED" and "SOURCE_GEOMETRY_UNAVAILABLE" in receipt["warnings"]:
                assert receipt["location_precision"] == "PAGE_TEXT"
                return
    raise AssertionError("No real degraded-geometry passage resolved with the required warning")


def test_bound_embedding_and_passage_hashes_match(tmp_path):
    output = tmp_path / "authority"
    built = build_task1_source_authority(ROOT, output)
    manifest = built["index_build_manifest"]
    paths = {item["artifact_role"]: item for item in manifest["artifacts"]}
    assert paths["passage_inventory"]["sha256"] == "dfb1f205bdd446d4219d219518560ed862d0f6c9edb5e9f0a312002f1b28f05f"
    assert manifest["passage_count"] == 6009
    assert manifest["embedding_dimension"] == 384
    stored = json.loads((output / "index_build_manifest.json").read_text())
    assert stored == manifest
