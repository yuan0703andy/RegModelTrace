# Proposal: Finalize the RegModelTrace GitHub release

## Problem

The working directory contains the completed system and reports together with unrelated document-editing artifacts, large raw/derived corpora, superseded experiment scripts, cluster logs, and many completed change specs. The repository has no commit or remote, so it cannot yet serve as a reviewable project release.

## Change

Create a compact public release package that preserves the executable application contract, source code for the parser/retrieval/generation/Ray architecture, static evidence demo, final metrics and limitations, selected immutable receipts, and current durable specifications. Remove local-only data, redundant experiment history, and unrelated project files. Verify the package, scan it for secrets and oversized files, then create and push the first GitHub commit.

## Scientific boundary

Cleanup must not improve, regrade, or hide final results. The public package must retain the `PARTIALLY_ALIGNED` failure, absent `CONFLICT` support, KCC table-portability failure, forced-choice probability limitation, exposed-test status, and Ray generative-nondeterminism limitation.

