# Qualify public RAG benchmarks as an independent research track

## Problem

FG-3 tests semantic judgment on bounded Florida source evidence; it is not a quantitative retrieval benchmark. A separate public-benchmark track can test retrieval and generation failures without waiting for FG-3 human gold. The proposed benchmarks, however, have different tasks, languages, annotations, and evaluation machinery. Treating their scores as commensurate would confound the research question.

## Change

Establish Track A as independent of frozen FG-3 Track B. First qualify official benchmark artifacts, their evaluation contracts, and feasible method comparisons. Record what can and cannot be evaluated before building baselines or running a model.

## Assumptions and falsification

The official data and implementation can be pinned and inspected. If a benchmark lacks an eligible development/test separation, evidence labels, reproducible scoring, or locally executable reference method, the affected comparison is limited or excluded rather than silently replaced by a different task. A simple metadata-aware baseline may account for apparent gains; no new method is presumed.

## Scope

This change covers A0 qualification and the prospective A1 plan only. It does not change FG-3 source selection, gold, prompts, or results; it does not run Qwen, retrieval baselines, or published methods.
