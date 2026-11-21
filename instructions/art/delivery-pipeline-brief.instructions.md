---
description: 'Workflow brief of delivery-pipeline: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Continuous Delivery Pipeline (`delivery-pipeline`)

Map the ART's Continuous Delivery Pipeline from ideation to on-demand release, find its bottlenecks and propose the enablers that remove them.

- **Main artifact:** `delivery-pipeline` at `portfolio/arts/<art-slug>/delivery-pipeline.md` (template `templates/art/delivery-pipeline.artifact-template.md`), owned by `devops-engineer`.
- **Challenge packets:** `portfolio/arts/<art-slug>/challenges/delivery-pipeline-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `platform-engineer`, `security-expert`, `quality-engineer`, `site-reliability-engineer`, `finops-engineer`.

## Draft

- Map what actually happens today, step by step, with lead time, process time and percent complete and accurate.
- Cover the four aspects: Continuous Exploration, Continuous Integration (Develop, Build, Test end-to-end, Stage), Continuous Deployment (Deploy, Verify, Monitor, Respond), Release on Demand.
- Name the largest delays and the enabler Features that would remove them; they are written in `enabler-feature-refinement`.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Where does work wait the longest, and is that where the improvement is aimed?
- Which quality, security or compliance check is still manual?

## Revise

Done when: The four aspects are mapped; the top bottlenecks each have a proposed enabler. Every packet of this run has its `challengeLedger` entry.

## Human gate

The ART's leaders decide which pipeline improvements to fund. Next: `art-gate-decision`; then `enabler-feature-refinement`.
