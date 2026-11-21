---
description: 'Workflow brief of release-transition: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Release transition (`release-transition`)

Record the human's decision on one release as a state change: released, rolled back or cancelled.

- **Item:** `release` at `portfolio/arts/<art-slug>/releases/<release-slug>/<release-slug>.release.md`, owned by `release-manager`.
- **States:** planned → ready → released → rolled-back; planned or ready → cancelled.

## Rules

- `released` and `rolled-back` need a challenged release; `released` sets `targetDate` to the release date.
- `rolled-back` follows a released release, triggered as its rollback plan says; `cancelled` needs no challenge.

## After the run

On `released`: `feature-transition` (releasing → done) once each Feature's benefit hypothesis is evaluated.
