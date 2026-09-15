# FT-1 Provisional Adjudication Candidate Pack

Labels and model outputs are omitted, but these historical-fixture candidates still require independent source-scope verification before blinded adjudication. CoreLogic is excluded. This pack is not certified source-only.

## 1. FC-IF23-CI5B-COMPONENT-TESTING

- Corpus: `impact-forecasting-2023`
- Requirement: `IF23-CI5B-COMPONENT-TESTING`
- Vendor group: `impact_forecasting`

### Candidate regulatory facets

- `IF23-CI5B-COMPONENT-TESTING.F1`: Testing software assists in documenting and analyzing all components.
- `IF23-CI5B-COMPONENT-TESTING.F2`: Unit tests are performed and documented for each updated component.
- `IF23-CI5B-COMPONENT-TESTING.F3`: Regression tests are performed and documented on incremental builds.
- `IF23-CI5B-COMPONENT-TESTING.F4`: Integration tests are performed and documented for all components, with sufficient testing to execute every component at least once.

### Bounded source propositions

**P4a465ec86cea6a91c93c — REGULATOR — fchlpm_2023_hurricane_standards, p. 275**

> 1. Testing software shall be used to assist in documenting and analyzing all components.

**Pe5d256c00124c6477f64 — REGULATOR — fchlpm_2023_hurricane_standards, p. 275**

> 2. Unit tests shall be performed and documented for each updated component.

**P2621ad424217bb82b0d4 — REGULATOR — fchlpm_2023_hurricane_standards, p. 275**

> 3. Regression tests shall be performed and documented on incremental builds.

**P4ef9219a9c0754a33721 — REGULATOR — fchlpm_2023_hurricane_standards, p. 275**

> 4. Integration tests shall be performed and documented to ensure the correctness of all hurricane model components.

**Pbcf96ef0878425befc0a — REGULATOR — fchlpm_2023_hurricane_standards, p. 275**

> Sufficient testing shall be performed to ensure that all components have been executed at least once.

**P17db5a5702a27373ce52 — VENDOR — impact_forecasting_2023_submission_20250528, p. 257**

> All unit test cases are documented and stored in Azure DevOps repository.

**Pb6a1a8841c33d122fb39 — VENDOR — impact_forecasting_2023_submission_20250528, p. 257**

> The Impact Forecasting Software team uses Azure DevOps Unit testing framework to perform unit tests on all components when applicable.

**Pd84e4194a3fe793c7726 — VENDOR — impact_forecasting_2023_submission_20250528, p. 258**

> Sets of regression tests are documented and performed with each iteration of internal and production releases.

**P5345c5ceba0809ccac21 — VENDOR — impact_forecasting_2023_submission_20250528, p. 258**

> End-to-end tests involving all hurricane model components are performed regularly by the QA team with each internal and production release.

**P92a069abe4ae70073b34 — VENDOR — impact_forecasting_2023_submission_20250528, p. 258**

> Multiple test cases are created to make sure all possible interactions among sub-components and components are covered.

**Pce54cb80114085c0c4be — VENDOR — impact_forecasting_2023_submission_20250528, p. 258**

> The Unified Function Test (UFT) suite by MicroFocus is used to automate test cases in addition to manual testing to verify communications between various components.

**P3ccd401000a7cc3c1fd2 — REVIEWER — impact_forecasting_2023_professional_team_20250425, p. 81**

> Discussed that manual testing was conducted for the roof and wall pressure coefficients code.

**Pf820fa34c4ff40f40763 — REVIEWER — impact_forecasting_2023_professional_team_20250425, p. 81**

> Discussed that Microsoft unit test framework is used for unit testing.

**Pd9e7eb40cfb929b5db91 — REVIEWER — impact_forecasting_2023_professional_team_20250425, p. 81**

> Reviewed a written R&D verification improvement plan including a process timeline concerning verification procedures, component testing, and data testing.

**P562ca1de9607d75e7b06 — REVIEWER — impact_forecasting_2023_professional_team_20250425, p. 81**

> Discussed the need to improve verification testing and the use of verification tools.

## 2. FC-TE23-V2

- Corpus: `kcc-2023-exposed-test-e`
- Requirement: `V-2`
- Vendor group: `kcc`

### Candidate regulatory facets

- `V-2.A`: Contents vulnerability-function development is based on a combination of insurance claims data and rational engineering analysis supported by permitted empirical investigation.
- `V-2.B`: The building-to-contents vulnerability relationship is consistent with and supported by claims data.

### Bounded source propositions

**P55e88d3d0807c0a349e1 — REGULATOR — shared_standards_2023_standards, p. 196**

> A. Development of the contents hurricane vulnerability functions shall be based on a combination of available insurance company hurricane claims data and rational engineering analysis supported by laboratory testing, field testing, or post-event site investigations. B. The relationship between the hurricane model building and contents hurricane vulnerability functions shall be consistent with, and supported by, the relationship observed in insurance company hurricane claims data.

**P5d0ed95d793108987487 — VENDOR — karen_clark_company_2023_kcc_submission, p. 116**

> The contents vulnerability functions were developed based on engineering judgement informed by rational structural analysis and post-event damage surveys.

**P0ffcbeabe3b4f6373b41 — VENDOR — karen_clark_company_2023_kcc_submission, p. 116**

> Vulnerability functions were then validated using insurance claims data.

**Paac6c6f23e799f1bfd52 — VENDOR — karen_clark_company_2023_kcc_submission, p. 116**

> The relationship between modeled building vulnerability functions and modeled contents vulnerability functions is reasonable and has been validated with insurance claims data.

**P8e262233263e733eb2ff — VENDOR — karen_clark_company_2023_kcc_submission, p. 118**

> Insurance claims data were then used to validate the relationship between building and contents damage.

**Pb1b8bab7cbb3001ed5ca — VENDOR — karen_clark_company_2023_kcc_submission, p. 118**

> This relationship is confirmed by analyses of insurance claims data.

**Pc31fef2a38cfda6538b0 — VENDOR — karen_clark_company_2023_kcc_submission, p. 116**

> The modeled MDRs are in good agreement with MDRs developed from claims data.

**P6d76a61144a5c086d78b — REVIEWER — karen_clark_company_2023_kcc_review, p. 49**

> Reviewed the building to contents damage relationship with claims data.

**P38e9882e3a2164848049 — REVIEWER — karen_clark_company_2023_kcc_review, p. 49**

> Discussed that the contents to building damage ratio relationship is based on engineering judgement informed by post-event damage assessment and rational structural analysis.

**Pa41ce5d148d1b18541f0 — REVIEWER — karen_clark_company_2023_kcc_review, p. 49**

> Reviewed examples of damage survey photos with minor, moderate, and severe building damage illustrating the building-to-contents damage ratio relationship.

**Pfb8fbeb4965f8a3d58f4 — REVIEWER — karen_clark_company_2023_kcc_review, p. 49**

> Reviewed the relationship between contents and building damage ratio by occupancy type and by construction type.

**P4d4d0ee0d3a5eb3ce9d3 — REVIEWER — karen_clark_company_2023_kcc_review, p. 50**

> Discussed that claims data are used to validate the contents vulnerability functions.

**Pab9516b81f0eed4e611c — REVIEWER — karen_clark_company_2023_kcc_review, p. 50**

> Reviewed flowchart for contents vulnerability function development and implementation.

**P6366007b68f1f188c529 — REVIEWER — karen_clark_company_2023_kcc_review, p. 48**

> Verified: YES

**Pf6b3b55be7f3712ee413 — VENDOR — karen_clark_company_2023_kcc_submission, p. 118**

> The impact of water infiltration is not explicitly modeled; however, since insurance claims data from historical events are used to validate the contents vulnerability functions, the impact of water infiltration, which is included in the insured claims data sets, is implicitly accounted for by the contents vulnerability functions.

## 3. FC-M3B-ARA

- Corpus: `rms-ara-2019-development`
- Requirement: `M-3.B:historical-coastal-consistency`
- Vendor group: `ara`

### Candidate regulatory facets

- `M-3.B:historical-coastal-consistency.F1`: Modeled landfall-frequency distributions reflect the Base Hurricane Storm Set and are consistent with observed frequencies.

### Bounded source propositions

**SRC-211f3cc2d0ec2e15b1e3 — REGULATOR — fchlpm_2019_hurricane_standards, p. 120**

> B. Modeled hurricane landfall frequency distributions shall reflect the Base Hurricane Storm Set used for category 1 to 5 hurricanes and shall be consistent with those observed for each coastal segment of Florida and neighboring states (Alabama, Georgia, and Mississippi).

**SRC-dfe5bce4ee2049464d59 — VENDOR — ara_hurloss_10_0_2019_submission_20210310, p. 57**

> B. The modeled hurricane probabilities reasonably reflect the Official Storm Set for each coastal segment of Florida and neighboring states as demonstrated in Form M-1.

**SRC-f2204311a1eb51c1990d — VENDOR — ara_hurloss_10_0_2019_submission_20210310, p. 169**

