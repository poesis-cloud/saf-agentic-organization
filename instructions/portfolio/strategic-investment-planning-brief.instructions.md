---
description: 'Workflow brief of strategic-investment-planning: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Generated: builds/model -->

# Strategic Investment Planning (`strategic-investment-planning`)

Establish or update Lean value stream budgets and their guardrails for the coming budget period (formerly Participatory Budgeting).

- **Main artifact:** `lean-budgets` at `portfolio/lean-budgets.md` (template `templates/portfolio/lean-budgets.artifact-template.md`), owned by `portfolio-manager`.
- **Challenge packets:** `portfolio/challenges/strategic-investment-planning-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `financial-controller`, `enterprise-architect`, `business-owner`, `finops-engineer`.

## Draft

- Read the Strategic Themes, Portfolio Vision, value streams, the Epics above the threshold and any forum results the human provides.
- Per value stream: Baseline Solution Investments first, then Proposed Solution Initiatives, budgeting only the cost expected in the period.
- Apply the four guardrails and record the forum insights. Forum results inform the allocation; Portfolio Leadership finalizes it.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Do the allocations respect the guardrails, and does the sum match the total budget?
- Is any initiative funded beyond its MVP before its hypothesis is proven?

## Revise

Done when: Every value stream has a budget with its reasons; the four guardrails are stated as applied. Every packet of this run has its `challengeLedger` entry.

## Human gate

Portfolio Leadership finalizes the portfolio budget. Next: `portfolio-gate-decision`; value streams prepare during the current PI and apply the change at the next one.
