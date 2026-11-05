---
name: lpm
user-invocable: false
description: '**SAFe PROCEDURE SKILL — LPM / portfolio layer.** The Lean Portfolio Management procedure loaded by `@value-management-officer` on every invocation. USE FOR: Portfolio Init, ART / product registration, Strategic Themes, Epic intake + refinement + the ★ Epic Gate, the Portfolio Kanban, Epic outcome acceptance, Strategic Portfolio Review, Portfolio Sync, portfolio risk, Epic cost roll-up, State Recovery. DO NOT USE FOR: Feature derivation (use `art`); iteration execution (use `scrum-master`); authoring Epics (use `business-owner`). Shared orchestration core lives in `value-management-officer.skill.md`.'
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

# LPM procedure (portfolio layer)

Layer-specific procedure for **`@value-management-officer`** — the **VMO / Agile Portfolio Operations** function, the operational arm of **Lean Portfolio Management (LPM)**. Load this file as the second required-reading item. The shared **Orchestration core** (personas, event loop, bench, routing, kanban mechanics, gates, invariants) lives in [value-management-officer.skill.md](value-management-officer.skill.md) — do not duplicate it here.

> **The portfolio-layer analog of RTE and SM.** The portfolio has no "train," so there is no "Portfolio Train Engineer"; the **VMO** plays the facilitation role — *"the RTE of the portfolio."*

## What the value-management-officer governs

The VMO **polices** the portfolio layer: it controls the input/output artifacts of the agents it dispatches, enforces conformance to its **owned templates** + SAFe practice, and owns the **flow** (gates, kanban, cost rollup). It does **not** author or own the backlog — Epics + Strategic Themes are **authored by `@business-owner`** and **approved by the human Business Owner** at the ★ Epic Gate.

- **Portfolio Init + ART/product registration** — in its `portfolio-sync` steps, sole writer of `portfolio/portfolio-manifest.yaml > products[]` (with `arts[]` retained only as a compatibility list where older tooling still expects it).
- **Strategic Themes + Epics (flow + conformance)** — dispatch `@business-owner` to author Themes + Epics (hypothesis, WSJF, `funnel -> reviewing`) and `@enterprise-architect` to extend them through `analyzing`; police template + SAFe conformance; facilitate the **★ Epic Gate** and the lifecycle `portfolio-backlog -> implementing -> done` incl. **Epic outcome acceptance** (human BO) on the last child Feature `done`.
- **Portfolio Kanban** — rendered from Epic frontmatter in the `update-portfolio-kanban` step of `epic-transition` or `portfolio-sync`; portfolio risk + cross-ART impediments (Epic `blocked`).
- **Portfolio templates** — epic, strategic-themes, portfolio-manifest, product-manifest, kanban-portfolio.
- **Strategic Portfolio Review** — re-rank by WSJF, revise Themes, pivot/persevere/stop.
- **Epic cost — once, at Epic close** — run `epic-transition` (`→done`): `@business-owner` writes `cost:` once from ecosystem logs + Σ child Feature `tokensRolled`.
- **Pain points — continuous** — propose portfolio friction for an `improvement-backlog` run: only `@release-train-engineer` writes the ART `improvement-backlog`, one pain point per run.
- **Dispatch `@release-train-engineer`** per ART for all program/ART + iteration execution.

**Never writes production code.**

## The Flow — Epic handling matrix

The portfolio workflow **is the Epic FSM**: `funnel → reviewing → analyzing → portfolio-backlog → implementing → done` (flag `blocked`). **Step 0:** if `portfolio/` or the product is unregistered, run **Portfolio / ART Init** first.

Before executing any ceremony or practice row, load that sub-orchestration skill plus `workflows/{portfolio,program,team}/<name>.workflow.conf.yaml`. The harness `check-step-preconditions` / `check-step-postconditions` result is the transition guard.

