---
description: 'The contract of every workflow step: one step, one session, one artifact, one stepOutcomes entry.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Step contract

You are dispatched for **one step** of one workflow run. The dispatch prompt gives you the step (its slug and artifact kind) and the **subject**: the human's concern in their words and the workspace paths of this run.

1. **One step, one artifact.** Create or update exactly one file of the step's artifact kind, at the path your workflow brief gives. Touch no other artifact.
2. **Template and schema.** Start a new file from the template the brief names (`templates/…` under the framework root). The frontmatter is validated against the kind's schema; an invalid write is reverted with the reason: fix it and write again.
3. **Always leave evidence.** Whatever the outcome, append one `stepOutcomes` entry: `{ step: <workflow-slug>/<step-slug>, outcome: written | revised | confirmed | no-change | none, date: "YYYY-MM-DD", note: <one line: what you decided and why> }`. A write identical to the committed file does not count.
4. **File-edit tools only.** Never write an artifact through the shell.
5. **Read little.** Read the paths named in the subject and the brief; follow a link only when a claim depends on it.
6. **Stay in your step.** Never ask the harness, never dispatch, never change an item's `status` outside a `record-transition` step, never decide in the human's place.
7. **Friction.** If the workflow itself got in your way, say so in the optional `friction` field of your entry; Inspect and Adapt reads it.
8. **Reply in five lines at most:** the path written, the outcome, and what the next step or the human must know. Your reply is indicative; the committed artifact is the only evidence.
