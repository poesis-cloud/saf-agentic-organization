---
description: 'Orchestrator duty: at the end of a run, bring the challenged artifact to the human gate.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# The human gate

`no-next-step` means every step delivered. Human judgment is the final loop: you present, the human decides.

Present in fifteen lines at most, from the committed artifacts, not from the workers' replies:

1. **The artifact:** its path and what it says in three lines.
2. **The challenge:** per packet, the expert, the verdict and the number of findings. Then every finding the owner rejected or deferred, blocking ones first, with both positions in one line each.
3. **The question:** read the `## Human gate` section of the workflow's brief (`instructions/<layer>/<workflow-slug>-brief.instructions.md` under the framework root) and ask it as written.
4. **The options:** accept, and the workflow that records it (the item's `*-transition`, or your gate-decision workflow) in a new session; or raise concerns or reject, and this workflow runs again in a new session with the concerns as subject.

For an event, a transition or a gate-decision run, present the record's path, its decisions and actions, and the workflow that carries each action.

Never record, assume or anticipate the decision.
