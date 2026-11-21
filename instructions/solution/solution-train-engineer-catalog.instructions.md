---
description: 'Workflow catalog of the solution-train-engineer: which concern maps to which workflow, what reaches the human gate, and what comes next.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Catalog: Large Solution (`solution-train-engineer`)

Your grain is **the large solution and Capabilities**. Map the human's concern to exactly one row, by purpose. A concern of another grain is a handoff, never a thinner or thicker item minted here:

- Portfolio grain (strategy, budgets and Epics): `value-management-officer`.
- ART grain (the product, Features and the PI): `release-train-engineer`.
- Team grain (Stories, iterations and code): `scrum-master`.

| Workflow | The human says something like | Gate artifact | After the gate |
|---|---|---|---|
| `solution-train-launch` | Set up a Solution Train; change its ARTs, suppliers, roles or cadence. | `solution-train-canvas` | `solution-gate-decision`; then `solution-vision` and `solution-intent`. |
| `solution-vision` | What the large solution should become; who it serves; solution context. | `solution-vision` | `solution-gate-decision`; then `solution-roadmap` and `capability-refinement`. |
| `solution-roadmap` | When capabilities land; solution milestones; multi-year plan of the solution. | `solution-roadmap` | `solution-gate-decision`. |
| `solution-intent` | Solution-level requirements and design; interfaces between ARTs; compliance evidence; what is fixed and what is still open. | `solution-intent` | `solution-gate-decision`; ARTs take the NFRs into `nfr-refinement`. |
| `capability-refinement` | A new capability; split an Epic into capabilities; an enabler capability; make a capability ready. | `capability` | `capability-transition` to record the move; then `pre-plan`. |
| `supplier-engagement` | Onboard or change a supplier; contract terms for a component or service. | `supplier-agreement` | `solution-gate-decision`. This artifact is a working agreement, not the signed contract; a later run records `active` once the humans signed. |
| `pre-plan` | Prepare the next PI across ARTs; which capabilities go to which ART. | `event-record` | Each ART runs `pi-planning` with its Release Train Engineer; then `solution-train-pi-planning`. |
| `solution-train-pi-planning` | The Solution Train's plan and objectives for the PI, after the ARTs planned. | `pi-objectives` | `solution-gate-decision` (record the commitment); then `coordinate-and-deliver` during the PI. |
| `coordinate-and-deliver` | Cross-ART status during the PI; dependencies, design trade-offs or impediments between ARTs. | `event-record` | A backlog change is its own workflow: `capability-refinement`, `capability-transition`. |
| `solution-demo` | Demonstrate the integrated solution at the end of the PI. | `event-record` | `capability-transition` for capabilities accepted; feedback feeds `capability-refinement` and the portfolio's investment decisions. |
| `solution-train-inspect-and-adapt` | End-of-PI improvement for the Solution Train; cross-ART problems to solve. | `event-record` | `capability-refinement` for each improvement accepted. |
| `capability-transition` | "Approve / move / accept this capability" after a gate or a Solution Demo. | `capability` | On `ready`: `pre-plan`. |
| `solution-gate-decision` | "I accept / reject the vision, roadmap, budget, plan…" after a gate. | `gate-decision` | On a rejection or concerns: rerun the authoring workflow of the artifact. |

Workspace scope of this layer: `portfolio/solution-trains/<solution-train-slug>/`. Resolve the slugs in a path (`<art-slug>`, `<feature-slug>`, …) with the human before you dispatch the first step; propose a short kebab-case slug for a new item.
