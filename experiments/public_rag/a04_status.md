# Track A A0.4 checkpoint — 2026-09-25

**Status: planning qualification advanced; A0 execution qualification is not closed; A1 full execution is not authorized.** No generator, retrieval benchmark, LIT judge, or FG-3 model run was performed.

TimelyRAG: the pinned public runner requires the mechanical `timely_compat/patch.diff`. A DCC compute-node smoke verified application, top-level CLI/import behavior, default dataset filename, and a synthetic auto-alpha call without changing `retrieval.py`. It used dependency import shims and did not execute BM25, BGE-M3, full ranking, or paper-score reproduction. Paper Table 4 maps structurally to the top-10 auto-alpha path, but the released `STAGE1_TOPN=100` versus the paper's N=50 main point remains a material numeric-parity question. Tables 5 and 8–10 are not mapped to a verified default-runner path. Best-alpha remains gold-ID oracle only.

TimelyQABench: 12,000 released rows were grouped by exact document-text overlap before any Track A model output. Distinct document IDs were insufficient: 397 exact text hashes recur across rows, creating a largest connected component of 486 rows. The frozen project split is 9,699 development / 2,301 confirmation, with no exact text crossing partitions. Near-duplicate and template leakage remains unaudited; the giant component is development-only.

LIT-RAGBench: a planned pinned local judge and 30-case human audit subset are frozen, with separate official global ordering and controlled case-specific ordering. The judge is **not yet qualified**: no answer outputs or independent human scores exist. VersionQA remains untouched 100-question end-to-end confirmation; evidence annotation is optional for that role and required for retrieval-specific claims. Public redistribution of raw or derivative benchmark artifacts remains separate from internal execution planning.

The checkpoint does not modify frozen FG-2/FG-3 materials. A1 requires its own runtime/config freeze and authorization. The prior checkout contained unrelated dirty files; they were not staged with this change.
