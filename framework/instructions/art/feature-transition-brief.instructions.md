---
description: 'Workflow brief of feature-transition: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Feature transition (`feature-transition`)

Record the human's decision to move one business Feature to a new ART Kanban state, then re-render the ART Kanban.

- **Item:** `feature` at `portfolio/arts/<art-slug>/features/<feature-slug>/<feature-slug>.feature.md`, owned by `product-manager`.
- **Board:** `portfolio/arts/<art-slug>/art-kanban.md` (template `templates/kanbans/art-kanban.artifact-template.md`).
- **States:** funnel → analyzing → ready → implementing → validating-on-staging → deploying-to-production → releasing → done.

## Rules

- A Feature leaves `analyzing` only after it was challenged.
- `implementing` follows the PI commitment and sets `targetPi`.
- `done` follows release and the evaluation of the benefit hypothesis.

## After the run

On `ready`: `pi-planning`. On `implementing`: `story-refinement` with the team's Scrum Master.
