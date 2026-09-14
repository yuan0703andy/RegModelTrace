# product-ui Specification

## Purpose
Define an honest evidence-first interface for the preserved development demonstration.
## Requirements
### Requirement: development-demo honesty

The product UI SHALL identify the displayed results as a development demonstration over eight frozen questions and SHALL NOT represent them as held-out evaluation or live arbitrary-question inference.

#### Scenario: viewer opens the workbench

- **WHEN** the product UI loads
- **THEN** it displays a development-demo label and the eight-question scope
- **AND** it provides a plain-language scope explanation

### Requirement: evidence-first answer display

For each question, the UI SHALL display the preserved answer, evidence status, and host-resolved source evidence. Evidence SHALL retain document role, physical page, exact source text, and original PDF navigation.

#### Scenario: viewer selects a frozen question

- **WHEN** the viewer selects any of the eight questions
- **THEN** the preserved answer and status are displayed
- **AND** every cited evidence item shows its role, page, exact source text, and PDF link

### Requirement: bundle-scoped uncertainty

The UI SHALL explain that `UNRESOLVED_FROM_RETRIEVED_EVIDENCE` denotes an evidentiary gap in the retrieved bundle and does not prove absence from the fixed corpus or nonoccurrence.

#### Scenario: unresolved answer is displayed

- **WHEN** a selected answer has status `UNRESOLVED_FROM_RETRIEVED_EVIDENCE`
- **THEN** the UI describes the gap as limited to the retrieved bundle
- **AND** it does not claim corpus absence or nonoccurrence

### Requirement: usable evidence inspection

The UI SHALL allow a viewer to move from an answer citation to its evidence card and from that card to the cited PDF page.

#### Scenario: viewer follows a citation

- **WHEN** the viewer activates an answer citation
- **THEN** the corresponding evidence card opens and receives focus
- **AND** the card provides a link to the preserved PDF page
