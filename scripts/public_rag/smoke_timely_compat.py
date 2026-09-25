"""Non-benchmark smoke of the pinned TimelyRAG compatibility patch.

Dependency shims permit import-only checks; no retriever/model is instantiated.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


EXPECTED_ARCHIVE = "9cbebab7cbf6ecf3d67020efd159ac40f26423fa661bf3925aa19246b9cd5984"
EXPECTED_RETRIEVAL = "2bcee767056192bdb33b78dae7c29e748b70b9fb096e2e782f5d48aca5ae3f19"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> None:
    archive, patch = map(Path, sys.argv[1:3])
    assert sha(archive) == EXPECTED_ARCHIVE
    with tempfile.TemporaryDirectory(prefix="timely-a04-") as tmp:
        root = Path(tmp)
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(root)
        source = next(p for p in root.iterdir() if p.is_dir())
        assert sha(source / "retrieval.py") == EXPECTED_RETRIEVAL
        subprocess.run(["git", "apply", str(patch)], cwd=source, check=True, capture_output=True)
        assert sha(source / "retrieval.py") == EXPECTED_RETRIEVAL
        shims = root / "shims"
        shims.mkdir()
        (shims / "rank_bm25.py").write_text("class BM25Okapi:\n    pass\n")
        (shims / "FlagEmbedding.py").write_text("class BGEM3FlagModel:\n    pass\n")
        env = os.environ.copy()
        env["PYTHONPATH"] = str(shims)
        env["TR_EXPERIMENT_DIR"] = str(root / "default-results")
        help_run = subprocess.run(
            [sys.executable, "-m", "pipeline", "--help"], cwd=source, env=env,
            text=True, capture_output=True, check=True,
        )
        assert "--exp-dir" in help_run.stdout and "--gpu" in help_run.stdout
        # This only verifies that early CLI parsing updates import-time config.
        probe = (
            "import sys; sys.argv=['pipeline','--exp-dir','" + str(root / "custom-results") +
            "','--gpu','7']; import pipeline, config; "
            "assert config.EXP_DIR.endswith('custom-results'); "
            "assert __import__('os').environ['CUDA_VISIBLE_DEVICES']=='7'; "
            "assert all(__import__('pathlib').Path(p).name != 'timelyrag_yonsei_dataset_v2.jsonl' "
            "for p in config.DATASET_PATHS); print('CLI_IMPORT_OK')"
        )
        probe_run = subprocess.run(
            [sys.executable, "-c", probe], cwd=source, env=env,
            text=True, capture_output=True, check=True,
        )
        assert "CLI_IMPORT_OK" in probe_run.stdout
        # Auto alpha accepts observable signals only; this is not a retrieval score.
        alpha_run = subprocess.run(
            [sys.executable, "-c", "import numpy as np; from alpha import choose_alpha_from_signals; "
             "a,_=choose_alpha_from_signals(qet_exists=1.0,gran_id=1.0,gap_avg=2.0,"
             "valid_ratio_terms={'QET_DET':1.0,'QIT_DIT':1.0,'QIT_DET':1.0,'QET_DIT':1.0},"
             "base_scores_norm=np.array([0.8,0.2]),delta_pen=np.array([0.1,0.2]),"
             "mix_finite_ratio=1.0,alpha_grid=[0.0,0.5,1.0]); "
             "assert a in (0.0,0.5,1.0); print('AUTO_ALPHA_OK',a)"],
            cwd=source, env=env, text=True, capture_output=True, check=True,
        )
        print(json.dumps({
            "status": "PASS_NON_CLAIM_BEARING_IMPORT_AND_AUTO_ALPHA_SMOKE",
            "archive_sha256": sha(archive), "patch_sha256": sha(patch),
            "retrieval_py_unchanged_sha256": EXPECTED_RETRIEVAL,
            "cli_import": probe_run.stdout.strip(),
            "auto_alpha": alpha_run.stdout.strip(),
            "limitation": "rank_bm25 and FlagEmbedding are import shims. No full official retriever, model, dataset evaluation, or paper-score parity was run.",
        }))


if __name__ == "__main__":
    run()
