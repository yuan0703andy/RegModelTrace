# RegModelTrace natural-document inventory — 2026-09-24

This is a source and readiness inventory for a possible natural evidence-boundary study. It does not select cases, adjudicate truth, run retrieval, or run a model. The two completed synthetic diagnostics (FG-2 and the Qwen3.8 boundary fixture) remain separate from any natural-document evaluation.

## Verified local custody

All **45 Florida PDF paths** in the [existing inventory](../corpus-inventory-20260923/inventory.json) still exist locally and match its recorded SHA-256 and byte size. They represent **33 distinct PDF contents**, not 45 independent documents. All six referenced source manifests also match their recorded hashes. The [machine-readable verification receipt](verification.json) records every checked path. A separate SEC filing-manual PDF under `regmodeltrace/data/external/sec-efm` is outside this Florida count.

After normalizing three legacy role names, the 45 paths consist of 7 regulator, 19 vendor, and 19 reviewer paths; distinct-content counts by role are 3, 15, and 15. Duplicate paths occur across historical fixtures and protected partitions. The previous [full per-path CSV](../corpus-inventory-20260923/inventory.csv) retains document IDs, editions, source URLs, local paths, hashes, dataset groups, and exposure labels. These checks establish local file identity, not parser accuracy or independent human truth.

The frozen Scale-1 parser manifest enumerates **20 worker documents**, including four Florida Public PDFs marked `SCALE_UNLABELLED`; the larger Scale-1 control plane has 28 logical documents when protected Verisk Validation D and KCC Test E records are counted. The combined parsed blocks, source pages, source words, semantic units, tables, diagnostics, and request assets are present locally. The request-freeze receipt lists 47,458 source assertions, 18,350 dispositions, 128 small requests, and 4,096 large requests. Those are workload counts, **not adjudicated natural cases**. Group-level artifact presence does not certify that every candidate assertion has faithful source-span reconstruction.

A targeted DCC check found the six PDFs below plus `parser_manifest.json` and `processed/parsed_blocks.parquet` at `/hpc/home/yh421/CIRCAD-LLM/regmodeltrace/data/corpus/scale-1/`. This was an existence check; this report does not claim current remote byte-for-byte equivalence. No compute or inference job was run for this inventory.

## Most plausible new source pool

The four `SCALE_UNLABELLED` Florida Public files form **two standards-cycle vendor/reviewer pairs**, not four independent corpora:

| Cycle | Regulator text | Vendor submission | Professional Team report |
| --- | --- | --- | --- |
| 2021 | [`shared_standards_2021_standards.pdf`](../../regmodeltrace/data/corpus/scale-1/raw/shared_standards_2021_standards.pdf) | [`florida_public_2021_fphlm_submission.pdf`](../../regmodeltrace/data/corpus/scale-1/raw/florida_public_2021_fphlm_submission.pdf) | [`florida_public_2021_fphlm_review.pdf`](../../regmodeltrace/data/corpus/scale-1/raw/florida_public_2021_fphlm_review.pdf) |
| 2023 | [`shared_standards_2023_standards.pdf`](../../regmodeltrace/data/corpus/scale-1/raw/shared_standards_2023_standards.pdf) | [`florida_public_2023_fphlm_submission.pdf`](../../regmodeltrace/data/corpus/scale-1/raw/florida_public_2023_fphlm_submission.pdf) | [`florida_public_2023_fphlm_review.pdf`](../../regmodeltrace/data/corpus/scale-1/raw/florida_public_2023_fphlm_review.pdf) |

The standards PDFs are already in the `HISTORICAL_CLOSED` Scale-1 partition and may contain previously exposed clauses. `SCALE_UNLABELLED` means these four PDFs have no frozen semantic labels in that split; it **does not establish that every passage is unseen**. Before calling any selected case independent, check whether its clause, vendor passage, reviewer passage, or substantially equivalent question was used in development, demos, adjudication, or diagnostics.

## Readiness by proposed panel

| Panel | Source material now present | Current gate |
| --- | --- | --- |
| A. Requirement semantics | 2021/2023 standards plus paired vendor text. Broad searches show illustrative and mandatory wording, but hits have not been context-adjudicated. | Verify exact clause, defined terms, surrounding exceptions, vendor evidence, and prior exposure. No natural cases selected. |
| B. Reviewer scrutiny versus challenge | Both Florida Public Professional Team reports. They contain review, verification, deficiency, and revision language. | Read complete comment/disposition context; do not classify on verbs alone. No human labels. |
| C. Review-to-modification link | Paired submissions and reviewer reports allow a bounded cross-document search. | Reconstruct chronology and exact object of a revision. Distinguish revised disclosure/response from a change to model method or implementation. No causal truth freeze. |

Two **screening leads, not adjudicated cases**, illustrate why Panel C needs careful source-context review. The 2023 Professional Team report, physical PDF page 7, says it confirmed no hurricane-model changes since the initial submission while also reviewing supporting material for hazard-model updates. On physical page 27 it records a revised response to M-6.4 for the final revised submission. The latter explicitly concerns a disclosure response; it cannot by itself establish a model-method modification. These observations have not been paired with complete vendor context or assessed for earlier exposure.

## Existing exposure and human-truth boundary

Gold Case 001 and the FG-1 source issues (ARA M-3.B, CoreLogic CI-5, RMS M-3.B, CoreLogic M-2) are real-source **exposed diagnostics**, not fresh held-out cases. FG-2 and the recent Qwen3.8 boundary set are **synthetic diagnostics**. Historical Impact, CoreLogic, Verisk, and KCC alignment fixtures have seen prior evaluation; KCC Test E remains closed. Their original PDFs can clarify interpretation rules, but their outcomes cannot be relabelled as new independent evidence.

JA-1H currently records real human source verification as pending and both signed independent returns as not created. FT-1 has 24 prepared candidate cases but zero eligible pilot cases while source-scope verification and independent human adjudication remain pending. The FT-1 receipt names an exported ZIP at a Downloads path that was not present in this local check; underlying source PDFs are present. Neither workflow supplies completed new human truth for the proposed panels.

## Next narrow gate

Audit exposure for the two Florida Public pairs and the relevant standards clauses, then inspect a small mix of clear and difficult **source-grounded candidate** passages with full surrounding context and exact PDF locations. Record cases that are ambiguous or not adjudicable rather than forcing panel quotas or assuming 30–40 usable cases exist. Only after independent human adjudication and a truth freeze should the same evidence be sent to the active Qwen2.5 default and opt-in Qwen3.8 candidate for a natural-case comparison. No model run or new gold was produced here.
