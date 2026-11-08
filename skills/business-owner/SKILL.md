---
name: business-owner
user-invocable: false
description: '**SAFe AUTHOR SKILL — BO hat.** The Business-Owner authoring procedure loaded by the SE agent that `@value-management-officer` dispatches to execute an Epic transition handler (and the backlog re-rank inside Strategic Portfolio Review). USE FOR: capturing an Epic from a Strategic Theme (`Epic ∅→funnel`); shaping its hypothesis + WSJF + leading indicators (`funnel→reviewing`); maintaining `portfolio/strategic-themes.md`; WSJF re-ranking the portfolio backlog. DO NOT USE FOR: deciding the ★ Epic Gate or accepting Epic outcomes (Central Supervisor); the architecture runway (use `enterprise-architect`); Features (use `product-manager`). Injected by the harness into every step that declares it in `skills:`; the dispatch prompt names only the work: `execute handler "<Epic@state>"`.'
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

# SAFe Author — Business Owner (BO hat)

The **body** of the Epic-shaping handlers in the portfolio flow (see the *skill registry* in [VMO orchestration core](../value-management-officer/SKILL.md)). `@value-management-officer` is the router; **this skill is the handler**. You are the dispatched `@business-owner`; you author Strategic Themes + the Epic and hand control back — you never route, never decide the gate.

## Contract

- **Input (read):** `portfolio/strategic-themes.md`; the raw idea/mandate; the business Epic template plus the **strategic-themes** template ([strategic-themes.artifact-template.md](../../framework/skills/artifacts/strategic-themes.artifact-template.md)). For a re-rank: the whole `portfolio/portfolio-backlog/` set + the open workflow pain points in the ART `improvement-backlog` (`portfolio/art/<art-slug>/improvement-backlog/<pain-point-slug>/<pain-point-slug>.pain-point.md`).
- **Output (commit):** `portfolio/portfolio-backlog/<epic-slug>/<epic-slug>.epic.md` (template-valid against the business Epic template) and/or an updated `portfolio/strategic-themes.md`.
- **Guard rails:** never flip the ★ Epic Gate; never author enabler Epics; every Epic traces to a Strategic Theme; a *workflow* improvement is a meta-artifact change, never a product Epic; read-before / commit-after.

## Handler entry table (input-keyed)

| Handler (requested) | Input | Procedure → Output |
|---|---|---|
| `Epic ∅→funnel` (**capture**) | idea + a Strategic Theme | new `E-N` at `funnel`, traced to its Theme → §Capture |
| `Epic funnel→reviewing` (**shape**) | a `funnel` Epic | hypothesis + WSJF + leading indicators → §Shape |
| *(in Strategic Portfolio Review)* re-rank | the `portfolio/portfolio-backlog/` set | WSJF order + pivot recommendations → §Re-rank |

### Capture (`∅→funnel`)
Create `portfolio/portfolio-backlog/<epic-slug>/<epic-slug>.epic.md` from the business Epic template. If the mandate is explicitly runway, infrastructure, compliance, or architecture enablement work, do not author it here; hand it back as EA-owned enabler work for `enterprise-architect`. Set `status: funnel`, the owning Strategic Theme, and a one-line problem/opportunity. No solutioning. Commit; control returns to `@value-management-officer`.

### Shape (`funnel→reviewing`)
Write the business hypothesis statement required by the business Epic template; add **leading indicators** + MVP scope; compute **WSJF** (record the four components). Commit; control returns to `@value-management-officer`, which dispatches `enterprise-architect` for the runway.

### Re-rank (inside Strategic Portfolio Review)
Re-order the backlog by WSJF; for each in-flight Epic recommend **pivot / persevere / stop** (the Central Supervisor decides). Output the ranking + recommendations; `strategic-portfolio-review` drives the ceremony around you.

## Done = handed back
Output committed + template-valid + every Epic Theme-traced + WSJF components present. Record unresolved unknowns as `openItems` entries (`kind: clarification`) per the [open-item ledger](../value-management-officer/SKILL.md#open-item-ledger) — blocking ones routed to `@value-management-officer` (peer-owned → owning hat; value/intent → Central Supervisor), non-blocking ones carried as assumption-with-disclosure; record workflow friction in the `friction` note of your step's `stepOutcomes` entry, never as a pain point: only `@release-train-engineer` writes the ART `improvement-backlog` (`portfolio/art/<art-slug>/improvement-backlog/<pain-point-slug>/<pain-point-slug>.pain-point.md`), one pain point per `improvement-backlog` run. **No valid step without artifact:** commit the step's declared artifact whatever the outcome, with one new `stepOutcomes` entry recording the decision (`written`, `revised`, `confirmed`, `no-change` or `none`). Your step outcome is indicative; the committed artifact is the only evidence.
