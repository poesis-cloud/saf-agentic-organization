---
description: 'Workflow brief of inspect-and-adapt: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Inspect and Adapt (`inspect-and-adapt`)

Evaluate the PI's result and the ART's way of working at the end of the PI, and derive improvement backlog items.

- **Main artifact:** `event-record` at `portfolio/arts/<art-slug>/events/<event-slug>.inspect-and-adapt.md` (template `templates/events/inspect-and-adapt.artifact-template.md`), owned by `release-train-engineer`.
- **Challenge packets:** `portfolio/arts/<art-slug>/challenges/inspect-and-adapt-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `agile-coach`, `data-analyst`.

## Draft

- Read the PI Objectives with actual business value, the System Demo records, the Kanban and the `friction` notes of the PI's artifacts. Set `event: inspect-and-adapt`.
- Three parts: the PI System Demo result, a quantitative and qualitative measurement review (predictability, flow), then a retrospective and problem-solving analysis of the largest problem.
- State each improvement as an action that names the workflow which will write the backlog item.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Do the measures support the conclusions?
- Does the root cause analysis reach a cause the ART can act on?

## Revise

Done when: Each improvement action has an owner and a carrying workflow. Every packet of this run has its `challengeLedger` entry.

## Human gate

The ART's stakeholders decide which improvements enter the ART Backlog. Next: `enabler-feature-refinement` or `feature-refinement` for each improvement accepted.
