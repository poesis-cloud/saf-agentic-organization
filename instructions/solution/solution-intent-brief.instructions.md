---
description: 'Workflow brief of solution-intent: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0. Generated: builds/model -->

# Solution Intent (`solution-intent`)

Record what the solution must do and how it is designed: fixed and variable intent, interfaces, NFRs, standards, verification and traceability.

- **Main artifact:** `solution-intent` at `portfolio/solution-trains/<solution-train-slug>/solution-intent.md` (template `templates/solution/solution-intent.artifact-template.md`), owned by `solution-architect`.
- **Challenge packets:** `portfolio/solution-trains/<solution-train-slug>/challenges/solution-intent-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `systems-engineer`, `security-expert`, `compliance-officer`, `data-protection-officer`, `site-reliability-engineer`.

## Draft

- Read the Solution Vision, the capabilities and the Architecture Vision.
- Separate fixed intent (non-negotiable) from variable intent (options still explored); for each open option, say what learning or date closes it.
- State solution-wide NFRs with measures, the standards that apply, and how evidence is produced as the solution is built.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Is anything fixed too early that set-based design should keep open, or left open that a regulation fixes?
- Can each fixed requirement be verified on a working system?

## Revise

Done when: Fixed and variable intent are separated; every NFR has a measure and a verification. Every packet of this run has its `challengeLedger` entry.

## Human gate

The solution's architects and compliance owner decide whether this intent governs the trains. Next: `solution-gate-decision`; ARTs take the NFRs into `nfr-refinement`.
