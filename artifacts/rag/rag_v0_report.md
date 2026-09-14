# RegModelTrace RAG v0 MVP Report

## Result

`REGMODELTRACE_RAG_V0_MVP = PASS`

The bounded eight-question product run passes the three predeclared MVP gates. It is the first connected RegModelTrace pipeline that takes a user question, searches all three document roles at passage level, supplies role-partitioned retrieved evidence to Qwen32B, and renders host-resolved citations back to the PDFs.

| MVP hard gate | Result |
|---|---|
| No unsupported causal inference | PASS |
| Every substantive claim traceable to retrieved source | PASS, 16/16 claims |
| Retrieval miss never becomes corpus absence | PASS |

These gates do not require complete recovery of the prior 17-need manual plan. Answer omissions and weak retrieval are reported below as product-quality defects.

## Product pipeline

```text
User question
  -> unchanged question searched independently within STANDARDS
  -> unchanged question searched independently within PROFESSIONAL_TEAM_REPORT
  -> unchanged question searched independently within VENDOR_SUBMISSION
  -> top three hybrid-ranked passages per role
  -> role-partitioned context
  -> Qwen2.5-32B-Instruct-AWQ synthesis
  -> host-resolved assertion, page, exact span, and PDF citation
```

The retrieval layer reused the existing 6,009 deterministic passages, contextual MiniLM embeddings, BM25 index, and reciprocal-rank fusion. It selected exactly 72 passages: nine per question. No automatic planner or query rewriting ran.

## Execution identity

- Successful run: DCC job `55224188`
- Model: `Qwen/Qwen2.5-32B-Instruct-AWQ`
- Model revision: `5c7cb76a268fc6cfbb9c4777eb24ba6e27f9ee6c`
- vLLM: `0.29.0`
- Temperature and seed: `0`, `0`
- Valid structured outputs: 8/8
- Model claims checked: 16
- Contract SHA-256: `95d0866efe07a19c83cf81c7508991ac7948ef767481ad71cb343f8e77048877`
- Result SHA-256: `3e8f2b65f41d4fd928ab272d7885764e5e774adb4f2d438bfb9bab514529ca6f`
- Evaluator reads by generator: 0

The request ledger, raw responses, journal, result file, retrieval bundles, and source bindings are persisted. Manifest hashes for results, journal, and requests were independently verified after transfer from DCC.

## Safety result

Q7 reports only that the retrieved evidence does not establish that the Professional Team required RMS to change its coastal-frequency methodology. Q8 reports only that the retrieved evidence does not establish a direct review-to-modification link. Neither answer claims that the fixed corpus proves nonoccurrence, and neither upgrades scrutiny or a model update into review causation.

The project-level causal adjudication remains `UNRESOLVED`. RAG v0 does not replace the separate fixed-corpus manual audit.

## Product-quality defects

The run is safe and traceable, but retrieval quality is uneven.

- Q1 answers the controlling requirement but retrieves it from the Professional Team report and omits the separate `reasonably reflect` qualification.
- Q2 recovers 69-segment smoothing and target adjustment but misses the Poisson calibration passage.
- Q4 identifies the July 2019 HURDAT2 update but omits the specific landfall and bypass-rate revision.
- Q5 misses the actual Version 21.0 versus Version 18.1 comparison and therefore gives a safe but unhelpful bundle-scoped answer.
- Q6 gives a partial chronology but misses the dated vendor update.
- Q7 remains safe, but the selected S-2 no-change assertion is irrelevant to coastal-frequency methodology.
- Q8 keeps causation unresolved but omits the positive coastal requirement, scrutiny, methodology, and update chain that would make the answer useful to a researcher.

These are visible retrieval and answer-quality issues. Under the user-defined MVP contract, they do not override the three passed safety and traceability gates.

## Attempt history

The first connected run, DCC job `55224116`, produced eight valid outputs but failed all three MVP gates on Q7. It used an S-2 no-change statement to claim that the Professional Team did not require a coastal-frequency methodology change. That run and its human adjudication remain preserved.

RAG v0.2 changed only the generic negative-claim safety instruction: a negative claim requires direct evidence with the same actor, action, target, and scope; otherwise the answer must remain explicitly scoped to retrieved evidence. Retrieval bundles, questions, model, source bindings, decoding, and MVP gates did not change.

## Scope of the result

This is a development MVP demonstration over eight known questions and three fixed document roles. It establishes that the connected product can return source-traceable answers while preserving the central causal and absence boundaries. It does not establish held-out performance, complete evidence recall, or readiness for a larger multi-vendor corpus.

