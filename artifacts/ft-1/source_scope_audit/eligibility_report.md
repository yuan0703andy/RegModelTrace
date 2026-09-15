# FT-1 source-scope eligibility audit

Status: COMPLETE. Scope: metadata, provenance, input lineage, and retained regulator locks only. No alignment labels or model predictions were consulted in this audit; no inference occurred.

**Current bundles: EXCLUDE 19/19. Fresh independent pilot ready: 0.**

Every current bundle exactly matches evidence membership selected in a post-adjudication fixture. Hiding labels does not establish outcome-independent selection. The facet definitions also originate in adjudicated comparison records. Existing packs and blank returns are retired for independent adjudication and retained as audit history.

**Source seeds: KEEP 9; UNRESOLVED 10.** KEEP means original PDF hashes and a regulator dimension lock predating paired adjudication are retained. It does not approve the existing evidence memberships or facet boundaries.

| Case | Current bundle | Source seed | Source dependency |
|---|---|---|---|
| FC-IF23-CI5B-COMPONENT-TESTING | EXCLUDE | KEEP | Raw hashes and pre-adjudication regulator lock verified; fresh evidence scope required |
| FC-TE23-V2 | EXCLUDE | UNRESOLVED | Original pre-adjudication regulator dimension lock not located; One or more exact raw PDFs not located in checked archive paths |
| FC-M3B-ARA | EXCLUDE | UNRESOLVED | Original pre-adjudication regulator dimension lock not located |
| FC-VD23-V2 | EXCLUDE | KEEP | Raw hashes and pre-adjudication regulator lock verified; fresh evidence scope required |
| FC-IF23-M3B-HISTORICAL-LANDFALL-OUTPUT | EXCLUDE | KEEP | Raw hashes and pre-adjudication regulator lock verified; fresh evidence scope required |
| FC-TE23-S2 | EXCLUDE | UNRESOLVED | Original pre-adjudication regulator dimension lock not located; One or more exact raw PDFs not located in checked archive paths |
| FC-CI5B-ARA | EXCLUDE | UNRESOLVED | Original pre-adjudication regulator dimension lock not located |
| FC-VD23-CI6 | EXCLUDE | KEEP | Raw hashes and pre-adjudication regulator lock verified; fresh evidence scope required |
| FC-IF23-S3-UNCERTAINTY-ANALYSIS | EXCLUDE | KEEP | Raw hashes and pre-adjudication regulator lock verified; fresh evidence scope required |
| FC-TE23-G2 | EXCLUDE | UNRESOLVED | Original pre-adjudication regulator dimension lock not located; One or more exact raw PDFs not located in checked archive paths |
| FC-V1A-ARA | EXCLUDE | UNRESOLVED | Original pre-adjudication regulator dimension lock not located |
| FC-VD23-S2 | EXCLUDE | KEEP | Raw hashes and pre-adjudication regulator lock verified; fresh evidence scope required |
| FC-IF23-G4-COMPONENT-INDEPENDENCE | EXCLUDE | KEEP | Raw hashes and pre-adjudication regulator lock verified; fresh evidence scope required |
| FC-TE23-CI6 | EXCLUDE | UNRESOLVED | Original pre-adjudication regulator dimension lock not located; One or more exact raw PDFs not located in checked archive paths |
| FC-CI5B-RMS | EXCLUDE | UNRESOLVED | Original pre-adjudication regulator dimension lock not located; One or more exact raw PDFs not located in checked archive paths |
| FC-VD23-M3 | EXCLUDE | KEEP | Raw hashes and pre-adjudication regulator lock verified; fresh evidence scope required |
| FC-TE23-A2 | EXCLUDE | UNRESOLVED | Original pre-adjudication regulator dimension lock not located; One or more exact raw PDFs not located in checked archive paths |
| FC-M3B-RMS | EXCLUDE | UNRESOLVED | Original pre-adjudication regulator dimension lock not located; One or more exact raw PDFs not located in checked archive paths |
| FC-VD23-A2 | EXCLUDE | KEEP | Raw hashes and pre-adjudication regulator lock verified; fresh evidence scope required |

## Next gate

Build fresh source-only evidence scopes for the nine Impact/Verisk seeds using the retained regulator locks and original documents, without consulting fixture memberships, historical facet decisions, or predictions. Add independently selected cases to reach 20–30, then obtain two independent human adjudications, resolve disagreement, and prospectively freeze truth. CoreLogic remains SKIPPED; it must not be reconstructed from its adjudicated fixture.

A/B/C comparisons must use identical prospectively frozen evidence. Saved A outputs on different evidence bundles are historical references, not a controlled representation comparison. A matched A reference requires a separately authorized prospective protocol; no closed KCC rerun is authorized.

Unlocated files refer only to checked archive paths, not proof of corpus-wide absence. Historical outcomes are exposed development information; fresh adjudicators must not have seen them.

Exact source hashes, regulator block IDs, and lineage are in eligibility_report.json; original regulator-only lock/selection files are retained under pretruth/.
