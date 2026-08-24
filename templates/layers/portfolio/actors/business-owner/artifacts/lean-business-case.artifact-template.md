<!-- Copyright 2026 Poesis Cloud and contributors

     Licensed under the Apache License, Version 2.0 (the "License");
     you may not use this file except in compliance with the License.
     You may obtain a copy of the License at

         http://www.apache.org/licenses/LICENSE-2.0

     Unless required by applicable law or agreed to in writing, software
     distributed under the License is distributed on an "AS IS" BASIS,
     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
     See the License for the specific language governing permissions and
     limitations under the License. -->

# Lean Business Case Template — `portfolio-backlog/<epic-slug>/<epic-slug>.lean-business-case.md`

The Epic's **Lean Business Case** (SAFe). Authored in the **Epic Lean Business Case** practice
(`epic-lean-business-case`) — `@business-owner` drafts; `@enterprise-architect`,
`@security-expert` challenge. It is the evidence the Central Supervisor (BO hat)
weighs at the **★ Epic Gate**, and the unit **Participatory Budgeting** funds. Portfolio-scoped;
companion to its Epic `E-N`.

```markdown
---
id: E-1-lbc
slug: e-1-lbc
title: E-1 — Lean Business Case
epic: E-1
status: draft            # draft | challenged | gate-ready
fundingState: proposed  # proposed | funded | not-funded   (set by Participatory Budgeting)
---

# E-1 — Lean Business Case

## Problem & opportunity
The systemic problem, who has it, why now.

## Solution hypothesis (MVP)
The smallest Feature set that tests the hypothesis (`mvpFeatures` on the Epic).

## WSJF
| Cost of Delay (UBV + TC + RR) | Job Size | WSJF |
|---|---|---|
| ... | ... | ... |

## Leading & lagging indicators
- Leading: ...
- Lagging: ...

## Cost / effort estimate
Rough order of magnitude; informs Participatory Budgeting.

## Enabler / runway dependency
Architectural-runway items this Epic consumes or requires (→ `architecture-vision`).

## Pivot / persevere / stop criteria
What evidence would change the decision (assessed at Strategic Portfolio Review / Inspect & Adapt).

## Challenge findings
EA / Security adversarial notes, folded in before the ★ Epic Gate.
```