> Figure 40 presents a comparison of the distribution of the historical and modeled basin-wide occurrence rate and the p-values for various statistical tests. Figure 41 presents coastal segments used to compare modeled and historical hurricane parameters. Figure 42 through Figure 45 presents comparisons of modeled and historical translation speeds, headings, occurrence rates, and central pressures along the coastal segments given in Figure 41. P-values associated with various statistical tests for equivalence are presented in the figures.

**SRC-c3fdc8f7d86ccf7ab0c7 — REVIEWER — ara_hurloss_10_0_2019_professional_team_20210311, p. 17**

> Reviewed comparison of historical to modeled annual landfall occurrence rates by coastal segment for Category 1-2 hurricanes and for Category 3-5 hurricanes by central pressure and by windspeed.

**SRC-92c8b12192f518b42bad — REGULATOR_COPY — ara_hurloss_10_0_2019_submission_20210310, p. 54**

> Provide plots of the annual landfall occurrence rates obtained directly from the Base Hurricane Storm Set for two intensity bands (Saffir-Simpson categories 1-2 and 3-5) as functions of coastal segments along Florida and adjacent states. Plot on the same axes the modeled annual landfall occurrence rates over the Base Hurricane Storm Set period. If the modeling organization has a previously-accepted hurricane model, also plot on these axes the previously-accepted hurricane model annual landfall occurrence rates.

**SRC-6b46567a2d385e36995c — VENDOR — ara_hurloss_10_0_2019_submission_20210310, p. 54**

> The model does not use coastline segments or partitions for determining parameters.

## 4. FC-VD23-V2

- Corpus: `verisk-2023-validation-d`
- Requirement: `V-2`
- Vendor group: `verisk`

### Candidate regulatory facets

- `V-2.A.1`: Contents vulnerability functions use available insurance-company hurricane claims data.
- `V-2.A.2`: Contents vulnerability functions use rational engineering analysis.
- `V-2.A.3`: The engineering analysis is supported by laboratory tests, field tests, or post-event site investigations.
- `V-2.B.1`: The building-to-contents relationship is consistent with the relationship observed in claims data.
- `V-2.B.2`: Claims data support the building-to-contents relationship.

### Bounded source propositions

**P55e88d3d0807c0a349e1 — REGULATOR — shared_standards_2023_standards, p. 196**

> A. Development of the contents hurricane vulnerability functions shall be based on a combination of available insurance company hurricane claims data and rational engineering analysis supported by laboratory testing, field testing, or post-event site investigations. B. The relationship between the hurricane model building and contents hurricane vulnerability functions shall be consistent with, and supported by, the relationship observed in insurance company hurricane claims data.

**Pf12a8c100365734bb3bf — VENDOR — verisk_2023_verisk_submission, p. 144**

> The Verisk Hurricane Model for the United States vulnerability functions for contents are primarily based on engineering and insurance-related research publications, damage surveys conducted by wind engineering and damage experts in the aftermath of historical hurricanes, and analyses of available insurance company claims and loss data.

**P831fadfc3b3f0feb3a07 — VENDOR — verisk_2023_verisk_submission, p. 144**

> Over time, the damage functions have been fine-tuned based on the results of post-disaster field surveys from major events in the U.S. and abroad, recently published research studies, computational simulations and analyses, and on detailed analyses of loss data from clients.

**Pc8d844db144677746229 — VENDOR — verisk_2023_verisk_submission, p. 145, 146**

> In the Verisk model, the secondary distributions for contents are based on insurance company claims data from several major companies across multiple events.

**P9c73268f191f8f982e83 — VENDOR — verisk_2023_verisk_submission, p. 146**

> These relationships are developed using claims data, published engineering studies, and expert engineering judgment.

**P1442ffbeb00b1a4a0183 — VENDOR — verisk_2023_verisk_submission, p. 144**

> The relationship among the modeled building damage ratios and modeled contents damage ratios is reasonable based on comparisons to actual loss data from client companies.

**P10be4ce14fbc85f6acff — VENDOR — verisk_2023_verisk_submission, p. 144**

> This process is used for contents loss validation and underscores the fact that our fundamental formulation of contents vulnerability as a function of building vulnerability is consistent with the signature observed in historical data.

**Pfe39bc0263030bda315c — VENDOR — verisk_2023_verisk_submission, p. 145**

> In the Verisk Hurricane Model for the United States, the contents vulnerability is a function of the building vulnerability, such that the resulting contents mean damage ratio is a function of the building mean damage ratio.

**P08ec171dd9f1fe52149f — VENDOR — verisk_2023_verisk_submission, p. 146**

> Since the model's vulnerability functions are calibrated and validated using insurance company claims data and water infiltration is the primary source of contents damage, the impact of the same is accounted for implicitly.

**Pe592a1825db311e0142a — REVIEWER — verisk_2023_verisk_review, p. 50**

> Discussed that vulnerability functions are predominantly derived from published research, engineering expertise, and damage surveys that are calibrated based on actual claims experience.

**Pb7008f7f290379c769af — REVIEWER — verisk_2023_verisk_review, p. 51**

> Discussed that contents vulnerability functions are derived based on the relationship to the primary building damage, and the relationship is calibrated based on claims data.

**P1d108a59bf6b1476cf29 — REVIEWER — verisk_2023_verisk_review, p. 51**

> Reviewed a scatter plot of modeled to actual contents MDRs.

**P2e9124033495b87996fa — REVIEWER — verisk_2023_verisk_review, p. 51**

> Reviewed scatter plots of actual and modeled contents damage ratios versus windspeed for masonry construction and for single family homes.

**P6eeae5eca08d4e695550 — REVIEWER — verisk_2023_verisk_review, p. 52**

> Reviewed the process for contents vulnerability function development and calibration based on claims data.

**P5c6a4834fcec3765eea0 — REVIEWER — verisk_2023_verisk_review, p. 52**

> Discussed that the relationship between exterior damage and contents damage is an empirically derived function that is calibrated based on claims data, and is a rational approach given uncertainties in interior damage and insurance payout practices.

**P8e25e49b84904272ea8f — REVIEWER — verisk_2023_verisk_review, p. 52**

> Reviewed the flowchart for derivation and implementation of the contents vulnerability functions.

**P045eb83f6b52f16865d6 — VENDOR — verisk_2023_verisk_submission, p. 144**

> The subsequent claims data corresponding to the exposure may or may not include loss information which contains the application of policy terms.

**Pcf9425de60816b4dbb45 — REVIEWER — verisk_2023_verisk_review, p. 50**

> Discussed that claims typically lack a detailed breakdown of the cause of loss other than identifying wind versus flood.

## 5. FC-IF23-M3B-HISTORICAL-LANDFALL-OUTPUT

- Corpus: `impact-forecasting-2023`
- Requirement: `IF23-M3B-HISTORICAL-LANDFALL-OUTPUT`
- Vendor group: `impact_forecasting`

### Candidate regulatory facets

- `IF23-M3B-HISTORICAL-LANDFALL-OUTPUT.F1`: Modeled hurricane landfall-frequency distributions reflect the Model Base Hurricane Set for category 1 to 5 hurricanes.
- `IF23-M3B-HISTORICAL-LANDFALL-OUTPUT.F2`: Modeled distributions are consistent with observations for each coastal segment of Florida and neighboring states.
- `IF23-M3B-HISTORICAL-LANDFALL-OUTPUT.F3`: Any differences are justifiable.

### Bounded source propositions

**Pd780f377332511518aa2 — REGULATOR — fchlpm_2023_hurricane_standards, p. 144**

> B. Modeled hurricane landfall frequency distributions shall reflect the Model Base Hurricane Set used for category 1 to 5 hurricanes and shall be consistent with those observed for each coastal segment of Florida and neighboring states (Alabama, Georgia, and Mississippi).

**P137eb9295287dd9fd158 — REGULATOR — fchlpm_2023_hurricane_standards, p. 144**

> Any differences shall be justifiable.

**Pbb3bb0823ee4f04f7276 — VENDOR — impact_forecasting_2023_submission_20250528, p. 95**

> The modeled hurricane frequencies at landfall match the observed frequencies obtained from the Base Hurricane Storm Set for different hurricane categories (1 to 5 based on the Saffir-Simpson Hurricane Wind Scale) and different geographic regions (coastal segments), including Northwest Florida, Southwest Florida, Southeast Florida, Northeast Florida, Alabama/Mississippi, and Georgia.

**Pc2cf7eb65320c07f050e — VENDOR — impact_forecasting_2023_submission_20250528, p. 95**

> The comparisons between modeled and observed hurricane frequencies are provided in Form M-1: Annual Occurrence Rates.

**P72f39e17b181374a4d49 — REVIEWER — impact_forecasting_2023_professional_team_20250425, p. 17**

> Reviewed the goodness-of-fit of modeled to historical statewide and regional hurricane frequencies provided in Form M-1.

**P52d116bbab816a1c7d90 — REVIEWER — impact_forecasting_2023_professional_team_20250425, p. 22**

> Reviewed comparisons between modeled and historical landfall rates in M-2.8.

**P26d733630ffb0685dac9 — REVIEWER — impact_forecasting_2023_professional_team_20250425, p. 3**

> 1. Form M-1, pages 299-301: Incomplete.

**Pe61e6dfd2fc5e5c9e5df — REGULATOR_COPY — impact_forecasting_2023_professional_team_20250425, p. 17**

