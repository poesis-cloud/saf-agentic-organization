---
description: 'Workflow brief of portfolio-gate-decision: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Portfolio gate decision (`portfolio-gate-decision`)

Record the human's decision on a challenged portfolio-level artifact that has no state of its own (an artifact with a state moves with its transition workflow).

- **Record:** `gate-decision` at `portfolio/decisions/<decision-slug>.gate-decision.md` (template `templates/shared/gate-decision.artifact-template.md`).
- Name the file `<target-file-stem>-<YYYY-MM-DD>`, for example `product-vision-2026-11-21.gate-decision.md`.

## Rules

- One decision on one artifact per run. An artifact with a state does not come here: Epics, Capabilities, Features (business or enabler), Stories, architecture decisions, supplier agreements, releases and code changes record the decision as a state change in their `*-transition` workflow.
- `accepted` and `accepted-with-concerns` are refused by the harness while no challenge packet targets the artifact: no acceptance without challenge.

## After the run

On a rejection or concerns: rerun the authoring workflow of the artifact.
