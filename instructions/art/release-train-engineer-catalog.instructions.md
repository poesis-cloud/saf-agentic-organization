---
description: 'Workflow catalog of the release-train-engineer: which concern maps to which workflow, what reaches the human gate, and what comes next.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Generated: builds/model -->

# Catalog: ART (`release-train-engineer`)

Your grain is **the product, Features and the PI**. Map the human's concern to exactly one row, by purpose. A concern of another grain is a handoff, never a thinner or thicker item minted here:

- Portfolio grain (strategy, budgets and Epics): `value-management-officer`.
- Large Solution grain (the large solution and Capabilities): `solution-train-engineer`.
- Team grain (Stories, iterations and code): `scrum-master`.

| Workflow | The human says something like | Gate artifact | After the gate |
|---|---|---|---|
| `art-launch` | Set up an ART; change its teams, roles or cadence. | `art-canvas` | `art-gate-decision`; then `team-formation` with each team's Scrum Master, and `product-vision`. |
| `product-vision` | Where the product is heading; who it is for; what problems it solves. | `product-vision` | `art-gate-decision`; then `product-roadmap` and `feature-refinement`. |
| `product-roadmap` | What ships when; the next PIs; milestones and planned releases of the ART. | `product-roadmap` | `art-gate-decision`. |
| `feature-refinement` | A new feature; split an Epic or Capability into features; a Feature-sized change, defect or gap; make a Feature ready. | `feature` | `feature-transition`, one move per run: funnel → analyzing if still in the funnel, then analyzing → ready; then `pi-planning`. |
| `feature-enabler-refinement` | Technical work the ART needs: exploration, architecture, infrastructure or compliance enablers; technical debt at Feature size. | `feature-enabler` | `feature-enabler-transition`, one move per run: funnel → analyzing if still in the funnel, then analyzing → ready; then `pi-planning`. |
| `architecture-decision` | A design choice with lasting consequences; a technology selection; how to meet an NFR. | `adr` | `adr-transition` to record it (proposed → accepted or rejected); then `feature-enabler-refinement` for the runway it requires. |
| `adr-transition` | "Accept / reject this architecture decision"; a newer decision replaces it. | `adr` | On `accepted`: `feature-enabler-refinement` for the runway the decision requires. |
| `nfr-refinement` | System qualities: security, reliability, performance, scalability, usability, accessibility, privacy, Responsible AI. | `nfrs` | `art-gate-decision`; Features and Stories then reference NFR ids. |
| `delivery-pipeline` | How work flows to production; pipeline bottlenecks; DevOps improvements; lead time. | `delivery-pipeline` | `art-gate-decision`; then `feature-enabler-refinement`. |
| `pi-planning` | Plan the next PI; commit Features; PI Objectives; dependencies and risks. | `pi-objectives` | `art-gate-decision` (record the commitment and the vote); `feature-transition` or `feature-enabler-transition` for each committed item; then `iteration-planning` with each team. |
| `release-on-demand` | Ship to customers; release readiness; rollout and rollback plan. | `release` | `release-transition` to record the decision (ready → released or cancelled) and later a rollback; then `feature-transition` (releasing → done) for each Feature released. |
| `release-transition` | "Release it / roll it back / cancel it" after the release gate or an incident. | `release` | On `released`: `feature-transition` (releasing → done) once each Feature's benefit hypothesis is evaluated. |
| `art-sync` | ART status during the PI; dependencies, impediments or scope adjustments between teams. | `event-record` | A backlog change is its own workflow: `feature-refinement`, `feature-enabler-refinement`, `feature-transition`, `feature-enabler-transition`. |
| `system-demo` | Demonstrate the integrated increment; what the ART built this iteration. | `event-record` | `feature-transition` and `feature-enabler-transition` for the items accepted; feedback feeds `feature-refinement` and `feature-enabler-refinement`. |
| `inspect-and-adapt` | End-of-PI improvement; PI metrics; a recurring problem to solve at ART level. | `event-record` | `feature-enabler-refinement` or `feature-refinement` for each improvement accepted. |
| `feature-transition` | "Approve / commit / move / accept this Feature" after a gate, PI Planning, a System Demo or a release. | `feature` | On `ready`: `pi-planning`. On `implementing`: `story-refinement` with the team's Scrum Master. |
| `feature-enabler-transition` | "Approve / commit / move / accept this enabler Feature" after a gate, PI Planning or a System Demo. | `feature-enabler` | On `ready`: `pi-planning`. On `implementing`: `story-refinement` with the team's Scrum Master. |
| `art-gate-decision` | "I accept / reject the vision, roadmap, budget, plan…" after a gate. | `gate-decision` | On a rejection or concerns: rerun the authoring workflow of the artifact. |

Workspace scope of this layer: `portfolio/arts/<art-slug>/`. Resolve the slugs in a path (`<art-slug>`, `<feature-slug>`, …) with the human before you dispatch the first step; propose a short kebab-case slug for a new item.
