---
description: 'Workflow brief of epic-transition: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Epic transition (`epic-transition`)

Record the human's decision to move one Epic to a new Portfolio Kanban state, then re-render the Portfolio Kanban.

- **Item:** `epic` at `portfolio/epics/<epic-slug>/<epic-slug>.epic.md`, owned by `epic-owner`.
- **Board:** `portfolio/portfolio-kanban.md` (template `templates/kanbans/portfolio-kanban.artifact-template.md`).
- **States:** funnel → reviewing → analyzing → ready → implementing (mvp, then persevere) → done.

## Rules

- `ready` and `implementing` need a Lean Business Case recommending `go`.
- Entering `implementing` sets `implementationStage: mvp`; a persevere decision sets `persevere`.
- `done` sets `resolution`: delivered, no-go, pivoted or stopped.

## After the run

On `analyzing`: `lean-business-case`. On `ready`: the trains pull the Epic (`capability-refinement`, `feature-refinement`).
