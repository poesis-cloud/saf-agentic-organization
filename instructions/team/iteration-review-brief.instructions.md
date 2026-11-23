---
description: 'Workflow brief of iteration-review: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Generated: builds/model -->

# Iteration Review (`iteration-review`)

Inspect the iteration increment with stakeholders, assess progress toward the iteration goals and PI Objectives, and adjust the Team Backlog.

- **Record:** `event-record` at `portfolio/arts/<art-slug>/teams/<team-slug>/events/<event-slug>.iteration-review.md` (template `templates/events/iteration-review.artifact-template.md`), with `event: iteration-review`.

## Agenda

- Each Story demonstrated as a working, tested increment against its acceptance criteria.
- Stories not completed and why.
- Iteration goals met or missed; progress toward the PI Objectives.
- Feedback and the backlog adjustments it suggests.

## After the run

`story-transition` for Stories accepted; then `iteration-retrospective`.
