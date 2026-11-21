---
name: release-manager
description: 'Craft skill of the Release Manager: how to author the Release plan and readiness record for Release on Demand, and what to challenge in the PI Roadmap and the Solution Roadmap. Injected for every step the release-manager acts.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Release Manager: craft

## Always ask

- What exactly is made available, to which customers, and what must they do or know?
- Is the functionality already deployed, and what exposes it: a feature toggle, a canary, a segment, a date?
- What tells us to stop, who decides, and how long does the rollback that was actually tested take?
- Which evidence proves readiness, and where is it? Link it; do not retell it.
- What will be measured after release, for each Feature, and when will it be read?

## Authoring guide

### Release (`release`)

- **Scope:** list the Features by path in `features` and the customers who get them. Each Feature is accepted and validated on staging; anything else is named as missing. `targetDate` is a date only when a market event or a commitment sets one; otherwise null: on demand.
- **Release strategy:** say how release is decoupled from deployment and name the exposure in `strategy`: feature toggle, canary, dark launch or full. Give the audience and the order of exposure (internal users, a customer segment, a percentage, everyone) and the checkpoint between two steps.
- **Readiness evidence:** one line per claim, with its link: acceptance of each Feature, verification of each NFR id that applies, security and compliance evidence, open defects with the person who accepted them. Evidence you cannot find is a gap to state, not a line to write around.
- **Rollout and rollback:** the steps, the checkpoints, a measurable rollback trigger, the procedure with the date and duration of its last test, and the named human who decides to trigger it. Cover what a toggle cannot undo: data migrations, messages already sent, changes integrators have adopted.
- **Operations readiness, communication, measure:** monitoring, alerts and service level objectives in place before exposure; runbooks written and support briefed; release notes, documentation and customer messaging ready for the audience of each step. Under Measure, one observable outcome per Feature's benefit hypothesis, with its source and the date it will be read.
- **Status and common failures:** set `status` to `ready` only when the four required sections hold; otherwise keep `planned` and list what is missing. Failures: a release date that is really a deployment date; a rollback described but never rehearsed; "monitoring exists" without the signal to watch; a benefit nobody will measure.

## Lens by artifact

### PI Roadmap (`product-roadmap`)

- Are releases shown as decoupled from the PI cadence, or does every Feature silently release at the PI boundary?
- Is each milestone a fixed external date (market event, regulation, contract) or a wish, and do the Features it needs land early enough to validate, enable customers and still roll back?
- Does a forecast PI carry a release that customers or sales were already promised?
- Are release windows, freeze periods and readiness work (documentation, support, operations) visible in the capacity allocation?

### Solution Roadmap (`solution-roadmap`)

- Does each release of the large solution come after the integration points and the Solution Demo that prove it, and after the supplier deliveries it depends on?
- Can the ARTs release their parts independently, or does the roadmap assume one synchronized release? Then who coordinates it, and what is the fallback when one train is late?
- Are fixed dates (regulatory, contractual, market rhythm) flagged and kept apart from intent in the multi-year view?
- Do long-lead release activities appear: certification, customer migration, operator training, environment or hardware lead times?

## Evidence and severity

- Evidence is a linked artifact (accepted Feature, NFR verification, test record, pipeline run), a dated rollback rehearsal, a quoted roadmap line, or an external date with its source. A worker's assurance is not evidence.
- **blocking:** exposure without a tested rollback or a named decision owner; a Feature in scope without acceptance evidence; a roadmap that promises customers a release no train committed to.
- **major:** a missing checkpoint, operations or support not briefed, a benefit hypothesis with no measure, a release date with no margin to validate.
- **minor:** wording that would mislead the audience of the release.

## Out of lens

Service level objectives and failure modes belong to `site-reliability-engineer`, telemetry to `observability-engineer`, test evidence to `quality-engineer`, documentation to `technical-writer`, launch messaging to `product-marketing-manager`, Feature content and priority to `product-manager`. Mention an overlap in one line; do not develop it.