> The goodness- of-fit of modeled to the Reference Hurricane Set statewide and regional hurricane frequencies as provided in Form M-1 will be reviewed.

## 6. FC-TE23-S2

- Corpus: `kcc-2023-exposed-test-e`
- Requirement: `S-2`
- Vendor group: `kcc`

### Candidate regulatory facets

- `S-2.1`: Sensitivity of temporal and spatial outputs is assessed under simultaneous input variation using current scientific and statistical methods.
- `S-2.2`: Appropriate action or inaction follows the sensitivity assessment.

### Bounded source propositions

**Pc2b77ae9ca88d7977777 — REGULATOR — shared_standards_2023_standards, p. 160**

> The modeling organization shall have assessed the sensitivity of temporal and spatial outputs with respect to the simultaneous variation of input variables using current scientific and statistical methods in the appropriate disciplines and shall have taken appropriate action.

**Pbf7ea0fafa0f24d5c7fd — VENDOR — karen_clark_company_2023_kcc_submission, p. 90**

> The sensitivity of temporal and spatial outputs with respect to the simultaneous variation of input values for the KCC US Hurricane Reference Model has been analyzed using accepted scientific and statistical methods.

**Pc3609672606a481485ba — VENDOR — karen_clark_company_2023_kcc_submission, p. 90**

> The sensitivity analysis included four model parameters: Vmax, Rmax, forward speed, and the exponential decay length.

**Pc8c4c1b65417efc98e51 — VENDOR — karen_clark_company_2023_kcc_submission, p. 90**

> The standardized regression coefficient was computed for all four input parameters at three different hurricane intensities (Category 1, Category 3, and Category 5).

**Pc7590f9016bd46cd3357 — VENDOR — karen_clark_company_2023_kcc_submission, p. 92**

> No other input variables impact the magnitude of the output when the input variables V max, Rmax, forward speed, and exponential decay length are varied simultaneously.

**Pb3f7d143c77027212fcd — VENDOR — karen_clark_company_2023_kcc_submission, p. 92**

> The sensitivity analyses from Standard S-2 have been reviewed, and the results are reasonable.

**P0b9dbc2564073528455e — VENDOR — karen_clark_company_2023_kcc_submission, p. 92**

> No action was taken as a result of the analyses performed.

**P9f4f4b59c4f15fb5f0f6 — REVIEWER — karen_clark_company_2023_kcc_review, p. 31**

> Discussed the test hurricane set used when performing the sensitivity analyses.

**P950f6ad2c78336aa45cf — REVIEWER — karen_clark_company_2023_kcc_review, p. 31**

> Discussed that no changes were made in model windfield methodology from the current accepted model, and that no new sensitivity analyses were performed.

**Pdce8043dd0a1b6c407dd — REVIEWER — karen_clark_company_2023_kcc_review, p. 31**

> Verified: YES

**Pe26373fa87622a80d417 — VENDOR — karen_clark_company_2023_kcc_submission, p. 90**

> Since insured losses are dependent on the final impact from a hurricane event and not the temporal variation, the KCC US Hurricane Reference Model does not output losses on an hourly basis.

**P4e9ffd0540b43fcd1cd6 — VENDOR — karen_clark_company_2023_kcc_submission, p. 90**

> Consequently, an analysis of the temporal sensitivities of the lost cost was not performed.

## 7. FC-CI5B-ARA

- Corpus: `rms-ara-2019-development`
- Requirement: `CI-5.B:component-testing`
- Vendor group: `ara`

### Candidate regulatory facets

- `CI-5.B:component-testing.F1`: Documented unit tests for each component, regression tests on incremental builds, and integration tests covering all components at least once.

### Bounded source propositions

**SRC-911a5693d054cdba874c — REGULATOR — fchlpm_2019_hurricane_standards, p. 231**

> 2. Unit tests shall be performed and documented for each component. 3. Regression tests shall be performed and documented on incremental builds. 4. Integration tests shall be performed and documented to ensure the correctness of all hurricane model components. Sufficient testing shall be performed to ensure that all components have been executed at least once.

**SRC-068777a1433cbf0bbde8 — VENDOR — ara_hurloss_10_0_2019_submission_20210310, p. 129, 130**

> B. ARA utilizes testing software written in-house and designed specifically to test, verify, and validate the various components of the models. The testing process has been designed to ensure that all components have been executed at least once. Unit tests are performed for each component as it is written. Regression tests are performed and documented for all incremental builds of the model. Regression testing includes comparisons of annual FCHLPM submissions to the previous year with an investigation and explanation of all associated differences. 2. Provide an overview of the component testing procedures. New components or existing components undergoing any code revision are subject to the testing procedures in place at the time of development or update. Existing components that were developed prior to the FCHLPM standards or under previous FCHLPM standards were tested in accordance with the adopted testing procedures at the time of development. Existing components are subject to new unit-level testing when revisions occur, and all components are subject to ARA’s ongoing system-level and regression testing. ARA’s current software testing procedures include unit-level testing for all newly developed or updated components, system-level testing for the model as a whole and its major sub-systems, and regression testing between versioned builds. Data files undergo specialized testing tailored to the specific dataset and designed to ensure that the data is accurate and complete.

**SRC-448a5b5351bf85ddae4a — REVIEWER — ara_hurloss_10_0_2019_professional_team_20210311, p. 61**

> Reviewed the series of logical tests performed on the loss cost relationships in Form A-6. Discussed the process and tests performed on the surface roughness update.

## 8. FC-VD23-CI6

- Corpus: `verisk-2023-validation-d`
- Requirement: `CI-6`
- Vendor group: `verisk`

### Candidate regulatory facets

- `CI-6.A.1`: Interfaces follow accepted HCI, Interaction Design, and UX practices.
- `CI-6.B.1`: Hurricane-model interface options are unique.
- `CI-6.B.2`: Hurricane-model interface options are explicit and distinctly emphasized.
- `CI-6.C.1`: Florida rate-filing options are limited to Commission-accepted options.

### Bounded source propositions

**Peca6c05cc5a1ae7347f2 — REGULATOR — shared_standards_2023_standards, p. 277**

> A. Interfaces shall be implemented as consistent with accepted principles and practices of Human-Computer Interaction (HCI), Interaction Design, and User Experience (UX) engineering. B. Interface options used in the hurricane model shall be unique, explicit, and distinctly emphasized. C. For a Florida insurance rate filing, interface options shall be limited to those options found acceptable by the Commission.

**P787fa0be76de64d5444b — VENDOR — verisk_2023_verisk_submission, p. 230**

> Verisk user experience (UX) designers consistently employ the accepted principles and practices of HCI, interaction design, and UX engineering when designing and implementing model software interfaces.

**Pc10c3740031acd16ae16 — VENDOR — verisk_2023_verisk_submission, p. 230**

> Our guiding HCI standards and practices are sourced from a variety of industry-recognized benchmarks, including:

**P994c9b52daac737fef37 — VENDOR — verisk_2023_verisk_submission, p. 230**

> • Published practitioners of user experience engineering, including Jacob Nielsen's 'Usability Engineering' Heuristic Evaluation, which lists the following design criteria on page 20:Published practitioners of User Experience engineering, including Jacob Nielsen's 'Usability Engineering' Heuristic Evaluation, page 20: ◦ Simple and natural dialog: Communications are stated clearly and simply in Touchstone.

**P3e8260475aae8285f793 — VENDOR — verisk_2023_verisk_submission, p. 230**

> • The World Wide Web Consortium's (W3C) internationally recognized online library of design principles, including, but not limited to: ◦ Content must be perceivable: The display of substantial amounts of intricate data is at the center of all interaction within Touchstone; the UI is designed to support the visualization and manipulation of that data.

**Pf931414bdcf0634e0821 — VENDOR — verisk_2023_verisk_submission, p. 231**

> The Verisk Hurricane Model for the United States implementation in Touchstone ensures that interface options for ratemaking in the state of Florida are unique, explicit, and distinctly emphasized by means of a detailed loss analysis template: Florida Rate Filing Analysis Template (the FL template).

**P8073d9bf923b84feadc1 — VENDOR — verisk_2023_verisk_submission, p. 231**

> The FL template contains pre-set menu selections and checked (true) and unchecked (false) attributes that are unique, explicit, and distinctly emphasized for the singular objective of running loss analysis calculations for rate making in Florida.

**P0b5fa0b649e8ef35b357 — VENDOR — verisk_2023_verisk_submission, p. 231**

> With the FL template applied, some settings are fixed to meet Florida requirements and cannot be changed.

**P67ce25cc51f50013bac9 — VENDOR — verisk_2023_verisk_submission, p. 231**

> The Touchstone Detailed Loss Configuration user interface only includes options approved for rate filing in the state of Florida.

**Pb93988d46b8d487c1b37 — VENDOR — verisk_2023_verisk_submission, p. 231**

> Finally, options that are not allowed for Florida rate filing, such as 'Storm Surge,' are locked in the OFF position and cannot be changed.

**Pc1fc1a1690a45a08210a — VENDOR — verisk_2023_verisk_submission, p. 231**

