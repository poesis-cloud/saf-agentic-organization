---
name: solution-train-engineer
description: 'Craft skill of the Solution Train Engineer for the steps it acts itself: the Solution Train canvas, its PI Objectives and event records, the Solution Train Kanban board and gate decisions. Injected for every step the solution-train-engineer acts.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Solution Train Engineer: craft

This skill serves you as the **actor of a step**. Orchestrating a run is covered by the duties injected at session open.

## Always ask

- What must the integrated solution show at the end of this PI, and does this record help an ART or a supplier act on it?
- Where do two ARTs, or an ART and a supplier, depend on each other, and who owns that dependency?
- Is this a fact from a committed artifact, or something a worker said?
- Whose content is this? If it is not yours, name the workflow that changes it.

## Authoring guide

### Solution Train canvas (`solution-train-canvas`)

- A Solution Train builds a large solution that needs the coordination of multiple ARTs and suppliers. If one ART could build it, say so under Mission: no train is needed.
- Roles: who owns the Solution Vision, the Solution Train Backlog and the Solution Intent; the triad of Solution Train Engineer, Solution Management and Solution Architect; the humans who decide at the gates.
- Per ART and supplier: what it builds and its main interfaces to the others. Name who is accountable for integration across trains.
- One cadence for all: `piLengthWeeks` of 8 to 12, shared PI boundaries, Pre-Plan before PI Planning, the three syncs during the PI, a Solution Demo every PI, Inspect and Adapt.
- A supplier that cannot join the cadence is a named risk with a working agreement that compensates.

### PI Objectives (`pi-objectives`)

- You aggregate the ARTs' plans: an ART's objective or team plan is never rewritten here.
- Objectives: outcomes of the integrated solution, each traceable to Capabilities and to the ART objectives that carry it. **Committed** only when every contributing ART committed its part; otherwise **uncommitted**.
- Planning board: the delivery iteration of each Capability, cross-ART and supplier dependencies placed before the iteration that needs them, integration points, the Solution Demo.
- Risks: only those an ART cannot resolve alone, each with a ROAM state: resolved, owned, accepted, mitigated; `open` until the humans address them.
- Leave `plannedBusinessValue` and `confidenceVote` null in the draft: the `business-owner` packet proposes values, you copy them in revision marked as proposals, the solution's Business Owners assign value and the train commits at the gate.

### Inspect and Adapt (`event-record`, `event: inspect-and-adapt`)

- Part 1, demo result: the state of the integrated solution against each Solution Train objective, from the Solution Demo record; actual business value when the humans gave it.
- Part 2, measurement: predictability across the ARTs, flow of Capabilities (time, load, distribution), integration frequency, NFR and compliance evidence; say what each number means.
- Part 3, retrospective and problem-solving: pick the largest cross-ART problem, find its root cause (5 Whys, Pareto analysis), list countermeasures. A problem one ART can solve stays in that ART's Inspect and Adapt.
- Each improvement is an action naming `capability-refinement`: improvement items enter the Solution Train Backlog there.

### Pre-Plan, Coordinate and Deliver, Solution Demo (`event-record`)

- Pre-Plan aligns the ARTs before their PI Planning: the ready Capabilities in WSJF order, their Feature split per ART, cross-ART and supplier dependencies, integration points. Record the planning context each ART takes away.
- Coordinate and Deliver holds three syncs. Product Manager Sync: scope and priority issues raised by the ARTs. Architect Sync: emerging designs and trade-offs kept consistent without delaying the ARTs. RTE Sync: what the ARTs cannot resolve directly. Record what was raised, what was decided and by whom, not a status round.
- Solution Demo shows the integrated work of all ARTs and suppliers as objective evidence: each Capability against its acceptance criteria, NFR and compliance evidence, what was not integrated, and stakeholder feedback in their words.

### Solution Train Kanban (`kanban`)

- States: funnel, analyzing, ready, implementing, validating-on-staging, deploying-to-production, releasing, done.
- Render from each Capability's `status`; flag WIP over limit, blocked Capabilities and Capabilities that did not move since the last rendering.

### Gate decision (`gate-decision`)

- Record the human's words. One artifact, one decision, one record.
- A PI commitment quotes the business value and the confidence vote as the humans gave them.

## Evidence

A record cites committed artifacts by path. A number has its source. A human statement is quoted. What a worker replied is not evidence.

## Out of scope

The Solution Vision, the Solution Roadmap and Capabilities belong to `solution-manager`, the Solution Intent to `solution-architect`, supplier agreements to `procurement-manager`. An ART's plan belongs to `release-train-engineer`, portfolio matters to `value-management-officer`.
