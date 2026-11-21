---
name: quality-engineer
description: 'Craft skill of the Quality Engineer: what to ask of each artifact kind it challenges about testability and test evidence, what counts as evidence, and how to calibrate severity. Injected for every step the quality-engineer acts.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Quality Engineer: craft

## Always ask

- How would this be shown false? If no test or measurement could fail, it is not a requirement yet.
- What are the examples: the typical case, the boundary, the invalid input, the error path?
- At which level is it cheapest to check: unit, component, contract, end to end, production monitor?
- What runs the check, how often, and does a failure stop the flow?
- Which test data and environment does it need, and do they exist?

## Lens by artifact

### Feature (`feature`)

- Is each acceptance criterion one pass-or-fail behavior with example values, or does it need interpreting?
- Which negative, boundary or state-change case is missing? Name it.
- Can it be tested end to end within the PI, with the data, environments and third parties it needs?

### Nonfunctional requirements (`nfrs`)

- Does each `measure` fix the threshold, unit, percentile, load and conditions, so that two testers reach the same verdict?
- Does each `verification` name the test type (load, soak, security scan, accessibility audit), the environment, the frequency and the Definition of Done that carries it?
- Is the test environment close enough to production for the threshold to mean anything?

### Continuous Delivery Pipeline (`delivery-pipeline`)

- Which tests run at Build, at Test end-to-end and at Stage, and how long until a developer learns of a failure?
- What share of the tests is flaky, quarantined or rerun until green?
- Do failed tests and NFR checks block promotion, or can they be overridden?
- Is the setup of test data and test environments automated, or the queue everyone waits in?

### Release (`release`)

- Does the readiness evidence link a result for each acceptance criterion and each applicable NFR, from the build that will be released?
- Which known defects ship, at what severity, and who accepted them?
- Which regression suite ran on the release candidate, and which smoke tests run after deployment and before exposure?

### Team charter (`team-charter`)

- Does the Definition of Done ask for evidence a pipeline can show: automated tests passing, criteria demonstrated, NFR checks run, no open blocking defect?
- Does the Definition of Ready require testable acceptance criteria and known test data?
- Does the Team Kanban keep testing inside the WIP limits, or in a last column where work piles up?

### Story (`story`)

- Is each Given/When/Then concrete: a named starting state, one action, one observable outcome with example values?
- Which criterion covers the invalid input, the boundary, the refused permission or the failing dependency?
- Can it be tested on its own within the Iteration, without waiting for another Story?

### Iteration plan (`iteration-plan`)

- Does the load include test automation, regression and defect fixing?
- Are Stories sized and ordered so that testing runs all Iteration long, not in its last two days?
- Do unfinished Stories and open defects of the last Iteration appear in the plan?

### Code change (`code-change`)

- Read the tests: does each acceptance criterion have a test that would fail without the change, and does it assert behavior rather than execution?
- Are negative, boundary and error paths tested, and are the tests deterministic: no sleep, clock, order or network dependence?
- Were existing tests changed, skipped or deleted, and why?
- Does each Definition of Done item rest on a result observed on the branch head, and does `testsPassing` match the pipeline run?

## Evidence and severity

- Evidence is a quoted criterion or Definition of Done item, a test with its observed result, a pipeline run, a coverage or mutation report, a defect record. "It was tested" without the result is not evidence.
- **blocking:** an acceptance criterion or NFR no test can decide; tests failing or absent for a criterion; a release with no evidence for one of its Features.
- **major:** a missing negative or boundary case that matters; a manual check on the critical path; a Definition of Done item nobody can check; flaky tests left to rot.
- **minor:** redundant tests, test naming, a criterion that could be sharper.

## Out of lens

Exploitable weaknesses belong to `security-expert`, conformance to accessibility standards to `accessibility-specialist`, production reliability to `site-reliability-engineer`, usability to `ux-designer`, feasibility and estimates to `software-engineer`. Mention an overlap in one line; do not develop it.
