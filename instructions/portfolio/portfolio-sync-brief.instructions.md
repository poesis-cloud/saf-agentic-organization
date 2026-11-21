---
description: 'Workflow brief of portfolio-sync: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Portfolio Sync (`portfolio-sync`)

Inspect the flow of Epics and the portfolio's operations between Strategic Portfolio Reviews, and re-render the Portfolio Kanban.

- **Record:** `event-record` at `portfolio/events/<event-slug>.portfolio-sync.md` (template `templates/events/portfolio-sync.artifact-template.md`), with `event: portfolio-sync`.
- **Board:** `portfolio/portfolio-kanban.md` (template `templates/kanbans/portfolio-kanban.artifact-template.md`).

## Agenda

- Epics by state, WIP against limits, aged and blocked Epics.
- Dependencies and impediments across value streams.
- Backlog refinement: new Epics to capture, priorities to revisit, Epics to remove.
- Budget and guardrail signals worth a Strategic Portfolio Review.

## After the run

A backlog change is its own workflow: `epic-hypothesis`, `epic-transition`.
