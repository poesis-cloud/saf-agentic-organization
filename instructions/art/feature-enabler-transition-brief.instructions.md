---
description: 'Workflow brief of feature-enabler-transition: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Enabler Feature transition (`feature-enabler-transition`)

Record the human's decision to move one enabler Feature to a new ART Kanban state, then re-render the ART Kanban.

- **Item:** `feature-enabler` at `portfolio/arts/<art-slug>/features/<feature-slug>/<feature-slug>.feature-enabler.md`, owned by `system-architect`.
- **Board:** `portfolio/arts/<art-slug>/art-kanban.md` (template `templates/kanbans/art-kanban.artifact-template.md`).
- **States:** funnel → analyzing → ready → implementing → validating-on-staging → deploying-to-production → releasing → done.

## Rules

- An enabler Feature leaves `analyzing` only after it was challenged.
- `implementing` follows the PI commitment and sets `targetPi`.
- `done` follows its demonstration on a working system and the evaluation of what it enables.

## After the run

On `ready`: `pi-planning`. On `implementing`: `story-refinement` with the team's Scrum Master.