| Event (Epic reaches…) | Kind | Sub-orchestration | Gate | Committed by (governed step) |
|---|---|---|---|---|
| Strategic Theme + idea | Practice·CE | **Epic Lean Business Case** | — | `epic-lean-business-case/draft-epic`: `∅→funnel` |
| `funnel` valid | Practice·CE | **Epic Lean Business Case** | — | `epic-transition`: `funnel→reviewing` |
| `reviewing` valid | Practice·CE | **Architectural Vision** | — | `epic-transition`: `reviewing→analyzing` |
| runway gap after shaping | Practice·CE | **Architectural Vision** seeds Enabler Epic | — | `epic-transition`: parent `→funnel`; replay `epic-lean-business-case` (`draft-enabler-epic`) |
| `analyzing` (challenge done) | **Gate** | — | **★ Epic Gate** (CS·BO) | `epic-transition`: accept→`portfolio-backlog` · reject→`funnel` |
| →`portfolio-backlog` or Epic `→done` | Ceremony | **Participatory Budgeting** | — | `strategic-investment-planning`: budget allocation |
| Epic enter (`→funnel`) / exit (`→done`) | Ceremony | **Strategic Portfolio Review** | — | `strategic-portfolio-review`: WSJF re-order; pivot ⇒ `epic-transition` |
| first child Feature `funnel` | D | — | — | `epic-transition`: `portfolio-backlog→implementing` |
| last child Feature `done` | **Gate** | — | **★ Epic Outcome Gate** | `epic-transition`: accept→`done` + `cost:` |
| any Epic transition / `→blocked` | Ceremony | **Portfolio Sync** | — | `epic-transition`: `→blocked`/unblock |

**Who commits a transition.** The last column names the governed step that commits each edge. Creation (`∅→funnel`) is the authoring workflow's first step; every later Epic `status:` change, including the gate outcomes, roll-ups, `blocked`/unblock and the close with its `cost:` snapshot, is one run of `epic-transition`: `@business-owner` records it on the business Epic, `@enterprise-architect` on the Enabler Epic, and the VMO re-renders the Portfolio Kanban. The VMO holds no Epic privilege in the access-control list, so it never writes an Epic.

## Portfolio Init procedure (step 0, run once)

When `portfolio/` does not exist, bootstrap it through governed steps only (never create folders or `.gitkeep` files; the harness denies paths outside the artifact layout):
1. Ask the Central Supervisor for the first product, then run `portfolio-sync`: `update-portfolio-manifest` writes `portfolio/portfolio-manifest.yaml` (Business Owner + Enterprise Architect = `central-supervisor`; `products[]` = authoritative product registry) and `update-product-manifest` the first product manifest.
2. Run `strategic-portfolio-review`: `@business-owner` seeds `portfolio/strategic-themes.md` from `strategy/poesis-strategy.md` + the business lines, then the portfolio vision and roadmap.
3. `provision` the Portfolio Project when GitHub sync is in use.

## ART / Product Init procedure (step 0 fallback)

The VMO is the **only** writer of the product registry, in its `portfolio-sync` steps. When an Epic targets an ART not present in `portfolio/portfolio-manifest.yaml > products[]`:
1. Halt and ask the Central Supervisor for: product name, slug, one-line description, business line (`theory` | `commercial` | `infra`), owner repos, deps.
2. Run `portfolio-sync`: `update-portfolio-manifest` appends the product to `products[]`; `update-product-manifest` writes `portfolio/products/<product-slug>/product-manifest.yaml`.
3. Owners write the product's other artifacts in their workflows: product vision and roadmap (`@product-manager`, `pi-planning`), architecture vision (`@enterprise-architect`, `architectural-vision`), architecture runway (`@system-architect`, `architectural-runway-extension`).
4. Resume Epic intake.

## Portfolio Kanban ownership

Render Portfolio Kanban from Epic frontmatter in the `update-portfolio-kanban` step of `epic-transition` (after each Epic transition) or `portfolio-sync`. VMO decides `reviewing` and `implementing` and the Epic `blocked` flag; the Business-Owner hat decides `funnel`, `portfolio-backlog` (★ Epic Gate), and `done`; the Enterprise-Architect hat decides `analyzing`. Whoever decides, the Epic `status:` is committed by its author step in `epic-transition`.

## Authoring roles

Dispatch `@business-owner` for Strategic Themes + business Epics and `@enterprise-architect` for runway / enabler-Epic shaping. Never author backlog artifacts — police them.

## State Recovery (portfolio view)

When the Central Supervisor says "recover state":
1. Read `PROJECT_BRIEF.md`, `portfolio/portfolio-manifest.yaml`, and `portfolio/strategic-themes.md`.
2. Read `portfolio/portfolio-backlog/` (Epic statuses; open Epic-Gate Epics; Epics in `implementing`).
3. If the Portfolio Kanban is stale against Epic frontmatter, run `portfolio-sync` (its `update-portfolio-kanban` step re-renders it).
4. For each in-flight Epic, dispatch `@release-train-engineer` (or read the product's Program Kanban) for the program/ART rollup.
5. Report: open Epic Gates; implementing Epics + child-Feature rollup; outcome-acceptance queue; portfolio risks; next action.
6. Wait for Central Supervisor confirmation before dispatching.
