---
description: 'Workflow brief of epic-enabler-transition: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Generated: builds/model -->

# Enabler Epic transition (`epic-enabler-transition`)

Record the human's decision to move one enabler Epic to a new Portfolio Kanban state, then re-render the Portfolio Kanban.

- **Item:** `epic-enabler` at `portfolio/epics/<epic-slug>/<epic-slug>.epic-enabler.md`, owned by `enterprise-architect`.
- **Board:** `portfolio/portfolio-kanban.md` (template `templates/kanbans/portfolio-kanban.artifact-template.md`).
- **States:** funnel → reviewing → analyzing → ready → implementing (mvp, then persevere) → done.

## Rules

- `ready` and `implementing` need a Lean Business Case recommending `go`.
- Entering `implementing` sets `implementationStage: mvp`; a persevere decision sets `persevere`.
- `done` sets `resolution`: delivered, no-go, pivoted or stopped; before `implementing`, `done` can follow any state (no-go or stopped).

## After the run

On `analyzing`: `epic-enabler-lean-business-case`. On `ready`: the trains pull it (`capability-enabler-refinement`, `feature-enabler-refinement`).
