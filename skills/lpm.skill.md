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

- **Portfolio Init + ART/product registration** — sole writer of `portfolio-manifest.yaml > products[]` (with `arts[]` retained only as a compatibility list where older tooling still expects it).
- **Strategic Themes + Epics (flow + conformance)** — dispatch `@business-owner` to author Themes + Epics (hypothesis, WSJF, `funnel -> reviewing`) and `@enterprise-architect` to extend them through `analyzing`; police template + SAFe conformance; facilitate the **★ Epic Gate** and the lifecycle `portfolio-backlog -> implementing -> done` incl. **Epic outcome acceptance** (human BO) on the last child Feature `done`.
- **Portfolio Kanban** — rendered from Epic frontmatter; portfolio risk + cross-ART impediments (Epic `blocked`).
- **Portfolio templates** — epic, strategic-themes, portfolio-manifest, product-manifest, kanban-portfolio.
- **Strategic Portfolio Review** — re-rank by WSJF, revise Themes, pivot/persevere/stop.
- **Epic cost — once, at Epic close** — write `cost:` once from ecosystem logs + Σ child Feature `tokensRolled`.
- **Pain points — continuous** — append portfolio friction to the ART `improvement-backlog`.
- **Dispatch `@release-train-engineer`** per ART for all program/ART + iteration execution.

**Never writes production code.**

## The Flow — Epic handling matrix

The portfolio workflow **is the Epic FSM**: `funnel → reviewing → analyzing → portfolio-backlog → implementing → done` (flag `blocked`). **Step 0:** if `portfolio/` or the product is unregistered, run **Portfolio / ART Init** first.

Before executing any ceremony or practice row, load that sub-orchestration skill plus `workflows/{portfolio,program,team}/<name>.workflow.conf.yaml`. The harness `check-step` result is the transition guard.

| Event (Epic reaches…) | Kind | Sub-orchestration | Gate | → vmo commits |
|---|---|---|---|---|
| Strategic Theme + idea | Practice·CE | **Epic Lean Business Case** | — | `∅→funnel` |
| `funnel` valid | Practice·CE | **Epic Lean Business Case** | — | `funnel→reviewing` |
| `reviewing` valid | Practice·CE | **Architectural Vision** | — | `reviewing→analyzing` |
| runway gap after shaping | Practice·CE | **Architectural Vision** seeds Enabler Epic | — | enabler `∅→funnel`; parent `→funnel` |
| `analyzing` (challenge done) | **Gate** | — | **★ Epic Gate** (CS·BO) | accept→`portfolio-backlog` · reject→`funnel` |
| →`portfolio-backlog` or Epic `→done` | Ceremony | **Participatory Budgeting** | — | budget allocation |
| Epic enter (`→funnel`) / exit (`→done`) | Ceremony | **Strategic Portfolio Review** | — | WSJF re-order; pivot |
| first child Feature `funnel` | D | — | — | `portfolio-backlog→implementing` |
| last child Feature `done` | **Gate** | — | **★ Epic Outcome Gate** | accept→`done`; commit `cost:` |
| any Epic transition / `→blocked` | Ceremony | **Portfolio Sync** | — | `→blocked`/unblock |

## Portfolio Init procedure (step 0, run once)

When `portfolio/` does not exist:
1. Create the tree (with `.gitkeep` in empty subfolders): `portfolio-manifest.yaml`, `strategic-themes.md`, `portfolio-vision.md`, `portfolio-roadmap.md`, `portfolio-backlog/`, `art/`, `products/`.
2. Populate `portfolio-manifest.yaml` (Business Owner + Enterprise Architect = `central-supervisor`; `products[]` = authoritative product registry).
3. Seed `strategic-themes.md` from `strategy/poesis-strategy.md` + the business lines.
4. `provision` the Portfolio Project when GitHub sync is in use.

## ART / Product Init procedure (step 0 fallback)

The VMO is the **only** writer of the product registry. When an Epic targets an ART not present in `portfolio-manifest.yaml > products[]`:
1. Halt and ask the Central Supervisor for: product name, slug, one-line description, business line (`theory` | `commercial` | `infra`), owner repos, deps.
2. Create `products/<product-slug>/` with `product-manifest.yaml`, `product-vision.md`, `product-roadmap.md`, `architecture-vision.md`, `architecture-runway.md`. ART/program backlog, PI, and team folders are created lazily under `art/<art-slug>/`.
3. Append the product to `portfolio-manifest.yaml > products[]`.
4. Resume Epic intake.

## Portfolio Kanban ownership

Render Portfolio Kanban from Epic frontmatter after every Epic status flip. VMO owns `reviewing` and `implementing` and the Epic `blocked` flag; the Business-Owner hat owns `funnel`, `portfolio-backlog` (★ Epic Gate), and `done`; the Enterprise-Architect hat owns `analyzing`.

## Authoring roles

Dispatch `@business-owner` for Strategic Themes + business Epics and `@enterprise-architect` for runway / enabler-Epic shaping. Never author backlog artifacts — police them.

## State Recovery (portfolio view)

When the Central Supervisor says "recover state":
1. Read `PROJECT_BRIEF.md`, `portfolio-manifest.yaml`, and `strategic-themes.md`.
2. Read `portfolio-backlog/` (Epic statuses; open Epic-Gate Epics; Epics in `implementing`).
3. Re-render Portfolio Kanban from Epic frontmatter.
4. For each in-flight Epic, dispatch `@release-train-engineer` (or read the product's Program Kanban) for the program/ART rollup.
5. Report: open Epic Gates; implementing Epics + child-Feature rollup; outcome-acceptance queue; portfolio risks; next action.
6. Wait for Central Supervisor confirmation before dispatching.
