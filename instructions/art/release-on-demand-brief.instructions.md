---
description: 'Workflow brief of release-on-demand: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Generated: builds/model -->

# Release on Demand (`release-on-demand`)

Plan one release and assemble its readiness evidence: what is made available to which customers, how, and how its outcome will be measured.

- **Main artifact:** `release` at `portfolio/arts/<art-slug>/releases/<release-slug>/<release-slug>.release.md` (template `templates/art/release.artifact-template.md`), owned by `release-manager`.
- **Challenge packets:** `portfolio/arts/<art-slug>/releases/<release-slug>/challenges/release-on-demand-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `site-reliability-engineer`, `observability-engineer`, `security-expert`, `quality-engineer`, `technical-writer`, `product-marketing-manager`.

## Draft

- Read the Features released, their acceptance evidence, the NFR register and the pipeline map.
- Describe how release is decoupled from deployment, the audience, the rollout steps and a tested rollback.
- Link the evidence, do not restate it. Say which outcome will be measured for each Feature's benefit hypothesis.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Is the rollback tested, and who decides to trigger it?
- Can the benefit hypothesis be measured after release?

## Revise

Done when: Scope, strategy, evidence links, rollout and rollback are filled; `status` is `ready` or says what is missing. Every packet of this run has its `challengeLedger` entry.

## Human gate

Product Management's human lead and the Business Owners decide to release. Next: `release-transition` to record the decision (ready → released or cancelled) and later a rollback; then `feature-transition` (releasing → done) for each Feature released.
