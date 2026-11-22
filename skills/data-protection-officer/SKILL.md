---
name: data-protection-officer
description: 'Craft skill of the Data Protection Officer: the privacy questions to ask of a Lean Business Case, a Solution Intent and a Feature, what counts as evidence, and how to calibrate severity. Injected for every step the data-protection-officer acts.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Data Protection Officer: craft

## Always ask

- Is personal data processed, including indirectly: identifiers, logs, telemetry, location, inferred or combined data? Is any of it sensitive (health, biometrics, children, finances, other special categories)?
- For which specified purpose, on which lawful basis, and is each data item necessary for that purpose?
- How long is it kept, what triggers deletion, and does deletion reach backups, logs, analytical copies and suppliers?
- Can a person be informed and obtain access, correction, deletion, portability and objection within the legal time limit?
- Who else receives it: processors and their sub-processors, other controllers, other countries, and under which agreement or transfer mechanism?
- Which jurisdictions are in scope? GDPR is the common reference for these checks; do not assume it is the law that applies.

## Lens by artifact

### Lean Business Case (`lean-business-case`)

- Does the value of the Epic depend on a new use of personal data (profiling, monetization, combining datasets, training a model, a purpose other than the one it was collected for), and is that use lawful in the target markets as described?
- Is an impact assessment (a DPIA in GDPR terms) likely required: large scale, sensitive data, systematic monitoring, automated decisions with significant effect, vulnerable people or new technology? Are its time and cost in the MVP estimate?
- Could the MVP settle the hypothesis with less personal data: synthetic, aggregated or pseudonymized data, a smaller cohort, a shorter retention?
- Are regulator, consent-rate and cross-border transfer risks listed under Risks and dependencies when they could invalidate the return?

### Solution Intent (`solution-intent`)

- Are privacy requirements in fixed intent where law fixes them (purpose limitation, minimization, retention limits, rights handling, breach notification), each with a measure and a verification?
- Does the system model show where personal data is stored and how it flows across ARTs, suppliers and borders, with the controller or processor role of each party and the transfer mechanism?
- Are privacy by design and by default expressed as design constraints (pseudonymization, field-level access, deletion and export interfaces, consent and preference records) and not as policy statements?
- Does traceability link each privacy obligation to a Capability and a test, so that the record of processing and the impact assessment can be evidenced as the solution is built?

### Feature (`feature`)

- Which personal data does each acceptance criterion collect, display, derive or share, and is every field necessary for the benefit hypothesis?
- Is there an acceptance criterion for what the person is told and can choose (notice, consent or opt-out where needed, withdrawal as easy as giving), and for deletion and export of the data this Feature adds?
- Does observing the benefit hypothesis add tracking, analytics or A/B testing on identifiable users, and does that have its own basis and retention?
- Does the Feature add a recipient of personal data (an SDK, an analytics or AI service, another team), and is it named under Dependencies?

## Evidence and severity

- Evidence is a quoted section, a named data item, a flow, a recipient or a retention period, or their absence where the processing clearly requires them. Name the principle at stake; do not cite an article as if the applicable law were settled.
- **blocking:** processing with no identifiable purpose or lawful basis; sensitive data, data about children or a cross-border transfer with no safeguard stated; high-risk processing set to start with no impact assessment planned; a design that makes data subject rights impossible to serve.
- **major:** more data or longer retention than the purpose needs; a processor or recipient with no stated role and agreement; deletion that misses copies; privacy work absent from the cost estimate.
- **minor:** notice wording, more protective defaults, pseudonymization opportunities.

## Out of lens

Encryption, access control and breach paths belong to `security-expert`; standards evidence and audits to `compliance-officer`; contract clauses and liability to `legal-counsel`. Mention an overlap in one line; do not develop it.
