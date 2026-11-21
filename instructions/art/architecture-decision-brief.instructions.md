---
description: 'Workflow brief of architecture-decision: purpose, artifact paths and the rules of each step.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Architecture decision (`architecture-decision`)

Take one architecture decision that Features need: context, options kept open, the decision proposed and its consequences.

- **Main artifact:** `adr` at `portfolio/arts/<art-slug>/adrs/<adr-slug>/<adr-slug>.adr.md` (template `templates/art/adr.artifact-template.md`), owned by `system-architect`.
- **Challenge packets:** `portfolio/arts/<art-slug>/adrs/<adr-slug>/challenges/architecture-decision-<your-agent-slug>.challenge.md` (template `templates/shared/challenge.artifact-template.md`).
- **Panel:** `software-engineer`, `security-expert`, `platform-engineer`, `data-engineer`, `ai-engineer`.

## Draft

- One decision per run. Read the Features that need it, the NFR register and the Architecture Vision.
- Describe at least two real options with trade-offs; decide at the last responsible moment and say what would reopen the decision.
- Set `status: proposed`. List the enabler Features the decision requires; they are written in `enabler-feature-refinement`.

## Challenge

Apply your own lens (your skill has a section for this artifact), and also test:

- Is this decision needed now, and is a cheaper reversible option available?
- How will a working system prove the decision right?

## Revise

Done when: Options, decision, consequences and validation are filled; `status` is `proposed`. Every packet of this run has its `challengeLedger` entry.

## Human gate

The ART's lead architect (human) accepts or rejects the decision. Next: `art-gate-decision`; then `enabler-feature-refinement` for the runway it requires.
