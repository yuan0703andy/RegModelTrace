# Panel C tier-1 match clarification

Status: frozen before regenerating the Panel C candidate set. This interprets
the existing `case_formation_protocol.json`; it does not change discovery,
anchors, source-only keys, semantic labels, or the match limit.

## Decision

For Panel C, a tier-1 *match* is a counterpart natural unit that physically
prints the same exact typed hierarchical identifier as a source key. A section
heading may locate and contextualize a candidate unit, but it does not turn
every child paragraph of that section into a tier-1 hit. This follows the
frozen distinction between Panel A's explicit whole-section expansion and
Panel C's requirement that the identifier appear in both units.

The candidate search first records every counterpart paragraph that itself
prints `Form X-n`, `Standard X-n`, or a syntactically identified numbered
review-comment target `X-n[.subsection]`. The search preserves physical page,
raw offset, exact printed identifier span, typed normalized key, and every
candidate. A separate source-boundary review then expands each candidate to
its complete panel-specific natural unit. The section heading may travel as
parent context; a heading alone is not a substantive counterpart. A copied
requirement remains a candidate until source-role review rejects it, never a
vendor-implementation or reviewer-action finding by itself.

At tier 1, no implicit identifier is inferred from being inside a section. If
no typed-ID-bearing unit exists, continue through the frozen lower tiers. A
failure to recover the natural unit from a matched paragraph is recorded as
`COUNTERPART_UNIT_BOUNDARY_UNRESOLVED`, not repaired by selecting a favorable
sentence. Apply the existing >20-paragraph or >3000-word match limit only after
all first-nonempty-tier natural units are reconstructed and deduplicated; no
manual pruning is allowed. Retain the old whole-section Panel C output as
`NONCONFORMING_BROAD_SECTION_DIAGNOSTIC` with its 16 preliminary over-limit
flags. Do not treat those flags as final overflow outcomes.

The strongest cost of this reading is that relevant work documented only under
an ID heading may be missed at tier 1. That is an intended bounded-search
limitation of this narrow Panel C rule, not evidence of corpus absence. The
lower-tier exact object/name search remains available where source-only keys
were frozen. Panel A continues its distinct whole-section rule unchanged.

No natural gold or model output has been consulted. The prior 18 chronology
deviations and the separate premature Form A-5 diagnostic remain permanently
secondary. A mechanically repaired chronology-clean plan may retain its
pre-gold status, but cannot become primary eligible until exposure,
counterpart-unit, same-object, and dependency checks are complete.
