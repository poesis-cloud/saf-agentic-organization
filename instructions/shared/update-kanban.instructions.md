---
description: 'Pattern of a kanban step: the orchestrator re-renders the board from the items it lists.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Re-render the Kanban board

- **Source of truth.** Read the `status` and `blocked` fields of every item of the board's backlog (the folders under the board's scope). Read frontmatter only.
- **Render.** Rewrite `columns` in flow order with the item paths per state; set `updated`; keep the existing WIP limits. A new board starts from the template the brief names.
- **Flow notes.** Flag a state over its WIP limit, blocked items and items that did not move since the last rendering.
- **Never** change an item or list one that does not exist.
- **Outcome:** `revised` when the board changed, `confirmed` when it did not.