> For example, under the 'Event Set' menu selection control, only the currently-certified hurricane event sets are listed, which are '50K US Hurricane – Florida Regulatory' and '100k US Hurricane – Florida Regulatory'.

**Pa540be18f7b76fee1096 — REVIEWER — verisk_2023_verisk_review, p. 89**

> Reviewed a live demonstration of the interface.

**P661eb543918ab8510d06 — REVIEWER — verisk_2023_verisk_review, p. 89**

> Reviewed the Florida Rate Filing Analysis template.

**Pbeb62482cb4c224660df — REVIEWER — verisk_2023_verisk_review, p. 89**

> Reviewed the design, implementation, and evaluation process for the interface options.

**Pd06eb5611b2cb5129f77 — REVIEWER — verisk_2023_verisk_review, p. 89**

> Reviewed the following documentation:

**P12efc6df4b8de04aa140 — REVIEWER — verisk_2023_verisk_review, p. 89**

> Discussed the process of using heuristic evaluations and design critiques to validate UI/UX design.

**Pec09c656f1686c435a77 — REVIEWER — verisk_2023_verisk_review, p. 89**

> Verified: YES

**P43f81f49e68e2ab8f9d5 — VENDOR — verisk_2023_verisk_submission, p. 231**

> All Florida template component control settings are documented and will be made available for inspection by the auditor upon request.

**P569c66bf6099145fbc68 — VENDOR — verisk_2023_verisk_submission, p. 231**

> A demonstration of the FL template user interface will be conducted during the audit.

## 9. FC-IF23-S3-UNCERTAINTY-ANALYSIS

- Corpus: `impact-forecasting-2023`
- Requirement: `IF23-S3-UNCERTAINTY-ANALYSIS`
- Vendor group: `impact_forecasting`

### Candidate regulatory facets

- `IF23-S3-UNCERTAINTY-ANALYSIS.F1`: An uncertainty analysis is performed on temporal and spatial hurricane-model outputs using current scientific and statistical methods.
- `IF23-S3-UNCERTAINTY-ANALYSIS.F2`: Appropriate action is taken.
- `IF23-S3-UNCERTAINTY-ANALYSIS.F3`: The analysis identifies and quantifies how input variables affect output uncertainty when inputs are simultaneously varied.

### Bounded source propositions

**P399882230f1be036fe5f — REGULATOR — fchlpm_2023_hurricane_standards, p. 161**

> The modeling organization shall have performed an uncertainty analysis on the temporal and spatial outputs of the hurricane model using current scientific and statistical methods in the appropriate disciplines and shall have taken appropriate action.

**P6d3f81a46c53d3319711 — REGULATOR — fchlpm_2023_hurricane_standards, p. 161**

> The analysis shall identify and quantify the extent that input variables impact the uncertainty in hurricane model output as the input variables are simultaneously varied.

**Pa97aec67e84c3d9f3873 — VENDOR — impact_forecasting_2023_submission_20250528, p. 152**

> Impact Forecasting assessed the uncertainty of model outputs with respect to the simultaneous variation of input variables using current scientific and statistical methods.

**Pa4436534a5619413c0cb — VENDOR — impact_forecasting_2023_submission_20250528, p. 152**

> Uncertainty analysis of loss costs includes six model input variables: central pressure (Cp), radius of maximum winds (Rmax), translational velocity (VT), far field pressure (FFP), inland decay rate (α), and windfield shape parameter (X1).

**Pa78f44c158c8e688202f — VENDOR — impact_forecasting_2023_submission_20250528, p. 153**

> The expected percentage reduction (EPR) in the variance of loss cost was computed for all six model parameters for hypothetical Category 1, 3, and 5 hurricanes, as shown in Figure 38.

**Pecfdcb18dd9023d0c573 — VENDOR — impact_forecasting_2023_submission_20250528, p. 152**

> Additionally, results of a temporal uncertainty analysis of modeled wind speeds are presented in Disclosure S-3.1 of that submission.

**P3bd6617932781dd78c3b — VENDOR — impact_forecasting_2023_submission_20250528, p. 154**

> Figure 39, Figure 40, and Figure 41 show time series of EPR in the variance of the modeled hourly wind speeds at the landfall point (denoted by the coordinates (9, 0)) of hypothetical Category 1, 3, and 5 hurricanes, respectively.

**P8e42ff53101772c41580 — VENDOR — impact_forecasting_2023_submission_20250528, p. 157**

> The areas with high or low wind risk are determined by their locations with respect to the storm track, which is largely defined by its landfall location and heading direction after landfall.

**Pcb2b37c556114e0c0f6a — VENDOR — impact_forecasting_2023_submission_20250528, p. 157**

> The landfall location and storm heading relative to exposure concentration also have a significant impact on the uncertainties in output results.

**Pb90bbe71cd458f70fac3 — VENDOR — impact_forecasting_2023_submission_20250528, p. 158**

> The results of the uncertainty analyses have been thoroughly reviewed and were found to be reasonable.

**P2ea6e2c4edd21a0f445f — REVIEWER — impact_forecasting_2023_professional_team_20250425, p. 32**

> Discussed current relevance of Form S-6.

**Pd8f966a61ea146932e67 — REVIEWER — impact_forecasting_2023_professional_team_20250425, p. 32**

> Verified: YES

**Pe0dd52d183b0fde6d968 — VENDOR — impact_forecasting_2023_submission_20250528, p. 158**

> No action was taken as a result of the analyses performed.

**Pae23ae25082187a7f20a — VENDOR — impact_forecasting_2023_submission_20250528, p. 154, 155**

> May 28, 2025 154 The temporal uncertainty analysis results described above are location-specific and could vary significantly depending on the selected grid point.

## 10. FC-TE23-G2

- Corpus: `kcc-2023-exposed-test-e`
- Requirement: `G-2`
- Vendor group: `kcc`

### Candidate regulatory facets

- `G-2.A`: Model construction, testing, and evaluation are performed by personnel or consultants with the necessary skills, education, and experience.
- `G-2.B`: The model and submission are reviewed by qualified personnel in the prescribed disciplines, who certify Forms G-1 through G-6 as applicable.

### Bounded source propositions

**P2f24db7b114f95f35993 — REGULATOR — shared_standards_2023_standards, p. 118**

> A. Hurricane model construction, testing, and evaluation shall be performed by modeling organization personnel or consultants who possess the necessary skills, formal education, and experience to develop the relevant components for hurricane loss projection methodologies. B. The hurricane model and hurricane model submission documentation shall be reviewed by modeling organization personnel or consultants in the following professional disciplines with requisite experience: structural/wind engineering (current licensed professional engineer), statistics (advanced degree or equivalent experience), actuarial science (Associate or Fellow of Casualty Actuarial Society or Society of Actuaries), meteorology (advanced degree), and computer/information science (advanced degree or equivalent experience and certifications). These individuals shall certify Expert Certification Forms G-1 through G-6 as applicable.

**P43aec4de4831f19b04d3 — VENDOR — karen_clark_company_2023_kcc_submission, p. 45**

> The KCC US Hurricane Reference Model was developed and verified by professionals who possess the requisite experience and formal education.

**P0a6546e2c7b91c1c5055 — VENDOR — karen_clark_company_2023_kcc_submission, p. 45**

> KCC professionals possess a wide range of skills and expertise in fields including meteorology, engineering, computer science, and statistics honed through experience and education.

**P1b5258b8f7ef7785e235 — VENDOR — karen_clark_company_2023_kcc_submission, p. 45**

> At each stage of model development, these experts evaluated and tested the model for accuracy and reliability using accepted methodologies and rigorous standards appropriate to their respective disciplines.

**Pef7286b252fce95922c4 — VENDOR — karen_clark_company_2023_kcc_submission, p. 45**

> The KCC US Hurricane Reference Model and associated documentation have been thoroughly reviewed by individuals holding the above-mentioned qualifications and are detailed further in Standard G-2, Disclosure 2A.

**P1ff9973d355457721e37 — VENDOR — karen_clark_company_2023_kcc_submission, p. 3**

> All model components have been reviewed by experts in the areas of meteorology, statistics, vulnerability, actuarial science, and computer science for completeness and compliance with the Commission’s Standards, as documented in the signed Expert Certification Forms G-1 to G-6.

**Pa3510929358a82ec6570 — VENDOR — karen_clark_company_2023_kcc_submission, p. 54**

> Table 2 - KCC professional credentials

**P8c40f5e8091332f6a916 — VENDOR — karen_clark_company_2023_kcc_submission, p. 175**

> I hereby certify that I have reviewed the current submission of KCC US Hurricane Reference Model Version 5.0 for compliance with the 2023 Hurricane Standards adopted by the Florida Commission on Hurricane Loss Projection Methodology and hereby certify that:

**Pebde8f0a653d209eccde — VENDOR — karen_clark_company_2023_kcc_submission, p. 175**

> Glen Daraskevich M.S., Engineering and Information Systems Name Professional Credentials (Area of Expertise)

**Pb1c87028a2cf8af96e1a — VENDOR — karen_clark_company_2023_kcc_submission, p. 176**

> I hereby certify that I have reviewed the current submission of KCC US Hurricane Reference Model Version 5.0 for compliance with the 2023 Hurricane Standards adopted by the Florida Commission on Hurricane Loss Projection Methodology and hereby certify that:

