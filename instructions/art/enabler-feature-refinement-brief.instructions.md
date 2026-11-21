---
description: 'Workflow brief of enabler-feature-refinement: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Enabler Feature refinement (`enabler-feature-refinement`)

Write or thicken one enabler Feature that extends the architectural runway or improves the delivery pipeline.

- **Main artifact:** `feature` at `portfolio/arts/<art-slug>/features/<feature-slug>/<feature-slug>.feature.md` (template `templates/art/feature.artifact-template.md`), owned by `system-architect`.
- **Challenge packets:** `portfolio/arts/<art-slug>/features/<feature-slug>/challenges/enabler-feature-refinement-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `software-engineer`, `platform-engineer`, `devops-engineer`, `site-reliability-engineer`, `observability-engineer`.

## Draft

- One enabler Feature per run, with `type: enabler` and its `enablerType`. Create it with `status: funnel`, or thicken it without changing its status.
- State the benefit as what it makes possible or faster for named business Features; write acceptance criteria that are demonstrable.
- Estimate WSJF so it competes fairly within the capacity allocated to enablers. Link the architecture decisions it implements.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Is the runway built just in time for the Features that need it?
- Can completion be demonstrated on a working system?

## Revise

Done when: `enablerType`, the Features enabled, acceptance criteria and WSJF are filled. Every packet of this run has its `challengeLedger` entry.

## Human gate

The ART's lead architect and Product Management decide whether the enabler is ready. Next: `feature-transition` to record the move; then `pi-planning`.
