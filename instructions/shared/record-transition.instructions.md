---
description: 'Pattern of a transition step: the owner records the human's decision as one state change of a backlog item.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Record a state change

The human decided to move this backlog item. You, its owner, record the move; you never decide it.

- **Subject.** It gives the item's path, the target state, who decided and why. If one is missing, refuse (below) and say which.
- **Check the move.** The states and rules are in the brief. A move that skips a state or breaks a rule is refused.
- **Record.** Set `status` and the fields the brief ties to the new state, and append to `transitions`: `{ from, to, date, decidedBy, reason }`. Outcome `revised`.
- **Refuse.** Change nothing else and append a `stepOutcomes` entry with outcome `no-change` and the reason. A recorded refusal is a valid step.
- **One state change per run.**
