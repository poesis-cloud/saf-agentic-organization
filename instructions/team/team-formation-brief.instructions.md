---
description: 'Workflow brief of team-formation: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Generated: builds/model -->

# Team formation (`team-formation`)

Define or revise one Agile team: its mission, members, working agreements, Definition of Done and Kanban.

- **Main artifact:** `team-charter` at `portfolio/arts/<art-slug>/teams/<team-slug>/team-charter.md` (template `templates/team/team-charter.artifact-template.md`), owned by `scrum-master`.
- **Challenge packets:** `portfolio/arts/<art-slug>/teams/<team-slug>/challenges/team-formation-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `agile-coach`, `product-owner`, `quality-engineer`.

## Draft

- Read the ART canvas and its working agreements.
- Keep the team cross-functional and small (ten or fewer), with a Product Owner and a Scrum Master/Team Coach.
- Write a Definition of Done that includes the NFR checks, and Team Kanban states with WIP limits.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Can the team define, build, test and deliver without waiting on another team?
- Is every item of the Definition of Done checkable?

## Revise

Done when: Mission, roles, Definition of Done and Kanban states with WIP limits are filled. Every packet of this run has its `challengeLedger` entry.

## Human gate

The team's human lead decides whether the team works this way. Next: `team-gate-decision`; then `story-refinement`.
