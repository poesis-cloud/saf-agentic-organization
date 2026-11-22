---
description: 'Workflow brief of architecture-vision: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Generated: builds/model -->

# Architecture Vision (`architecture-vision`)

Establish or revise the portfolio's technology vision, strategy and roadmap, and the architectural runway it needs.

- **Main artifact:** `architecture-vision` at `portfolio/architecture-vision.md` (template `templates/portfolio/architecture-vision.artifact-template.md`), owned by `enterprise-architect`.
- **Challenge packets:** `portfolio/challenges/architecture-vision-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `solution-architect`, `security-expert`, `platform-engineer`, `data-engineer`, `finops-engineer`.

## Draft

- Read the Strategic Themes, Portfolio Vision and the Epics.
- Describe intentional architecture and a few principles; leave room for emergent design in the trains.
- Name the enabler Epics the runway needs and list those that exist in `enablerEpics`; you write each one in `epic-enabler-hypothesis`, not here.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Is the runway just enough for the near-term Epics, or built far ahead of need?
- Which decision must be taken now, and which can wait for learning?

## Revise

Done when: Target, principles and the ordered runway are stated; each enabler Epic is named by intent. Every packet of this run has its `challengeLedger` entry.

## Human gate

Portfolio Leadership and the lead architects decide whether this is the technical direction. Next: `portfolio-gate-decision`; then `epic-enabler-hypothesis` for each enabler Epic.
