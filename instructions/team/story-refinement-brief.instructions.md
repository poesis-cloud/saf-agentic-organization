---
description: 'Workflow brief of story-refinement: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Generated: builds/model -->

# Story refinement (`story-refinement`)

Write or thicken one Story so it is ready for Iteration Planning: user voice, acceptance criteria and an estimate.

- **Main artifact:** `story` at `portfolio/arts/<art-slug>/teams/<team-slug>/stories/<story-slug>/<story-slug>.story.md` (template `templates/team/story.artifact-template.md`), owned by `product-owner`.
- **Challenge packets:** `portfolio/arts/<art-slug>/teams/<team-slug>/stories/<story-slug>/challenges/story-refinement-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `software-engineer`, `quality-engineer`, `security-expert`, `ux-designer`.

## Draft

- One Story per run, a vertical slice that fits in an iteration. Create it with `status: backlog`, or thicken it without changing its status.
- User stories use the user-voice form; an enabler Story (a spike is an exploration enabler) says what must be learned or built.
- Write Given/When/Then acceptance criteria and the NFR ids that apply. Set `parent` to the Feature or enabler Feature it splits from. Leave `estimate` to the team's challenge.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Is it independent, negotiable, valuable, estimable, small and testable?
- Does each acceptance criterion describe an observable outcome?

## Revise

Done when: The Story statement and acceptance criteria are filled; `estimate` is set from the Software Engineer's packet. Every packet of this run has its `challengeLedger` entry.

## Human gate

The Product Owner (human) decides whether the Story is ready. Next: `story-transition` to record the move; then `iteration-planning`.
