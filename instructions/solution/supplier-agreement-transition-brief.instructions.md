---
description: 'Workflow brief of supplier-agreement-transition: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Generated: builds/model -->

# Supplier agreement transition (`supplier-agreement-transition`)

Record the human's decision on one supplier agreement as a state change.

- **Item:** `supplier-agreement` at `portfolio/solution-trains/<solution-train-slug>/suppliers/<supplier-slug>/<supplier-slug>.supplier-agreement.md`, owned by `procurement-manager`.
- **States:** draft → negotiating → active → ended.

## Rules

- `negotiating` follows the decision to proceed on these terms; `active` follows the signature by the humans; both need a challenged agreement.
- `ended` follows termination or the end of the term; say the continuity measures in the reason.

## After the run

On `active`: the supplier joins `pre-plan` and `solution-train-pi-planning`.
