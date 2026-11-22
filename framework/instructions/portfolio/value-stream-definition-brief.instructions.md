---
description: 'Workflow brief of value-stream-definition: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Value stream definition (`value-stream-definition`)

Define one development value stream: the operational value streams it supports, its solutions and customers, the trains that realize it, and its KPIs.

- **Main artifact:** `value-stream` at `portfolio/value-streams/<value-stream-slug>/<value-stream-slug>.value-stream.md` (template `templates/portfolio/value-stream.artifact-template.md`), owned by `portfolio-manager`.
- **Challenge packets:** `portfolio/value-streams/<value-stream-slug>/challenges/value-stream-definition-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `business-analyst`, `enterprise-architect`, `agile-coach`.

## Draft

- Start from the operational value stream: who is served and what triggers the flow.
- Name the solutions, then the people needed, then trains sized to deliver with few cross-train dependencies (an ART is 50 to 125 people).
- Give four to seven KPIs tied to the Strategic Themes.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Can the trains named deliver end to end, or do hand-offs to other value streams remain?
- Are the KPIs outcomes of the value stream rather than activity counts?

## Revise

Done when: Trains and KPIs are named; known cross-value-stream dependencies are listed. Every packet of this run has its `challengeLedger` entry.

## Human gate

Portfolio Leadership decides whether to organize and fund the value stream this way. Next: `portfolio-gate-decision`; then `solution-train-launch` or `art-launch` with the train's orchestrator.
