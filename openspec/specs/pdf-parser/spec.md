# PDF parser

## Purpose

Define the Milestone 2 preservation and structure contract against the frozen twelve-record core. Measured results live in the implementation acceptance report; semantic interpretation belongs to Milestone 3.

## Requirements

### Requirement: Parser inputs exclude gold annotations
The parser SHALL read only raw PDFs, registered metadata, and versioned generic parsing configuration. Gold IDs, source spans, question labels, and conclusions SHALL NOT be parser inputs. Only an independent scorer MAY load the frozen Gold Core after parser output is persisted.

#### Scenario: Gold hidden during parsing
- **WHEN** gold files are unavailable to the parsing process
- **THEN** the parser produces identical blocks from the same PDFs and configuration.

### Requirement: Recoverable source structure
Blocks SHALL preserve document identity, physical pages, source text positions and geometry, reading order, section/standard/disclosure/form context, content type, and header/footer status. Continuation links SHALL make cross-page units reconstructable without crossing unrelated sections.

#### Scenario: Continued frequency methodology
- **WHEN** a source paragraph continues across a page boundary
- **THEN** its connected unit retains both source-page references and excludes the intervening header/footer from searchable body text.

### Requirement: Core-only evaluation with separate structural checks
Core Span Recoverability SHALL count twelve unique frozen core records. A record SHALL pass only if every constituent span is recoverable. Audit-context records SHALL be reported separately. One or more blocks MAY reconstruct a frozen span; identical annotation boundaries SHALL NOT be required. Text coverage SHALL NOT imply required structural identity, correct table columns, retrieval success, evidence-type precision, or causal correctness.

#### Scenario: Text survives but table associations fail
- **WHEN** table values are present but historical and modeled columns are swapped
- **THEN** table-structure acceptance fails despite perfect text coverage.

### Requirement: Nine independent hard gates
Milestone 2 SHALL pass only when source-span recoverability, provenance, hierarchy, continuation, header/footer separation, table integrity, gold isolation, determinism, and failure transparency all pass. There SHALL be no weighted aggregate. Semantics SHALL remain outside this milestone.

#### Scenario: All text survives but columns swap
- **WHEN** all source spans remain recoverable but historical and modeled columns are exchanged
- **THEN** G6 and overall Milestone 2 fail regardless of the other gates.

### Requirement: Operational hierarchy and whole-table integrity
Required ancestor/child relationships SHALL be machine-checkable. Every target-table numeric cell SHALL have unique row/column identity, complete hierarchical paths, a value, a source bbox, and source-token provenance. Whole-table generic checks SHALL accompany the frozen critical-cell checks.

#### Scenario: Noncritical cell is corrupted
- **WHEN** a target-table cell outside the four critical examples is dropped, duplicated, misassigned, or moved
- **THEN** generic table integrity fails rather than accepting the four examples alone.

### Requirement: Stop after acceptance
Parser implementation SHALL stop once all nine hard gates pass. Further changes SHALL require a demonstrated downstream need rather than cosmetic chunk improvements.

#### Scenario: Nonrequired layout could look cleaner
- **WHEN** all nine gates pass and an unrelated layout remains explicitly diagnosed
- **THEN** report the limitation without continuing parser polishing.
