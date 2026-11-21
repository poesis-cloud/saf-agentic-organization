---
description: 'Workflow brief of nfr-refinement: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# NFR refinement (`nfr-refinement`)

Create or revise the ART's register of nonfunctional requirements: each one bounded, measurable and verifiable.

- **Main artifact:** `nfrs` at `portfolio/arts/<art-slug>/nfrs.md` (template `templates/art/nfrs.artifact-template.md`), owned by `system-architect`.
- **Challenge packets:** `portfolio/arts/<art-slug>/challenges/nfr-refinement-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `site-reliability-engineer`, `observability-engineer`, `security-expert`, `quality-engineer`, `accessibility-specialist`, `ai-engineer`.

## Draft

- Read the Product Vision, the Solution Intent when there is one, and the current register.
- Give each NFR an id, a bounded statement, a measurable threshold and a verification (test, monitor or audit) with the Definition of Done that carries it.
- Keep the register small: an NFR that cannot be verified, or that nobody would pay for, does not belong.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Can each NFR be tested or monitored continuously?
- Which NFRs conflict, and is the trade-off economic?

## Revise

Done when: Every NFR has a measure and a verification; trade-offs are stated. Every packet of this run has its `challengeLedger` entry.

## Human gate

The ART's lead architect and Business Owners decide whether these qualities bind the backlog. Next: `art-gate-decision`; Features and Stories then reference NFR ids.
