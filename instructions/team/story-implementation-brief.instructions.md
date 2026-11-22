---
description: 'Workflow brief of story-implementation: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Generated: builds/model -->

# Story implementation (`story-implementation`)

Implement one ready Story test-first in its code repository and record the change with its evidence; experts review it before the human merges.

- **Main artifact:** `code-change` at `portfolio/arts/<art-slug>/teams/<team-slug>/stories/<story-slug>/<story-slug>.code-change.md` (template `templates/team/code-change.artifact-template.md`), owned by `software-engineer`.
- **Challenge packets:** `portfolio/arts/<art-slug>/teams/<team-slug>/stories/<story-slug>/challenges/story-implementation-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `quality-engineer`, `security-expert`, `observability-engineer`, `database-administrator`, `accessibility-specialist`.

## Draft

- One Story per run. Read the Story, its Feature, the team's Definition of Done and the architecture decisions that apply.
- Work test-first in the code repository on a branch; the code lives there, not in the workspace. Never merge.
- Record the change: repository, branch, pull request, summary, the tests and their result, the Definition of Done checked item by item. Set `status: ready-for-review`.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Do the tests pin down each acceptance criterion, and do they pass?
- Is the change the smallest one that satisfies the Story?

## Revise

Done when: Review findings are fixed in the code or answered; tests pass; `status` is `ready-for-review`. Every packet of this run has its `challengeLedger` entry.

## Human gate

The human reviewer approves and merges the pull request. Next: `code-change-transition` to record the reviewer's decision (approved, then merged); then `story-transition` (in-review → accepted, by the Product Owner).
