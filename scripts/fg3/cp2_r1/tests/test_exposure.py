from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path


MODULE = Path(__file__).resolve().parents[1] / "exposure.py"
spec = importlib.util.spec_from_file_location("cp2_r1_exposure", MODULE)
assert spec and spec.loader
exposure = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exposure)


def test_stride_one_detects_window_missing_at_stride_three():
    words = [f"word{i}" for i in range(15)]
    query = " ".join(words)
    assert tuple(words[1:13]) in exposure.windows(query)


def test_escaped_json_string_has_same_logical_text(tmp_path: Path):
    phrase = (
        "The reviewed methodology kept coastal gate rates distinct across every hurricane category."
    )
    source = "Prefix " + phrase + " Suffix"
    raw = json.dumps({"source": source}, ensure_ascii=True).encode()
    file = tmp_path / "saved.json"
    file.write_bytes(raw)
    manifest = {"files": [{"path": "saved.json", "sha256": hashlib.sha256(raw).hexdigest()}]}
    matches, failures = exposure.scan_unit(phrase, manifest, tmp_path)
    assert failures == []
    assert matches
    assert matches[0]["json_pointer_or_text"] == "/source"


def test_hash_drift_fails_closed(tmp_path: Path):
    file = tmp_path / "saved.json"
    file.write_text('{"text": "one two three four five six seven eight nine ten eleven twelve"}')
    manifest = {"files": [{"path": "saved.json", "sha256": "0" * 64}]}
    try:
        exposure.scan_unit(
            "one two three four five six seven eight nine ten eleven twelve", manifest, tmp_path
        )
    except ValueError as error:
        assert "hash mismatch" in str(error)
    else:
        raise AssertionError("hash drift was silently accepted")
