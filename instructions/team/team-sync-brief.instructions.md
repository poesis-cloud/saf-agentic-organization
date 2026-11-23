---
description: 'Workflow brief of team-sync: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Generated: builds/model -->

# Team Sync (`team-sync`)

Inspect progress toward the iteration goals, adjust the plan for the coming day, and re-render the Team Kanban.

- **Record:** `event-record` at `portfolio/arts/<art-slug>/teams/<team-slug>/events/<event-slug>.team-sync.md` (template `templates/events/team-sync.artifact-template.md`), with `event: team-sync`.
- **Board:** `portfolio/arts/<art-slug>/teams/<team-slug>/team-kanban.md` (template `templates/kanbans/team-kanban.artifact-template.md`).

## Agenda

- Progress toward each iteration goal.
- Stories by state, WIP against limits, blocked Stories.
- Impediments: next step or escalation for each.
- Items for a 'meet after', not solved here.

## After the run

A backlog change is its own workflow: `story-refinement`, `story-transition`.