**P15afcf3669944c2ff83b — VENDOR — karen_clark_company_2023_kcc_submission, p. 176**

> Daniel Ward Ph.D., Atmospheric Science Name Professional Credentials (Area of Expertise)

**P5ebd1349e2113e4e2885 — VENDOR — karen_clark_company_2023_kcc_submission, p. 177**

> I hereby certify that I have reviewed the current submission of KCC US Hurricane Reference Model Version 5.0 for compliance with the 2023 Hurricane Standards adopted by the Florida Commission on Hurricane Loss Projection Methodology and hereby certify that:

**P2ab986dbd68bdb8fdc19 — VENDOR — karen_clark_company_2023_kcc_submission, p. 177**

> Hongyu Wu Ph.D., Statistics Name Professional Credentials (Area of Expertise)

**Pc8923931385432523a67 — VENDOR — karen_clark_company_2023_kcc_submission, p. 178**

> I hereby certify that I have reviewed the current submission of KCC US Hurricane Reference Model Version 5.0 for compliance with the 2023 Hurricane Standards adopted by the Florida Commission on Hurricane Loss Projection Methodology and hereby certify that:

**P79f19e7136c96aae7af3 — VENDOR — karen_clark_company_2023_kcc_submission, p. 178**

> Shaoning Li Ph.D., Structural/Wind Engineering Name Professional Credentials (Area of Expertise) State:_____ Expiration Date: _____ Professional License Type: _____

**P3173cbdd6708042ff6bb — VENDOR — karen_clark_company_2023_kcc_submission, p. 179**

> I hereby certify that I have reviewed the current submission of KCC US Hurricane Reference Model Version 5.0 for compliance with the 2023 Hurricane Standards adopted by the Florida Commission on Hurricane Loss Projection Methodology and hereby certify that:

**P1060bf9194eb8f3ea7ee — VENDOR — karen_clark_company_2023_kcc_submission, p. 179**

> Girma Tsegaye Bitsuamlak Ph.D., P.Eng., Building Engineering Name Professional Credentials (Area of Expertise) State: Ontario, CA Expiration Date: 8/31/2025 Professional License Type: Professional Engineer

**P1e66906ced32bcd16c9e — VENDOR — karen_clark_company_2023_kcc_submission, p. 180**

> I hereby certify that I have reviewed the current submission of KCC US Hurricane Reference Model Version 5.0 for compliance with the 2023 Hurricane Standards adopted by the Florida Commission on Hurricane Loss Projection Methodology and hereby certify that:

**Pdd248ceab8c9ae73aa81 — VENDOR — karen_clark_company_2023_kcc_submission, p. 180**

> Melinda Vasecka B.A., Mathematics, ACAS Name Professional Credentials (Area of Expertise)

**P886b6a17347a5515e9d9 — VENDOR — karen_clark_company_2023_kcc_submission, p. 181**

> I hereby certify that I have reviewed the current submission of KCC US Hurricane Reference Model Version 5.0 for compliance with the 2023 Hurricane Standards adopted by the Florida Commission on Hurricane Loss Projection Methodology and hereby certify that:

**Pdef4f33355040b5f65f7 — VENDOR — karen_clark_company_2023_kcc_submission, p. 181**

> Vivek Basrur M.S., Management Sciences Name Professional Credentials (Area of Expertise)

**P5028007a2575bc0ed125 — REVIEWER — karen_clark_company_2023_kcc_review, p. 9**

> Reviewed resumes of new personnel:

**P82c9edf63d1f956f0935 — REVIEWER — karen_clark_company_2023_kcc_review, p. 10**

> Discussed that there were no departures of personnel attributable to violations of professional standards.

**P4ceeb88360ee054ca8de — REVIEWER — karen_clark_company_2023_kcc_review, p. 9**

> Verified: YES

## 11. FC-V1A-ARA

- Corpus: `rms-ara-2019-development`
- Requirement: `V-1.A:derivation-basis`
- Vendor group: `ara`

### Candidate regulatory facets

- `V-1.A:derivation-basis.F1`: Development uses at least one allowed evidence or analysis basis; rational analysis, testing, and post-event investigation bases are supported by historical data.

### Bounded source propositions

**SRC-5513c1423f7ac7827167 — REGULATOR — fchlpm_2019_hurricane_standards, p. 165**

> A. Development of the building hurricane vulnerability functions shall be based on at least one of the following: (1) insurance claims data, (2) laboratory or field testing, (3) rational structural analysis, and (4) post- event site investigations. Any development of the building hurricane vulnerability functions based on rational structural analysis, post-event site investigations, and laboratory or field testing shall be supported by historical data.

**SRC-dab7a3c7bc3584b69c2a — VENDOR — ara_hurloss_10_0_2019_submission_20210310, p. 85**

> A. ARA’s vulnerability functions include elements of each of the following: (1) insurance claims data, (2) tests, (3) rational structural analysis, and (4) site inspections. The development of the building hurricane vulnerability functions is supported by historical data. The ARA personnel responsible for developing the damage and loss models have extensive experience in wind load modeling, structural analysis, post-hurricane damage surveys, and meteorology.

**SRC-0ff463230dc6a469bc01 — REVIEWER — ara_hurloss_10_0_2019_professional_team_20210311, p. 33**

> Discussed new claims data received from Hurricane Irma (2017) and Hurricane Michael (2018) used for validation of the model. Discussed that no changes were made to the vulnerability model based on the analysis of the new claims data. Reviewed examples of commercial residential vulnerability curves for different numbers of stories.

## 12. FC-VD23-S2

- Corpus: `verisk-2023-validation-d`
- Requirement: `S-2`
- Vendor group: `verisk`

### Candidate regulatory facets

- `S-2.1`: Sensitivity is assessed for temporal and spatial outputs.
- `S-2.2`: Input variables are varied simultaneously.
- `S-2.3`: The assessment uses current scientific and statistical methods in the appropriate disciplines.
- `S-2.4`: Appropriate action is taken after the assessment.

### Bounded source propositions

**Pc2b77ae9ca88d7977777 — REGULATOR — shared_standards_2023_standards, p. 160**

> The modeling organization shall have assessed the sensitivity of temporal and spatial outputs with respect to the simultaneous variation of input variables using current scientific and statistical methods in the appropriate disciplines and shall have taken appropriate action.

**P9d737f0a1ddbece6fa72 — VENDOR — verisk_2023_verisk_submission, p. 110**

> Model sensitivity has been assessed via investigating the changes in losses as well as wind speed with modeled wind parameters, both spatially and temporarily, using metric standardized regression coefficient, which is widely accepted by the scientific community and is recommended by the Florida Commission.

**Pf25f4b5bd2cd92f5d254 — VENDOR — verisk_2023_verisk_submission, p. 110**

> However, the sensitivities of wind speeds both spatially and temporally were studied using the hypothetical storms in Form S-6.

**P22cc318e237544387018 — VENDOR — verisk_2023_verisk_submission, p. 110**

> Figure 23, Figure 24, and Figure 25 show the standardized regression coefficients vs time for category 1, 3, and 5 hurricanes at landfall.

**P832359aec5f0531e335b — VENDOR — verisk_2023_verisk_submission, p. 110**

> The sensitivity analysis for loss costs uses standardized regression coefficients associated with all six input parameters for Category 1, 3, and 5 hurricanes.

**Pacb5d454735d114c5c1e — VENDOR — verisk_2023_verisk_submission, p. 110**

> The Form S-6 included six model parameters: central pressure, radius of maximum winds, forward speed, far field pressure, gradient wind reduction factor, and peak weighting factor.

**P9e9b69b9086b6f9aaee2 — VENDOR — verisk_2023_verisk_submission, p. 112**

> Verisk has identified, discussed, and disclosed all input variables that impact the output values in S-2.1.

**Pe79dd5c4c0cc151ce37f — VENDOR — verisk_2023_verisk_submission, p. 112**

> The results of the sensitivity analysis have been carefully reviewed and found to be reasonable.

**P21d2899c984d61af6207 — VENDOR — verisk_2023_verisk_submission, p. 112**

> No specific action was taken after reviewing the results.

**P96ffe11fb6452db462ca — REVIEWER — verisk_2023_verisk_review, p. 34**

> No changes were made in model methodology from the current accepted model, and no new sensitivity analyses were performed.

**P3b928dd6afd96ea0c835 — REVIEWER — verisk_2023_verisk_review, p. 34**

> Verified: YES

**P676ec0a204bc30aba01e — VENDOR — verisk_2023_verisk_submission, p. 110**

> An analysis of the temporal sensitivities of the loss costs was not performed since the model does not output the loss costs by hour.

**Pae856e864365d273953e — VENDOR — verisk_2023_verisk_submission, p. 112**

> Decadal and even century-long data collection and investigation are needed to quantify the sensitivity and uncertainty due to such long-term change, which is beyond the scope of this submission.

## 13. FC-IF23-G4-COMPONENT-INDEPENDENCE

- Corpus: `impact-forecasting-2023`
- Requirement: `IF23-G4-COMPONENT-INDEPENDENCE`
- Vendor group: `impact_forecasting`

