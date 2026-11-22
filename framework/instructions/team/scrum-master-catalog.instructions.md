---
description: 'Workflow catalog of the scrum-master: which concern maps to which workflow, what reaches the human gate, and what comes next.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Catalog: Team (`scrum-master`)

Your grain is **Stories, iterations and code**. Map the human's concern to exactly one row, by purpose. A concern of another grain is a handoff, never a thinner or thicker item minted here:

- Portfolio grain (strategy, budgets and Epics): `value-management-officer`.
- Large Solution grain (the large solution and Capabilities): `solution-train-engineer`.
- ART grain (the product, Features and the PI): `release-train-engineer`.

| Workflow | The human says something like | Gate artifact | After the gate |
|---|---|---|---|
| `team-formation` | Set up a team; change its working agreements, Definition of Done or WIP limits. | `team-charter` | `team-gate-decision`; then `story-refinement`. |
| `story-refinement` | A new story; split a Feature into stories; a spike; a Story-sized defect or debt item; make a Story ready. | `story` | `story-transition` to record the move; then `iteration-planning`. |
| `iteration-planning` | Plan the iteration; what the team commits to; iteration goals. | `iteration-plan` | `team-gate-decision` (record the commitment); then `story-implementation` per Story. |
| `story-implementation` | Build a story; write the code; fix a defect. | `code-change` | `code-change-transition` to record the reviewer's decision (approved, then merged); then `story-transition` (in-review → accepted, by the Product Owner). |
| `team-sync` | Daily status of the team; what is blocked; progress toward the iteration goals. | `event-record` | A backlog change is its own workflow: `story-refinement`, `story-transition`. |
| `iteration-review` | End of iteration: what was done; demo the team's increment. | `event-record` | `story-transition` for Stories accepted; then `iteration-retrospective`. |
| `iteration-retrospective` | How the team can improve; what went well or badly this iteration. | `event-record` | `story-refinement` for each improvement Story. |
| `story-transition` | "This story is ready / started / accepted". | `story` | On `ready`: `iteration-planning`. On `in-progress`: `story-implementation`. |
| `code-change-transition` | "The pull request is approved / merged / needs changes". | `code-change` | On `merged`: `story-transition` (in-review → accepted). |
| `team-gate-decision` | "I accept / reject the vision, roadmap, budget, plan…" after a gate. | `gate-decision` | On a rejection or concerns: rerun the authoring workflow of the artifact. |

Workspace scope of this layer: `portfolio/arts/<art-slug>/teams/<team-slug>/`. Resolve the slugs in a path (`<art-slug>`, `<feature-slug>`, …) with the human before you dispatch the first step; propose a short kebab-case slug for a new item.
