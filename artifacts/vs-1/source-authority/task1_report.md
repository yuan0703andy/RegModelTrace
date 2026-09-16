# VS-1 Task 1 — Source Authority Verification

**Status:** `PASS`
**Corpus snapshot:** `CS_815122cca84bcfd9c1637df6`
**Index build:** `IB_e922be7973b49bb13e2b340a`

## Verified

- all three frozen source PDFs exist and match their declared SHA-256 values;
- corpus identity is derived only from source/canonical identities;
- the retrieval representation has a separate `IndexBuildManifest`;
- all bound FTS, record-store, passage, embedding, ID, and canonical-page artifacts exist and match recorded hashes;
- M-3.B resolves from passage to assertion, source spans, canonical physical page 120, and the verified original Standards PDF;
- one passage from each of `STANDARDS`, `PROFESSIONAL_TEAM_REPORT`, and `VENDOR_SUBMISSION` completes the same real-source round trip;
- a returned `source_span_id` resolves independently;
- an unknown ID fails closed without fuzzy substitution;
- a real alignment-failure passage remains `RESOLVED` at `PAGE_TEXT` precision with `SOURCE_GEOMETRY_UNAVAILABLE`.

## Boundaries

```text
new model inference runs = 0
retrieval rebuilt = false
retrieval tuned = false
source PDFs copied = false
Qwen / Ray / UI changes = none
```

Task 1 establishes source authority and real-corpus binding only. It does not
create the retrieval candidate packet, product workbench, review persistence,
or Qwen reconnection.
