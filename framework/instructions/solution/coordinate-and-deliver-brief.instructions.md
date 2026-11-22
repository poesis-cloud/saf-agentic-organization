---
description: 'Workflow brief of coordinate-and-deliver: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Coordinate and Deliver (`coordinate-and-deliver`)

Keep the ARTs and suppliers aligned during the PI (Product Manager Sync, Architect Sync, RTE Sync) and re-render the Solution Train Kanban.

- **Record:** `event-record` at `portfolio/solution-trains/<solution-train-slug>/events/<event-slug>.coordinate-and-deliver.md` (template `templates/events/coordinate-and-deliver.artifact-template.md`), with `event: coordinate-and-deliver`.
- **Board:** `portfolio/solution-trains/<solution-train-slug>/solution-train-kanban.md` (template `templates/kanbans/solution-train-kanban.artifact-template.md`).

## Agenda

- Product Manager Sync: scope and priority issues raised by the ARTs.
- Architect Sync: emerging designs and trade-offs kept consistent across the train.
- RTE Sync: progress, dependencies and impediments the ARTs cannot resolve alone.
- Decisions and actions, each with its owner.

## After the run

A backlog change is its own workflow: `capability-refinement`, `capability-enabler-refinement`, `capability-transition`, `capability-enabler-transition`.
