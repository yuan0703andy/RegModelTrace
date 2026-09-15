# Proposal: Diagnose facet representation before fine-tuning

## Problem

The closed RegModelTrace release repeatedly classified some multi-facet `PARTIALLY_ALIGNED` cases as `ALIGNED`. The observed error may arise because whole-bundle classification hides missing facets, because the model aggregates correct facet judgments poorly, or because Base Qwen misjudges the facets themselves. Training before separating these causes would confound task design with weight adaptation.

## Change

Open a separate FT-1 research module that preserves the closed release, defines a four-state facet ontology, prepares leakage-aware historical development metadata and a blinded human-adjudication pilot, freezes deterministic aggregation, and implements Conditions A/B/C. Condition A reuses saved historical predictions. Conditions B and C may run only after prospective facet truth and the human-agreement pilot are complete.

## Assumptions and falsification

The main hypothesis is that explicit facet decomposition and host aggregation explain most false-`ALIGNED` errors. It is falsified if Base Qwen continues to misclassify atomic facets after evidence, ontology, and aggregation are held fixed. A second independent human adjudicator is required because agreement cannot be established by code or by another model.

## Historical boundary

The closed release, Test E results, v2.2 scores, retrieval, Ray implementation, Base Qwen weights, citations, and provenance remain immutable. This change does not authorize LoRA, QLoRA, a KCC rerun, production deployment, or a new sealed-test claim.
