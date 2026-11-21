---
description: 'Workflow brief of team-gate-decision: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Team gate decision (`team-gate-decision`)

Record the human's decision on a challenged team-level artifact that is not a backlog item (backlog items move with their transition workflow).

- **Record:** `gate-decision` at `portfolio/arts/<art-slug>/teams/<team-slug>/decisions/<decision-slug>.gate-decision.md` (template `templates/shared/gate-decision.artifact-template.md`).
- Name the file `<target-file-stem>-<YYYY-MM-DD>`, for example `product-vision-2026-11-21.gate-decision.md`.

## Rules

- One decision on one artifact per run. Backlog items (Epic, Capability, Feature, Story) do not come here: their decision is a state change in their `*-transition` workflow.
- `accepted` and `accepted-with-concerns` are refused by the harness while no challenge packet targets the artifact: no acceptance without challenge.

## After the run

On a rejection or concerns: rerun the authoring workflow of the artifact.
