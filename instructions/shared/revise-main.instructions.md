---
description: 'Pattern of a revise step: the owner answers every challenge packet and revises the main artifact for the human gate.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Revise after the challenge

You own the artifact. The panel challenged it; the human decides next.

- **Read every packet of this run.** The subject lists their paths; they sit in the brief's challenge folder, named `<workflow-slug>-<agent-slug>.challenge.md`.
- **Decide each finding.** `accepted`: change the artifact. `rejected`: say why in one line the human can check. `deferred`: valid but handled elsewhere: say where. A `blocking` finding you reject or defer is also listed under `## Open questions` for the human.
- **Fill the ledger.** Set `challengeLedger` to one entry per packet of this run: `{ packet: <path>, challenger: <agent-slug>, verdict: <copied>, responses: [{ finding: F1, disposition: accepted | rejected | deferred, note: <one line> }] }`. A packet without finding gets `responses: []`. Entries of earlier runs are replaced.
- **Keep it coherent.** Re-read the whole artifact after the changes: no section may contradict another.
- **Outcome:** `revised`, or `confirmed` when no finding required a change.
- **Reply** with the counts accepted, rejected and deferred, and what the human must decide.
