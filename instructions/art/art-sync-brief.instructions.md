---
description: 'Workflow brief of art-sync: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# ART Sync (`art-sync`)

Inspect the ART's progress toward its PI Objectives (Coach Sync and PO Sync combined), handle dependencies and impediments, and re-render the ART Kanban.

- **Record:** `event-record` at `portfolio/arts/<art-slug>/events/<event-slug>.art-sync.md` (template `templates/events/art-sync.artifact-template.md`), with `event: art-sync`.
- **Board:** `portfolio/arts/<art-slug>/art-kanban.md` (template `templates/kanbans/art-kanban.artifact-template.md`).

## Agenda

- Coach Sync: progress, dependencies and impediments across teams.
- PO Sync: progress toward the PI Objectives and scope adjustments.
- Risks to revisit (ROAM).
- Decisions and actions, each with its owner.

## After the run

A backlog change is its own workflow: `feature-refinement`, `feature-enabler-refinement`, `feature-transition`, `feature-enabler-transition`.
