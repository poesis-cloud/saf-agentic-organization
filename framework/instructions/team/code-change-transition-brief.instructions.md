---
description: 'Workflow brief of code-change-transition: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Code change transition (`code-change-transition`)

Record the human reviewer's decision on one code change as a state change.

- **Item:** `code-change` at `portfolio/arts/<art-slug>/teams/<team-slug>/stories/<story-slug>/<story-slug>.code-change.md`, owned by `software-engineer`.
- **States:** ready-for-review → changes-requested or approved → merged.

## Rules

- `approved` and `merged` need a challenged change; `merged` follows `approved` and the human's merge.
- `changes-requested` sends the Story back to `story-implementation`, which sets `ready-for-review` again.

## After the run

On `merged`: `story-transition` (in-review → accepted).
