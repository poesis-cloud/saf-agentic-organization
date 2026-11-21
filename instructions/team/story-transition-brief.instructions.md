---
description: 'Workflow brief of story-transition: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Story transition (`story-transition`)

Record the human's decision to move one Story to a new Team Kanban state, then re-render the Team Kanban.

- **Item:** `story` at `portfolio/arts/<art-slug>/teams/<team-slug>/stories/<story-slug>/<story-slug>.story.md`, owned by `product-owner`.
- **Board:** `portfolio/arts/<art-slug>/teams/<team-slug>/team-kanban.md` (template `templates/kanbans/team-kanban.artifact-template.md`).
- **States:** backlog → ready → in-progress → in-review → accepted.

## Rules

- A Story leaves `backlog` only after it was challenged.
- `in-progress` sets `iteration`.
- `accepted` means the acceptance criteria and the Definition of Done are met and the Story's code change, when it has one, is `merged`.

## After the run

On `ready`: `iteration-planning`. On `in-progress`: `story-implementation`.
