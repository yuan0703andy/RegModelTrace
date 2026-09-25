# Track A baseline reproduction plan — A0 draft

## Decision now

The three public datasets are locally acquired and hash-pinned, but A1 model runs remain unqualified. TimelyQABench is a **synthetically constructed** temporal retrieval task with Korean queries and gold document IDs; its policy/regulation scenarios are not authentic source law. VersionQA is a 100-question QA evaluation set without evidence IDs; LIT-RAGBench is a supplied-context generator task. They cannot share a single headline score. Source archives are in `datasets/official/` and intentionally excluded from Git.

## A1 order and comparison contract

1. Resolve each benchmark's open items in `public_benchmark_inventory.json`, especially split/cluster leakage, source licenses, and scoring. TimelyQABench is the primary project-defined grouped development/confirmation benchmark. VersionQA's 100 official questions remain untouched confirmation; no VersionQA tuning. LIT-RAGBench is a fixed-generator diagnostic, preferably one-shot confirmation unless a separate split is prospectively frozen.
2. Freeze one local open-weight generator configuration *before* benchmark output is inspected. The Track A research configuration is independent of the RegModelTrace service default and FG-3 model configurations. Retrieval-only TimelyQABench runs need no generator.
3. Run within-benchmark B1 BM25, B2 one pinned dense model, B3 frozen hybrid fusion, and B4 the strongest metadata-aware hybrid that the observed fields permit. Use the same eligible corpus and retrieval budget within each controlled comparison. Preserve publication/availability time separately from effective/valid time; do not infer validity from the former.
4. Qualify the official TimelyRAG implementation on TimelyQABench. `TIMELY_AUTO_ALPHA` is the fair/deployable path. `TIMELY_BEST_ALPHA` uses each query's gold positive IDs to maximize nDCG and is **oracle upper bound only**; it must never appear as an ordinary method. Map reported paper tables to the released execution path before describing any number as faithful. Record `FAITHFUL_TIMELYRAG` separately from a `CONTROLLED_TIMELY_COMPONENT`.
5. Qualify the official VersionRAG implementation on VersionQA. Its Neo4j and external-LLM dependencies make a purely local faithful reproduction unresolved. If unavailable, record `REPRODUCTION_NOT_QUALIFIED`; do not score it as a failed method. A local controlled version-aware component is a distinct result.
6. Split LIT-RAGBench into two contracts. `FAITHFUL_LIT_RAGBENCH` uses the official generator prompt, positive-plus-negative context, official `random.seed(42)` plus sequential `random.shuffle`, and the qualified official scoring contract. It must explicitly set `--num-tasks 114` because the official default is five, and save the actual IDs/order. `CONTROLLED_CONTEXT_DIAGNOSTIC` separately compares positive-only, negative-only, and combined contexts under a prospectively frozen **case-specific** ordering/seed and token budget. It is not an official LIT score. No retrieval Recall@k is reported for either.

## Gold-context and sufficient-context boundaries

TimelyQABench gold IDs support retrieval metrics, and the paper describes them as minimal answer evidence, but that claim has not been independently checked on the acquired bytes. VersionQA provides answer labels but no source evidence IDs; a gold-context condition requires independent source annotation. LIT-RAGBench supplies positive/negative chunks and supports controlled generator tests, but case-level sufficiency and judge validity still need verification. Reference answers are not substituted for evidence.

## Holdout and statistics

No official development split was found in the pinned artifacts. For TimelyQABench, freeze a project-defined development/confirmation partition by evolving document family, not a random query partition; identify or reconstruct family identity before splitting. Preserve all 100 VersionQA questions as untouched confirmation, with development done on TimelyQABench or other independent material. Keep LIT-RAGBench as a one-shot fixed-generator diagnostic unless it becomes a tuning source, in which case first freeze a split. Use paired case-level differences and cluster-aware uncertainty where questions share a source family. Do not pool task-level raw accuracies or infer calibration from these data.

## Execution boundary

No Qwen, retriever, judge, or published-method run occurred in A0. A1 will use DCC compute nodes after a separate frozen runtime plan. FG-3 remains under its existing source and human-gold gates.

## Primary sources

- Nam et al. (2026), *TimelyRAG: Semantic-Temporal Hybrid Retrieval for Time-Critical Question Answering in Overlapping-Evolving Documents*, arXiv:2609.11572, https://arxiv.org/abs/2609.11572 ; official code/data: https://github.com/kaist-dmlab/TimelyRAG .
- Huwiler, Stockinger, and Fürst (2025), *VersionRAG: Version-Aware Retrieval-Augmented Generation for Evolving Documents*, arXiv:2510.08109, https://arxiv.org/abs/2510.08109 ; official code/data: https://github.com/danielhuwiler/versionrag .
- Itai et al. (2026), *LIT-RAGBench: Benchmarking Generator Capabilities of Large Language Models in Retrieval-Augmented Generation*, LREC 2026 / arXiv:2603.06198, https://arxiv.org/abs/2603.06198 ; official code/data: https://github.com/Koki-Itai/LIT-RAGBench .
- Joren et al. (2025), *Sufficient Context: A New Lens on Retrieval-Augmented Generation Systems*, ICLR 2025, https://arxiv.org/abs/2411.06037 .
- Ru et al. (2024), *RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation*, NeurIPS 2024 Datasets and Benchmarks, https://proceedings.neurips.cc/paper_files/paper/2024/hash/27245589131d17368cccdfa990cbf16e-Abstract.html .
