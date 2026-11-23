---
description: 'Workflow brief of adr-transition: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Generated: builds/model -->

# Architecture decision transition (`adr-transition`)

Record the human's decision on one architecture decision as a state change.

- **Item:** `adr` at `portfolio/arts/<art-slug>/adrs/<adr-slug>/<adr-slug>.adr.md`, owned by `system-architect`.
- **States:** proposed → accepted or rejected; accepted → superseded.

## Rules

- `accepted` sets `decisionDate` and needs a challenged decision; `rejected` needs no challenge.
- `superseded` follows the acceptance of a newer decision that lists this one under `supersedes`.

## After the run

On `accepted`: `feature-enabler-refinement` for the runway the decision requires.
