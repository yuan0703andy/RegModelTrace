# TimelyRAG A0.4a compatibility qualification

The source is `kaist-dmlab/TimelyRAG@381019d3add63f93187b06e7696d10bf451a58b5`, preserved as the SHA-256-pinned archive in the acquisition receipt. `patch.diff` has SHA-256 `7cca4e70fcfd85c15e61617b4a342ddd95c17d97389edcd5234b8d17c9dc0a42`. It applies cleanly to that archive and does not touch `retrieval.py` (SHA-256 `2bcee767056192bdb33b78dae7c29e748b70b9fb096e2e782f5d48aca5ae3f19`).

Every edit is mechanical: the three `from .metrics` calls become top-level imports because the released launcher uses `python -m pipeline`; the fourth default dataset path changes from the absent Yonsei filename to the released University filename; `--exp-dir` and `--gpu` are parsed before `config` and retrieval imports so their import-time effects are real. The patch does not alter temporal scoring, alpha selection, normalization, candidate pool, ranking, or metrics. The README's advertised `--datasets` option remains unimplemented and must not be assumed available.

On 2026-09-25, `smoke_timely_compat.py` ran on a Duke DCC CPU compute node using the pinned archive and patch. It passed patch application, unchanged retrieval source, CLI `--help`, early `--exp-dir`/`--gpu` import behavior, default dataset filename, and a synthetic call to `choose_alpha_from_signals` returning an allowed alpha. `rank_bm25` and `FlagEmbedding` were **import shims**; no retriever or model was instantiated. This is a non-claim-bearing compatibility smoke, not full official-runtime or benchmark parity. The exact receipt is in `smoke_receipt.json`.

The released `retrieval.py` calls `choose_alpha_from_signals` with observable query/candidate signals. In contrast, `rerank_with_alpha_grid` chooses a best alpha by evaluating each candidate against per-query `pos_ids`; that path is an oracle upper bound, never an ordinary baseline.

## Paper table to code path

| Paper object | Relevant released path | Qualification |
|---|---|---|
| Table 4, TimelyQABench nDCG/MAP/Recall/Hit at 10 | `pipeline.run_pipeline` → `evaluate_2stage` → auto-alpha, `metrics.py`; `config.K=10` | Structural match for BM25/BGE-M3 and top-10 metrics. Numeric parity is untested. The released code uses `STAGE1_TOPN=100`, while the paper's candidate-pool sensitivity table identifies 50 as its main comparison point. Exact Table 4 configuration is therefore unresolved. |
| Table 5, nDCG/MAP at 5 | Same pipeline has `K=10` | No released run path at `K=5` was verified. Paper's Oracle Temporal Filtering is not the same as released `best-alpha` gold-ID grid search. Do not map one to the other. |
| Figure 5, optimal alpha distribution | `pipeline.py` persists `best-alpha` histogram; `retrieval.py` uses positive IDs for that selection | Oracle diagnostic only. The auto-alpha histogram is a different output. |
| Tables 8–10, ablation/overhead/candidate-pool sensitivity | No released CLI configuration for ablations, timing isolation, or pool sweep was verified | Not reproducible from the default runner as a faithful paper-table result without further code/config evidence. |

The authors describe first/second alpha heuristics for different datasets in Section 5.2, but the pinned public pipeline exposes one `choose_alpha_from_signals` call for the released TimelyQABench path. No paper number has been reproduced here. The proper prospective label is `FAITHFUL_TIMELYRAG_PATCHED_CANDIDATE`, with numeric paper parity **unqualified** until the pool/top-k and dependency configuration is resolved. The public benchmark can still support a clearly labeled controlled comparison at the released-code settings.

Primary source: Youngeun Nam, Joeun Kim, Hwanjun Song, Susik Yoon, Jae-Gil Lee, and Byung Suk Lee (2026), *TimelyRAG: Semantic-Temporal Hybrid Retrieval for Time-Critical Question Answering in Overlapping-Evolving Documents*, arXiv:2609.11572, https://arxiv.org/html/2609.11572v1 ; pinned code https://github.com/kaist-dmlab/TimelyRAG/tree/381019d3add63f93187b06e7696d10bf451a58b5 .