### Candidate regulatory facets

- `IF23-G4-COMPONENT-INDEPENDENCE.F1`: Meteorology, vulnerability, and actuarial components are each theoretically sound without compensation for potential bias from other components.
- `IF23-G4-COMPONENT-INDEPENDENCE.F2`: Adjustments to one component do not compensate for deficiencies in another.
- `IF23-G4-COMPONENT-INDEPENDENCE.F3`: Interrelationships among components are reasonable, logical, and justifiable.

### Bounded source propositions

**P190b0903eff89cc84637 — REGULATOR — fchlpm_2023_hurricane_standards, p. 123**

> The meteorology, vulnerability, and actuarial components of the hurricane model shall each be theoretically sound without compensation for potential bias from other components.

**P39bd5683be3d80afd003 — REGULATOR — fchlpm_2023_hurricane_standards, p. 123**

> Purpose: The primary components of the hurricane model shall be individually sound and operate independently.

**P99aa0660fe7b82d4ed8c — REGULATOR — fchlpm_2023_hurricane_standards, p. 123**

> In other words, the hurricane model shall not allow adjustments to one component to compensate for deficiencies in other components (compensation which could inflate or reduce hurricane loss costs and hurricane probable maximum loss levels).

**P863d1f675d83f4795449 — REGULATOR — fchlpm_2023_hurricane_standards, p. 123**

> A hurricane model would not meet this standard if an unjustifiable calibration or adjustment has been made to improve the match between hurricane model output and the Model Base Hurricane Set for a specific hurricane.

**P1e6ce1b67b49b4059d5c — REGULATOR — fchlpm_2023_hurricane_standards, p. 123**

> In addition to each component of the hurricane model meeting its respective standards, the interrelationship of the hurricane model components as a whole shall be reasonable, logical, and justifiable.

**P52128906db5f535cc8de — VENDOR — impact_forecasting_2023_submission_20250528, p. 77**

> The meteorological, vulnerability, and actuarial components of the Impact Forecasting Florida Hurricane (FCHLPM) Model are theoretically sound and developed independently.

**P352c7bc7cf4cba2f1c10 — VENDOR — impact_forecasting_2023_submission_20250528, p. 77**

> Each component is validated individually without consideration of possible biases in other components.

**P5acad054fbfc9f3b6933 — REVIEWER — impact_forecasting_2023_professional_team_20250425, p. 13**

> Reviewed all changes in the hurricane model from the current accepted hurricane model, and determined that none of the model updates impacted the independence of each model component.

**P87c5b557967bc176c94d — REVIEWER — impact_forecasting_2023_professional_team_20250425, p. 13**

> No evidence was seen to suggest that one component of the model was deliberately adjusted to compensate for another component.

**Pfb1b5e8273d2a04efb42 — REVIEWER — impact_forecasting_2023_professional_team_20250425, p. 13**

> Discussed that the historical storm footprints that are used for calibration of the vulnerability functions using Bayesian maximum likelihood estimation, further supports the independence of the hurricane model components.

**P7999cc0fb6e3e569ad6b — REVIEWER — impact_forecasting_2023_professional_team_20250425, p. 13**

> Verified: YES

## 14. FC-TE23-CI6

- Corpus: `kcc-2023-exposed-test-e`
- Requirement: `CI-6`
- Vendor group: `kcc`

### Candidate regulatory facets

- `CI-6.A`: Interfaces follow accepted HCI, Interaction Design, and UX practices.
- `CI-6.B`: Hurricane-model interface options are unique, explicit, and distinctly emphasized.
- `CI-6.C`: Florida rate-filing options are limited to Commission-accepted choices.

### Bounded source propositions

**Peca6c05cc5a1ae7347f2 — REGULATOR — shared_standards_2023_standards, p. 277**

> A. Interfaces shall be implemented as consistent with accepted principles and practices of Human-Computer Interaction (HCI), Interaction Design, and User Experience (UX) engineering. B. Interface options used in the hurricane model shall be unique, explicit, and distinctly emphasized. C. For a Florida insurance rate filing, interface options shall be limited to those options found acceptable by the Commission.

**P929da2358a5906be09e8 — VENDOR — karen_clark_company_2023_kcc_submission, p. 168**

> The RiskInsight® User Interface adheres to accepted principles (such as spacing and positioning, size, grouping, and intuitiveness) for user interface design to implement an intuitive and informative user experience utilizing Microsoft Windows Forms, React JS, and Leaflet JS.

**Pc7b88f9c28d69ec34bf8 — VENDOR — karen_clark_company_2023_kcc_submission, p. 168**

> The RiskInsight® user interface design process follows a three phase workflow.

**P16149dfb11d7f7154e81 — VENDOR — karen_clark_company_2023_kcc_submission, p. 168**

> User workflows for interacting with the hurricane model within RiskInsight® follow an intuitive process that makes it clear that all options are within the context of using the hurricane model.

**Pbf6914e1f1ba970c3f50 — VENDOR — karen_clark_company_2023_kcc_submission, p. 168**

> RiskInsight® provides a pre-defined, read-only loss analysis options template which automatically selects only the options found acceptable by the Commission for insurance rate filing in the state of Florida.

**P0092f46c4520ea81525e — REVIEWER — karen_clark_company_2023_kcc_review, p. 87**

> Reviewed the documentation associated with HCI, interactive design, and UX engineering.

**P01035c57acf5e447dd68 — REVIEWER — karen_clark_company_2023_kcc_review, p. 87**

> Discussed the process for enforcing HCI, Interaction Design, and UX engineering through the code review process.

**P2fba4b8998ad69b33521 — REVIEWER — karen_clark_company_2023_kcc_review, p. 87**

> Discussed that the decision process was simplified by eliminating unacceptable options and enabling only relevant choices controlled by an immutable template.

**P5708148f58f023a206e0 — REVIEWER — karen_clark_company_2023_kcc_review, p. 87**

> Reviewed the flowchart of the process for selecting the Florida rate filing template and exposures for loss analysis.

**Pc34a12d13814d8f5912e — REVIEWER — karen_clark_company_2023_kcc_review, p. 87**

> Reviewed and discussed the use of the Florida Hurricane Rate Filing v5.0 template with read-only model options.

**P8efb8b871b4e8a0a7ea7 — REVIEWER — karen_clark_company_2023_kcc_review, p. 87**

> Verified: YES

## 15. FC-CI5B-RMS

- Corpus: `rms-ara-2019-development`
- Requirement: `CI-5.B:component-testing`
- Vendor group: `rms`

### Candidate regulatory facets

- `CI-5.B:component-testing.F1`: Documented unit tests for each component, regression tests on incremental builds, and integration tests covering all components at least once.

### Bounded source propositions

**SRC-911a5693d054cdba874c — REGULATOR — fchlpm_2019_hurricane_standards, p. 231**

> 2. Unit tests shall be performed and documented for each component. 3. Regression tests shall be performed and documented on incremental builds. 4. Integration tests shall be performed and documented to ensure the correctness of all hurricane model components. Sufficient testing shall be performed to ensure that all components have been executed at least once.

**SRC-de17727d15a0663cb53f — VENDOR — rms_21_0_2019_submission_20210422, p. 160**

> 2. Unit tests shall be performed and documented for each component. All software components are unit tested as they are developed or modified. The results of the unit tests are summarized in technical specification documents that are written by software developers while implementing and testing software components, or in the JIRA incident database. 3. Regression tests shall be performed and documented on incremental builds. A large suite of regression tests are performed and documented on incremental builds of the RiskLink and Risk Modeler software. The majority of the regression tests are implemented using automated tools, including Rational Robot and Rational Functional Tester test scripts, though some additional manual testing is always performed. The automated regression tests are split into two sets. The first set is a broad but shallow set of tests that are executed by the software development team before passing the build to the QA department. The QA department then executes an extensive, broad and deep set to check for stability of results in all areas of the software. 4. Integration tests shall be performed and documented to ensure the correctness of all hurricane model components. Sufficient testing shall be performed to ensure that all components have been executed at least once. Integration tests are performed and documented to ensure correctness of all components and data defining the model. Most of the integration testing is done by executing the product as a complete package, using a comprehensive suite of test scripts supplemented with a dditional manual tests, to ensure that component interactions that would escape unit testing are checked. These tests cover the complete start-to-finish workflow of the user of the software, and contain a wide range of possible inputs, thus ensuring that all components relevant to this submission are executed at least once.

**SRC-6f80b536f6ad1c88daab — REVIEWER — rms_21_0_2019_professional_team_20210422, p. 61**

> Reviewed unit test for hazard event rates implementation.

## 16. FC-VD23-M3

- Corpus: `verisk-2023-validation-d`
- Requirement: `M-3`
- Vendor group: `verisk`

### Candidate regulatory facets

- `M-3.A.1`: Modeled hurricane-parameter distributions are consistent with the Model Base Hurricane Set.
- `M-3.A.2`: Differences from the Model Base Hurricane Set are justifiable.
- `M-3.B.1`: Landfall-frequency distributions reflect the category 1-5 Model Base Hurricane Set.
- `M-3.B.2`: Landfall frequencies are consistent with observations for each coastal segment of Florida, Alabama, Georgia, and Mississippi.
- `M-3.B.3`: Differences in coastal landfall frequencies are justifiable.
- `M-3.C.1`: Maximum one-minute sustained 10-meter windspeed defines landfall intensity for both the base set and modeled damaging hurricanes.
- `M-3.C.2`: The windspeed is within the Saffir-Simpson category ranges.

