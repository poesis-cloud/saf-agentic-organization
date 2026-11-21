---
description: 'Workflow brief of iteration-planning: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Iteration Planning (`iteration-planning`)

Plan one iteration: the iteration goals, the Stories selected and the capacity behind them.

- **Main artifact:** `iteration-plan` at `portfolio/arts/<art-slug>/teams/<team-slug>/iterations/<iteration-slug>/iteration-plan.md` (template `templates/team/iteration-plan.artifact-template.md`), owned by `scrum-master`.
- **Challenge packets:** `portfolio/arts/<art-slug>/teams/<team-slug>/iterations/<iteration-slug>/challenges/iteration-planning-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `product-owner`, `software-engineer`, `quality-engineer`.

## Draft

- Read the team charter, the ready Stories in priority order, the PI Objectives and the last iteration's review.
- Select Stories within capacity, then summarize them as iteration goals aligned to the PI Objectives.
- The commitment is to the goals, not to the Stories.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Is the load within capacity, given past velocity?
- Do the goals still make sense if one Story slips?

## Revise

Done when: Goals, selected Stories, capacity and load are filled. Every packet of this run has its `challengeLedger` entry.

## Human gate

The team and the business commit to the iteration goals. Next: `team-gate-decision` (record the commitment); then `story-implementation` per Story.
