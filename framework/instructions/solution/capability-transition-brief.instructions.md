---
description: 'Workflow brief of capability-transition: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Capability transition (`capability-transition`)

Record the human's decision to move one Capability to a new Solution Train Kanban state, then re-render the Solution Train Kanban.

- **Item:** `capability` at `portfolio/solution-trains/<solution-train-slug>/capabilities/<capability-slug>/<capability-slug>.capability.md`, owned by `solution-manager`.
- **Board:** `portfolio/solution-trains/<solution-train-slug>/solution-train-kanban.md` (template `templates/kanbans/solution-train-kanban.artifact-template.md`).
- **States:** funnel → analyzing → ready → implementing → validating-on-staging → deploying-to-production → releasing → done.

## Rules

- A Capability leaves `analyzing` only after it was challenged.
- `implementing` follows the PI commitment; `done` follows acceptance at a Solution Demo.

## After the run

On `ready`: `pre-plan`.