### Bounded source propositions

**Paff1a77ca108481cb610 — REGULATOR — shared_standards_2023_standards, p. 144**

> A. Modeled probability distributions of hurricane parameters shall be consistent with the Model Base Hurricane Set. Any differences shall be justifiable. B. Modeled hurricane landfall frequency distributions shall reflect the Model Base Hurricane Set used for category 1 to 5 hurricanes and shall be consistent with those observed for each coastal segment of Florida and neighboring states (Alabama, Georgia, and Mississippi). Any differences shall be justifiable. C. The hurricane model shall use maximum one-minute sustained 10-meter windspeed when defining hurricane landfall intensity. This applies both to the Model Base Hurricane Set used to develop landfall frequency distributions as a function of coastal location and to the modeled winds in each hurricane which causes damage. The associated maximum one-minute sustained 10-meter windspeed shall be within the range of windspeeds (in statute miles per hour) categorized by the Saffir- Simpson Hurricane Wind Scale.

**Pfaa96f6fa3935567c3d9 — VENDOR — verisk_2023_verisk_submission, p. 79**

> The modeled probability distributions for landfall location, hurricane intensity, forward speed, radius of maximum winds, storm heading at landfall and gradient wind reduction factor are consistent with observed Model Base Hurricane Set and are bounded by observed extremes.

**P92b59bef18ee8587d06e — VENDOR — verisk_2023_verisk_submission, p. 80**

> The probability distributions used for all hurricane parameters and characteristics are derived based on the available historical hurricane data.

**P407d9a8f428bfb2da678 — VENDOR — verisk_2023_verisk_submission, p. 80**

> Probability distributions are appropriate for each parameter, for example, discrete landfall counts (Negative Binomial), central pressure which is continuous and highly skewed (Weibull), and the gradient wind reduction factor (Normal).

**P08536df1741c435df900 — VENDOR — verisk_2023_verisk_submission, p. 80, 81**

> A summary of rationale/justification can be found in Form S-3: Distributions of Stochastic Hurricane Parameters and in Standard M-1: Model Base Hurricane Set.

**P3ce519f2d29f026b184d — VENDOR — verisk_2023_verisk_submission, p. 80**

> As shown in Figure 9, the modeled hurricane probabilities for categories 1-2 and 3-5 hurricanes accurately represent the historical record through 2022, and are consistent with those observed for each coastal segment of Florida, Alabama, Georgia and Mississippi.

**P9ce5490fca0102382aac — VENDOR — verisk_2023_verisk_submission, p. 80**

> The annual probabilities are shown in Table 29 of Form M-1: Annual Occurrence Rates.

**P3ec2054a7a141268e4c8 — VENDOR — verisk_2023_verisk_submission, p. 79**

> The probability distribution for landfall location is defined on 50-nautical-mile coastal segments.

**Pcb2848ac37d66c89f0f2 — VENDOR — verisk_2023_verisk_submission, p. 79**

> Goodness-of-fit tests show a close agreement between historical and modeled landfall frequencies by Florida segments.

**Pd42fc0fba11a5c87081b — VENDOR — verisk_2023_verisk_submission, p. 79**

> Also, for the state as a whole, the modeled average annual frequency of 0.57 landfalling hurricanes per year agrees with the average annual historical frequency of 0.61 landfalling hurricanes per year.

**Pf2669ee6e391f22f6dc9 — VENDOR — verisk_2023_verisk_submission, p. 79**

> Weibull distributions are fitted to the historical data for each 100-nautical-mile coastal segment.

**P8ab97349f038c6379e4f — VENDOR — verisk_2023_verisk_submission, p. 79**

> The Weibull distribution was selected based on goodness-of-fit tests with actual historical data.

**P14fe3304c3e810ea87a7 — VENDOR — verisk_2023_verisk_submission, p. 79**

> The Weibull scale and shape parameters are estimated using the maximum likelihood estimation method.

**P6be8fe80621b083d1e6e — VENDOR — verisk_2023_verisk_submission, p. 80**

> The model uses maximum one-minute sustained 10-meter windspeed to define hurricane landfall intensity, both for developing the Model Base Hurricane Set and for the modeled windspeeds in each hurricane that causes damage.

**Pa2bf6b95e5972d5664e2 — VENDOR — verisk_2023_verisk_submission, p. 80**

> The windspeed values available in Form M-1: Annual Occurrence Rates are categorized according to the Saffir-Simpson Hurricane Wind Scale.

**P75fa38426790b0fd1e8b — REVIEWER — verisk_2023_verisk_review, p. 23**

> Reviewed the regression equation for GWRF and input of HURDAT2 data.

**P0421db370fe19b0bb0fb — REVIEWER — verisk_2023_verisk_review, p. 23**

> Reviewed the goodness-of-fit results for Alabama, Georgia, and Mississippi under M-1, Audit 4.

**P28a01a67e18987afc036 — REVIEWER — verisk_2023_verisk_review, p. 23**

> Reviewed the methodology for selecting stochastic storm tracks.

**P8a48f205f9c0b2dab390 — REVIEWER — verisk_2023_verisk_review, p. 23**

> Reviewed a statistical comparison of historical to stochastic storms making multiple Florida landfalls.

**P0a217372a5c5fbddf5c7 — REVIEWER — verisk_2023_verisk_review, p. 24**

> Discussed that landfall locations are selected from a continuous uniform distribution within each 50-mile coastal segment.

**Pafd897bc9f80e60992f9 — REVIEWER — verisk_2023_verisk_review, p. 24**

> Reviewed the published scientific literature used for simulating hurricane model variables.

**P6283f6cffcb8ceb4e886 — REVIEWER — verisk_2023_verisk_review, p. 30**

> Reviewed Form M-3.

**P7dd70568969537661c6c — REVIEWER — verisk_2023_verisk_review, p. 23**

> Verified: YES

**Pf003cc89a659eb9c81d9 — REVIEWER — verisk_2023_verisk_review, p. 23**

> Reviewed a requested revision to the text under M-3.A to clarify the Verisk definition of intensity in the model.

**Pe7ffb0ab11c85cfaf362 — VENDOR — verisk_2023_verisk_submission, p. 81**

> No changes have been made to the modeled distributions of parameters in the Model Base Hurricane Set that are not contained in Form S-3: Distributions of Stochastic Hurricane Parameters.

## 17. FC-TE23-A2

- Corpus: `kcc-2023-exposed-test-e`
- Requirement: `A-2`
- Vendor group: `kcc`

### Candidate regulatory facets

- `A-2.A`: Loss costs and PMLs reflect all insured wind damage from qualifying landfalling and bypassing hurricanes in Florida.
- `A-2.B`: A documented procedure distinguishes wind-related hurricane losses from other-peril losses.

### Bounded source propositions

**Pd07398e5a937639346dc — REGULATOR — shared_standards_2023_standards, p. 221**

> A. Modeled hurricane loss costs and hurricane probable maximum loss levels shall reflect all insured wind related damages from hurricanes that produce minimum damaging windspeeds or greater on land in Florida. B. The modeling organization shall have a documented procedure for distinguishing wind-related hurricane losses from other peril losses.

**Pa813f481c74da8a4d111 — VENDOR — karen_clark_company_2023_kcc_submission, p. 143**

> Modeled hurricane loss costs and hurricane probable maximum loss levels reflect all insured wind-related damages from storms classified as landfalling or by-passing hurricanes—consistent with the definitions stated in the Hurricane Standards Report of Activities as of November 1, 2023 developed by the FCHLPM—that produce minimum damaging wind speeds or greater on land in Florida.

**Padd548ce1ea9867609b2 — VENDOR — karen_clark_company_2023_kcc_submission, p. 143**

> The calculation of hurricane loss costs and hurricane probable maximum loss levels for Florida include damage from landfalling and by-passing model-generated storms.

**P7c064dc0717b220152d0 — VENDOR — karen_clark_company_2023_kcc_submission, p. 143**

> KCC has a documented procedure for distinguishing wind-related hurricane losses from other peril losses, which will be available for review by the Professional Team during the on-site visit.

**Pbfb8c1472d2488904531 — VENDOR — karen_clark_company_2023_kcc_submission, p. 143**

> The hurricane loss costs and hurricane probable maximum loss levels in this submission do not include storm surge or inland flood losses.

**P34364764f559f42b2a1a — VENDOR — karen_clark_company_2023_kcc_submission, p. 143**

> If the storm surge and inland flood model options are not selected, no storm surge or inland flood losses are included in the calculations.

**P810757276432805a24ce — REVIEWER — karen_clark_company_2023_kcc_review, p. 60**

> Discussed that the model begins to estimate wind-related damage at a 1-minute windspeed of 25 mph or greater at 10-meter height.

**P3dab55bb8e9558e2aa85 — REVIEWER — karen_clark_company_2023_kcc_review, p. 60**

