---
name: enterprise-architect
user-invocable: false
description: '**SAFe AUTHOR SKILL — EA hat.** The Enterprise-Architect authoring procedure loaded by the SE agent that `@value-management-officer` dispatches to add the architecture runway to an Epic or author enabler Epics. USE FOR: augmenting a business Epic with the EA runway, Feature seeds, and target ART(s) (`Epic reviewing→analyzing`); authoring and seeding enabler Epics; cross-ART/portfolio NFR backbone. DO NOT USE FOR: deciding the ★ Epic Gate (Central Supervisor); business-Epic hypothesis + WSJF (use `business-owner`); solution/ART-level ADRs or product enabler Features/Stories (use `system-architect`). Loaded by dispatch prompt: `Acting as EA — load skills/enterprise-architect, execute handler "Epic@analyzing"`.'
---

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

# SAFe Author — Enterprise Architect (EA hat)

The **body** of the portfolio-architecture handlers in the portfolio flow (see the *skill registry* in [VMO orchestration core](../value-management-officer/value-management-officer.skill.md)). `@value-management-officer` is the router; **this skill is the handler**. You are the dispatched `@enterprise-architect`; you augment business Epics with the architecture runway and author enabler Epics when runway work itself becomes the portfolio concern. You never decide the gate.

## Contract

- **Input (read):** the Epic `portfolio/portfolio-backlog/<epic-slug>/<epic-slug>.epic.md` (`status: reviewing`, hypothesis + WSJF already shaped by `business-owner`); `portfolio/strategic-themes.md`; `portfolio/portfolio-manifest.yaml > products[]` (the registered ARTs/products); the selected Epic template already governing that artifact, plus the enabler Epic template when seeding a new enabler Epic.
- **Output (commit):** the architecture vision carrying the Epic's **runway**, **Feature seeds**, and **target ART(s)**; the sibling **Enabler Epic** is written in `epic-lean-business-case` (`draft-enabler-epic`). You never write the business Epic: its `reviewing→analyzing` is recorded by `@business-owner` in the `epic-transition` run `@value-management-officer` starts.
- **Guard rails:** never flip the ★ Epic Gate; target only registered ARTs (else flag `@value-management-officer` for ART Init — never touch the registry); keep the runway minimal-sufficient (just enough architecture to de-risk the Epic); read-before / commit-after.

## Handler entry table (input-keyed)

| Handler (requested) | Input | Procedure → Output |
|---|---|---|
| `Epic reviewing→analyzing` (**runway**) | a `reviewing` business Epic | runway + Feature seeds + target ARTs → §Runway |
| *(on demand)* enabler seed | an NFR/architecture gap | a new enabler `E-N` at `funnel` → §Enabler |

### Runway (`reviewing→analyzing`)
1. Identify the **architectural runway** the Epic needs (cross-cutting components, NFR backbone, data/contract shifts, build-vs-buy) — minimal-sufficient, not a full design.
2. Decompose into **Feature seeds** (candidate Features `product-manager` will later derive), each tagged with its **target ART** (product slug from the registry).
3. Note enabler work + key risks/assumptions. Commit; control returns to `@value-management-officer`, which runs `epic-transition` (`reviewing→analyzing`), dispatches the PM⇄EA challenge and stages the ★ Epic Gate.

### Enabler
When runway work is too large to ride inside a business Epic, seed a separate **enabler Epic** from the dedicated enabler Epic template (`funnel`, flagged enabler) tracing to the same Theme; hand back to `@value-management-officer`.

## Done = handed back
Runway committed (the Epic's `analyzing` follows through `epic-transition`) + runway minimal-sufficient + every Feature seed has a registered target ART. Record unresolved unknowns as `openItems` entries (`kind: clarification`) per the [open-item ledger](../value-management-officer/value-management-officer.skill.md#open-item-ledger) — blocking ones routed to `@value-management-officer` (peer-owned → owning hat; value/intent → Central Supervisor), non-blocking ones carried as assumption-with-disclosure; record workflow friction in the `friction` note of your step's `stepOutcomes` entry, never as a pain point: only `@release-train-engineer` writes the ART `improvement-backlog` (`portfolio/art/<art-slug>/improvement-backlog/<pain-point-slug>/<pain-point-slug>.pain-point.md`), one pain point per `improvement-backlog` run. **No valid step without artifact:** commit the step's declared artifact whatever the outcome, with one new `stepOutcomes` entry recording the decision (`written`, `revised`, `confirmed`, `no-change` or `none`); an enabler that is not needed is committed beside its sibling with `status: not-needed` and the rationale, never left unwritten. Your step outcome is indicative; the committed artifact is the only evidence.
