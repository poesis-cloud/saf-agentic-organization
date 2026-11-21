---
description: 'Workflow brief of art-launch: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# ART launch (`art-launch`)

Define or revise one Agile Release Train: its mission, teams, roles and PI cadence.

- **Main artifact:** `art-canvas` at `portfolio/arts/<art-slug>/art-canvas.md` (template `templates/art/art-canvas.artifact-template.md`), owned by `release-train-engineer`.
- **Challenge packets:** `portfolio/arts/<art-slug>/challenges/art-launch-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `agile-coach`, `system-architect`, `product-manager`.

## Draft

- Read the value stream definition and, when the ART belongs to one, the Solution Train canvas.
- Design teams that can deliver value with few dependencies (5 to 15 teams, each ten people or fewer) and give each a type.
- Set the PI calendar: iterations, the IP iteration, PI Planning, System Demo, Inspect and Adapt.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Can each team deliver a vertical slice, or does every Feature cross all teams?
- Are Product Management, System Architect and Business Owners named?

## Revise

Done when: Mission, teams with their type, roles and the PI calendar are filled. Every packet of this run has its `challengeLedger` entry.

## Human gate

The ART's Business Owners decide whether to launch or change the train this way. Next: `art-gate-decision`; then `team-formation` with each team's Scrum Master, and `product-vision`.
