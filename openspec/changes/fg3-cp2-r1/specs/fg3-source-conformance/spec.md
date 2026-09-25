## ADDED Requirements

### Requirement: Canonical source-unit custody
Every nonterminal FG-3 lead SHALL have a panel-specific source unit with exact original-PDF spans, a verified fixed anchor, a printed parent heading with source ref, and start/end boundary evidence before a pairing key is derived.

#### Scenario: Fixed anchor appears more than once on a page
- **WHEN** a phrase appears in multiple subsections
- **THEN** the system SHALL use the frozen normalized offset and SHALL reject a source unit that contains only another occurrence.

### Requirement: Typed source-derived pairing keys
Every counterpart search key SHALL identify its source span and type. Form and Standard identifiers SHALL remain separate, and only the frozen Unicode dash glyph mapping MAY canonicalize printed identifiers.

#### Scenario: Form and Standard share an identifier
- **WHEN** both `Form A-5` and `Standard A-5` appear in a counterpart document
- **THEN** a `FORM:A-5` key SHALL match the Form section and SHALL NOT match the Standard section.

### Requirement: Frozen-tier counterpart search
Panel A SHALL retrieve complete substantive paragraphs within the matching vendor section. Panel C SHALL retain every matching counterpart paragraph at its first nonempty frozen tier. A tier SHALL NOT be declared unavailable until source-derived keys for that tier have been materialized or explicitly ruled out.

#### Scenario: A table of contents and a section heading share an identifier
- **WHEN** the identifier occurs in a TOC and in the substantive vendor section
- **THEN** the TOC SHALL be recorded as a rejected search hit and the complete bounded section SHALL be retained according to the frozen rule.

### Requirement: Exact exposure candidate fidelity
The exact-overlap scanner SHALL verify the frozen file hashes, decode JSON string values, normalize Unicode and whitespace, and inspect every 12-token source window at stride one. It SHALL NOT infer exposure clearance from an unmatched exact window.

#### Scenario: Escaped JSON text and Unicode punctuation
- **WHEN** a known-exposure JSON file serializes a phrase using escaped Unicode characters
- **THEN** the scanner SHALL compare the decoded logical string and report any matching exposure candidate.

### Requirement: Prospective boundary preservation
The repair SHALL preserve the 85 leads and first anchors, keep the 18 prior chronology-deviated plans outside the primary set, and perform no natural model inference or human-truth scoring.

#### Scenario: A repaired pairing now finds a substantive counterpart
- **WHEN** that pairing belongs to a previously chronology-deviated plan
- **THEN** its status SHALL remain secondary/exploratory and SHALL NOT become primary eligible.
