---
description: 'Workflow brief of solution-train-inspect-and-adapt: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Solution Train Inspect and Adapt (`solution-train-inspect-and-adapt`)

Evaluate the integrated solution and the train's way of working at the end of the PI, and derive improvement backlog items.

- **Main artifact:** `event-record` at `portfolio/solution-trains/<solution-train-slug>/events/<event-slug>.inspect-and-adapt.md` (template `templates/events/inspect-and-adapt.artifact-template.md`), owned by `solution-train-engineer`.
- **Challenge packets:** `portfolio/solution-trains/<solution-train-slug>/challenges/solution-train-inspect-and-adapt-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `agile-coach`, `data-analyst`.

## Draft

- Read the Solution Demo record, the PI Objectives with actual business value, and the ARTs' Inspect and Adapt records. Set `event: inspect-and-adapt`.
- Three parts: the demo result, a quantitative and qualitative measurement review, then a retrospective and problem-solving analysis of the largest cross-ART problem.
- State each improvement as an action that names the workflow which will write the backlog item.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Do the measures support the conclusions?
- Does the root cause analysis reach a cause the train can act on?

## Revise

Done when: Each improvement action has an owner and a carrying workflow. Every packet of this run has its `challengeLedger` entry.

## Human gate

The train's stakeholders decide which improvements enter the Solution Train Backlog. Next: `capability-refinement` or `capability-enabler-refinement` for each improvement accepted.
