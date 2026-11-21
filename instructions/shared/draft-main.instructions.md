---
description: 'Pattern of a draft step: the owner creates or thickens the main artifact for the human gate.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Draft the main artifact

You own this workflow's main artifact. A human will decide on it after the experts challenged it.

- **New or existing.** New: create it from the template, with the slug the subject gives. Existing: thicken it in place: keep what still holds, change what the subject asks, and preserve `challengeLedger`, `transitions` and the `stepOutcomes` history.
- **Reiteration.** When the subject carries concerns from a previous gate, address each one and say how in your `stepOutcomes` note.
- **Write for the gate.** The human must be able to decide from this artifact alone: facts over adjectives, every number with its unit and source, every unknown under `## Open questions` (or the closest section) with who can answer and the assumption taken meanwhile.
- **Stay in your grain.** Content that belongs to another artifact kind or layer is named with the workflow that will write it, not written here.
- **Do not pre-answer the challenge.** Leave `challengeLedger` as it is; the `revise` step fills it.
- **Outcome:** `written` for a new artifact, `revised` for a thickened one, `no-change` when the subject asks nothing of it (the entry is still appended).
