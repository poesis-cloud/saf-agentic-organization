---
description: 'Workflow catalog of the value-management-officer: which concern maps to which workflow, what reaches the human gate, and what comes next.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Catalog: Portfolio (`value-management-officer`)

Your grain is **strategy, budgets and Epics**. Map the human's concern to exactly one row, by purpose. A concern of another grain is a handoff, never a thinner or thicker item minted here:

- Large Solution grain (the large solution and Capabilities): `solution-train-engineer`.
- ART grain (the product, Features and the PI): `release-train-engineer`.
- Team grain (Stories, iterations and code): `scrum-master`.

| Workflow | The human says something like | Gate artifact | After the gate |
|---|---|---|---|
| `strategic-themes` | New or changed strategy, business objectives, OKRs for the portfolio. | `strategic-themes` | `portfolio-gate-decision` to record the decision; then `portfolio-vision` and `strategic-investment-planning`. |
| `portfolio-vision` | Where the portfolio is heading; portfolio canvas; future state. | `portfolio-vision` | `portfolio-gate-decision`; then `epic-hypothesis` for each Epic on the path and `portfolio-roadmap`. |
| `value-stream-definition` | Organize around value; identify a value stream; decide which ARTs or Solution Trains exist. | `value-stream` | `portfolio-gate-decision`; then `solution-train-launch` or `art-launch` with the train's orchestrator. |
| `epic-hypothesis` | A new big business initiative or idea; thicken an Epic in the funnel or under review. | `epic` | `epic-transition` to record the move (funnel → reviewing → analyzing); once analyzing, `lean-business-case`. |
| `epic-enabler-hypothesis` | Runway or platform work at portfolio size; an enabler Epic the Architecture Vision names; a replatforming, migration or compliance programme; thicken an enabler Epic in the funnel or under review. | `epic-enabler` | `epic-enabler-transition` to record the move (funnel → reviewing → analyzing); once analyzing, `epic-enabler-lean-business-case`. |
| `lean-business-case` | Business case, MVP definition, cost estimate, go/no-go for an Epic under analysis. | `lean-business-case` | `epic-transition` to record it (analyzing → ready on go; → done with resolution no-go otherwise). |
| `epic-enabler-lean-business-case` | Business case, MVP definition, cost estimate, go/no-go for an enabler Epic under analysis. | `lean-business-case` | `epic-enabler-transition` to record it (analyzing → ready on go; → done with resolution no-go otherwise). |
| `epic-mvp-evaluation` | MVP results are in; pivot or persevere; stop an Epic. | `epic` | `epic-transition` to record it; a pivot starts a new `epic-hypothesis`. |
| `epic-enabler-mvp-evaluation` | Enabler MVP results are in; is the runway used; pivot or persevere; stop an enabler Epic. | `epic-enabler` | `epic-enabler-transition` to record it; a pivot starts a new `epic-enabler-hypothesis`. |
| `portfolio-roadmap` | Multi-year plan of the portfolio; when Epics land; portfolio milestones. | `portfolio-roadmap` | `portfolio-gate-decision`. |
| `strategic-investment-planning` | Budgets per value stream; funding; guardrails; capacity allocation; investment horizons. | `lean-budgets` | `portfolio-gate-decision`; value streams prepare during the current PI and apply the change at the next one. |
| `architecture-vision` | Technology strategy; target architecture; portfolio-level runway; which enabler Epics are needed. | `architecture-vision` | `portfolio-gate-decision`; then `epic-enabler-hypothesis` for each enabler Epic. |
| `epic-transition` | "Approve / reject / move / stop this Epic" after a gate. | `epic` | On `analyzing`: `lean-business-case`. On `ready`: the trains pull the Epic (`capability-refinement`, `feature-refinement` and their enabler siblings). |
| `epic-enabler-transition` | "Approve / reject / move / stop this enabler Epic" after a gate. | `epic-enabler` | On `analyzing`: `epic-enabler-lean-business-case`. On `ready`: the trains pull it (`capability-enabler-refinement`, `feature-enabler-refinement`). |
| `portfolio-sync` | Portfolio status; where the Epics are; impediments and dependencies across value streams. | `event-record` | A backlog change is its own workflow: `epic-hypothesis`, `epic-enabler-hypothesis`, `epic-transition`, `epic-enabler-transition`. |
| `strategic-portfolio-review` | Is the portfolio on strategy; keep, pivot or stop investments; review KPIs and OKRs. | `event-record` | Each decision is carried by its workflow: `strategic-themes`, `strategic-investment-planning`, `epic-transition`, `epic-enabler-transition`, `portfolio-roadmap`. |
| `portfolio-gate-decision` | "I accept / reject the vision, roadmap, budget, plan…" after a gate. | `gate-decision` | On a rejection or concerns: rerun the authoring workflow of the artifact. |

Workspace scope of this layer: `portfolio/`. Resolve the slugs in a path (`<art-slug>`, `<feature-slug>`, …) with the human before you dispatch the first step; propose a short kebab-case slug for a new item.