> Discussed that landfalling hurricanes are defined as events with a 1-minute sustained windspeed at 10-meter height of at least 74 mph at landfall.

**P48e7a454d2b863a1408a — REVIEWER — karen_clark_company_2023_kcc_review, p. 60**

> Discussed the process and criteria for identifying by-passing hurricanes.

**P4355ac931c008555c78c — REVIEWER — karen_clark_company_2023_kcc_review, p. 60**

> Reviewed the documented procedure for distinguishing wind losses from other peril losses.

**P43ba5d008622b265acee — REVIEWER — karen_clark_company_2023_kcc_review, p. 61**

> Discussed that the model calculates and saves wind and other peril losses separately.

**P89244dae5eea42e0f8a7 — REVIEWER — karen_clark_company_2023_kcc_review, p. 61**

> Discussed that the model does not take into account any damage resulting directly and solely from flood when the wind-only peril is selected.

**P9a49026cc7934c06ea21 — REVIEWER — karen_clark_company_2023_kcc_review, p. 61**

> Reviewed the documented procedure of the methodology for distinguishing wind-related hurricane losses from other peril losses.

**P4e5adb3c2d2eb9c50299 — REVIEWER — karen_clark_company_2023_kcc_review, p. 60**

> Verified: YES

**P4a4e69f27594b1670637 — REVIEWER — karen_clark_company_2023_kcc_review, p. 3**

> KCC discussed the manual error that occurred when generating FHCF losses from the Model Base Hurricane Set where demand surge was not applied and required revisions to Forms A-2 and A-3.

**Pb9babdf8fcd0c7512316 — REVIEWER — karen_clark_company_2023_kcc_review, p. 3**

> The Professional Team reviewed the error, how it occurred, the revised forms, and corrective actions taken by KCC to mitigate against similar issues in the future, and confirmed there was no issue with the model, the platform, or other submission forms.

## 18. FC-M3B-RMS

- Corpus: `rms-ara-2019-development`
- Requirement: `M-3.B:historical-coastal-consistency`
- Vendor group: `rms`

### Candidate regulatory facets

- `M-3.B:historical-coastal-consistency.F1`: Modeled landfall-frequency distributions reflect the Base Hurricane Storm Set and are consistent with observed frequencies.

### Bounded source propositions

**SRC-211f3cc2d0ec2e15b1e3 — REGULATOR — fchlpm_2019_hurricane_standards, p. 120**

> B. Modeled hurricane landfall frequency distributions shall reflect the Base Hurricane Storm Set used for category 1 to 5 hurricanes and shall be consistent with those observed for each coastal segment of Florida and neighboring states (Alabama, Georgia, and Mississippi).

**SRC-65d640dfbb45b5c60224 — VENDOR — rms_21_0_2019_submission_20210422, p. 67**

> Modeled landfall frequencies are consistent with what has been observed historically for each geographical area of Florida and neighboring states, as demonstrated in Form M-1. The model is consistent both in terms of the total rate of hurricanes making landfall by region, and the rate of hurricanes of various intensities by region.

**SRC-1a1ebd756dca5c4c303b — VENDOR — rms_21_0_2019_submission_20210422, p. 16**

> The last step is a calibration process ensuring that simulated landfall frequencies are in agreement with the historical record. Target landfall rates are computed on a set of 69 linear coastal segments by smoothing the historical landfall rates. This smoothing technique is widely used in the scientific community to reduce the local under-sampling or over-sampling issues associated with the limited historical records (119 years). The stochastic set is then adjusted toward these targets using methods such as selecting the optimum intensity time series among several candidates.

**SRC-94f9b38842d735567c0a — REVIEWER — rms_21_0_2019_professional_team_20210422, p. 18**

> Reviewed the methodology for landfall updates by gate and by category and for smoothing the historical frequencies.

## 19. FC-VD23-A2

- Corpus: `verisk-2023-validation-d`
- Requirement: `A-2`
- Vendor group: `verisk`

### Candidate regulatory facets

- `A-2.A.1`: Loss costs and PMLs reflect all insured wind-related hurricane damage.
- `A-2.A.2`: Included hurricanes produce minimum damaging windspeed or greater on land in Florida.
- `A-2.B.1`: A documented procedure distinguishes hurricane wind losses from other-peril losses.

### Bounded source propositions

**Pd07398e5a937639346dc — REGULATOR — shared_standards_2023_standards, p. 221**

> A. Modeled hurricane loss costs and hurricane probable maximum loss levels shall reflect all insured wind related damages from hurricanes that produce minimum damaging windspeeds or greater on land in Florida. B. The modeling organization shall have a documented procedure for distinguishing wind-related hurricane losses from other peril losses.

**P3f15e333db3aad32d6e2 — VENDOR — verisk_2023_verisk_submission, p. 168**

> Modeled hurricane loss costs and hurricane probable maximum loss levels reflect all insured wind related damages from storms that reach hurricane strength and produce minimum damaging windspeeds or greater on land in Florida.

**P598252c57cf4641b6712 — VENDOR — verisk_2023_verisk_submission, p. 168**

> The calculation of hurricane loss costs and probable maximum losses includes the losses from all hurricanes contained in the Event Set referenced in Table 16 that make landfall or bypass Florida.

**P5d77e457098072b9fbcc — VENDOR — verisk_2023_verisk_submission, p. 168**

> Modeled loss costs and probable maximum losses reflect all loss costs resulting from modeled bypassing hurricanes as well as those making landfall in Florida.

**P67c47773de54bbe29687 — VENDOR — verisk_2023_verisk_submission, p. 168**

> Damage is included in the calculation of hurricane loss costs and probable maximum losses from the time the hurricane first causes damaging wind speeds on land in Florida.

**P9c4d3d5c8200dca38300 — VENDOR — verisk_2023_verisk_submission, p. 168**

> Damage included in the calculation of hurricane loss costs and probable maximum losses comes from events producing at least minimum damaging wind speeds on land in Florida.

**P50b6da9fbffbe4dd74bf — VENDOR — verisk_2023_verisk_submission, p. 168**

> Hurricane wind is the only peril available to users of the FL template to run an analysis with the Verisk Hurricane Model for the United States V3.0.0 as Implemented in Touchstone 2024A.

**P3362c33a350abec1944c — VENDOR — verisk_2023_verisk_submission, p. 169**

> Damage resulting from concurrent or preceding storm surge flooding is estimated separately from wind damage, and, if combined damage from the two perils exceeds 100% of a structure’s replacement value, the modeled loss estimates for the two perils are normalized.

**P0383f9d26fd21f682ce3 — VENDOR — verisk_2023_verisk_submission, p. 169**

> Model users of the FL template do not have the option of running storm surge to produce or display losses related to the storm surge peril.

**P5c8c73feb8419aa9606a — VENDOR — verisk_2023_verisk_submission, p. 169**

> Fluvial and pluvial flooding from hurricane induced precipitation perils are not included in losses when using the FL template.

**Pd63f8115c99d4ef2e16e — REVIEWER — verisk_2023_verisk_review, p. 62**

> Reviewed the documented procedure for distinguishing wind-related hurricane losses from other peril losses.

**Pe14c1665dee7239045bf — REVIEWER — verisk_2023_verisk_review, p. 62**

> Discussed that modeled loss costs and PML levels reflect all insured wind related damages from storms that reach hurricane strength and produce minimum damaging windspeeds or greater over land in Florida.

**P3054fe97523a224b2525 — REVIEWER — verisk_2023_verisk_review, p. 63**

> Discussed that the calculation of loss costs and PMLs include the losses from all hurricanes that make landfall in Florida or are Florida by-passers.

**P753378823924bd5af3f8 — REVIEWER — verisk_2023_verisk_review, p. 63**

> Discussed that damage is included in the calculation of loss costs and PMLs from the time the hurricane first causes damaging windspeeds over land in Florida.

**P4b248cb33453e635f37f — REVIEWER — verisk_2023_verisk_review, p. 63**

> Discussed that the storm surge model is separate from the wind model and is run in parallel with the wind model.

**Pc357737ea485d574f47d — REVIEWER — verisk_2023_verisk_review, p. 63**

> Discussed that precipitation flood peril is not included in the wind model.

**Pea128c4f2d63bf9881d1 — REVIEWER — verisk_2023_verisk_review, p. 63**

> Discussed that storm surge losses are not output from the model when using the Florida Rate Filing Analysis template.

**P2d1fef24ac599012ade6 — REVIEWER — verisk_2023_verisk_review, p. 62**

> Verified: YES

**P08bae1d4f33b9d06cfb6 — REVIEWER — verisk_2023_verisk_review, p. 3**

> Verisk stated that the incorrect historical event set had been used to complete the initial forms, and that the forms were revised with updated values to reflect the correct historical event set.

**Pa2dc9d2b3b1295e5d7da — REVIEWER — verisk_2023_verisk_review, p. 3**

> Verisk indicated that Form S-4, Form S-5, Form A-2, and Form A-3 were revised and provided with the on-site review materials on March 20, 2025.

**P8aefb5550f9bee1777ca — VENDOR — verisk_2023_verisk_submission, p. 168**

> No other peril loss analyses are available.
