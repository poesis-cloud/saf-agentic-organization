---
name: art
user-invocable: false
description: '**SAFe PROCEDURE SKILL — ART / program layer.** The Agile Release Train procedure loaded by `@release-train-engineer` on every invocation. USE FOR: receiving an approved Epic, Feature derivation + refinement, architecture runway (★ Architecture Gate), PI Planning, dispatching `@scrum-master`, Demo Gate, ART Sync, PI Inspect & Adapt, the Program Kanban, State Recovery. DO NOT USE FOR: Epic approval (use `lpm`); iteration execution (use `scrum-master`); authoring Features (use `product-manager` / `system-architect`). Shared orchestration core lives in `release-train-engineer.skill.md`.'
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

# ART procedure (program / ART layer)

Layer-specific procedure for **`@release-train-engineer`**. Load this file as the second required-reading item. The shared **Orchestration core** lives in [release-train-engineer.skill.md](release-train-engineer.skill.md). Portfolio concerns (Strategic Themes, Epics, the ★ Epic Gate, Portfolio Kanban, ART registration) belong to **`@value-management-officer`** / [lpm.skill.md](lpm.skill.md).

## What the release-train-engineer governs

The RTE **polices** the program layer: it controls the agents' input/output artifacts, enforces conformance to its **owned templates** + SAFe practice, and owns the **flow**. It does **not** author or own the backlog.

Central-Supervisor review comments do not relax that boundary. Route them back through the owning authoring skill; do not patch owner-authored files.

- **Features (PM-owned)** — dispatch `@product-manager` to author + refine `art/<art-slug>/program-backlog/<feature-slug>/<feature-slug>.feature.md`; police template + SAFe conformance; render the **Program Kanban**.
- **Architecture runway** — **ART Sync** while ADRs are in flight; facilitate the **★ Architecture Gate** with the full architecture packet (not ADR-only).
- **PI Planning** — `art/<art-slug>/pi-<pi-slug>/objectives.md`; flip Features `ready -> committed`; **dispatch `@scrum-master`**.
- **Demo Gate / System Demo** — facilitate the **★ Demo Gate**; facilitate **PI Inspect & Adapt**; merge approved PRs (**★ PR Gate**).
- **ART health** — gate compliance, Story → Feature → Epic trace, `art/<art-slug>/pi-<pi-slug>/risks.md`; escalate portfolio impediments to `@value-management-officer`.
- **Feature cost — once, at the ★ Demo Gate** — write `cost:` once; notify VMO.
- **Pain points — continuous** — append program/ART friction to the ART `improvement-backlog`.

**Never writes production code.**

## The Flow — Feature handling matrix

The program/ART workflow **is the Feature FSM**: `funnel → refined → arch-pending → ready → committed → in-progress → done` (flag `blocked`). **Step 0:** if the product is unregistered, **escalate to `@value-management-officer`**.

Before executing any ceremony or practice row, load that sub-orchestration skill plus `workflows/{portfolio,program,team}/<name>.workflow.conf.yaml`.

| Event (Feature reaches…) | Kind | Sub-orchestration | Gate | → rte commits |
|---|---|---|---|---|
| Epic `portfolio-backlog`+ | Ceremony·CE | **Feature Backlog Refinement** (full roster) | — | `∅→funnel` → `funnel→refined`; notify VMO |
| `refined` | **Gate** | — | **★ Feature Gate** | accept→`arch-pending` / `ready` · reject→`funnel` |
| `arch-pending` (produce / extend) | Practice·CE | **Architectural Runway Extension** | — | packet committed; stay `arch-pending` |
| runway gap after refinement | Practice·CE | **Architectural Runway Extension** seeds Enabler Feature | — | enabler `∅→funnel`; parent `→funnel` |
| `arch-pending` (inventory covered) | **Gate** | — | **★ Architecture Gate** | accept→`ready` · reject→`refined` |
| `ready` and `dependsOn` met | Ceremony | **PI Planning** | — | `ready→committed`; dispatch SM |
| first child Story `ready` | D | — | — | `committed→in-progress` |
| child Stories all `done` | Ceremony | **System Demo** / Demo Gate | **★ Demo Gate** | accept→`done`; commit `cost:`; notify VMO |
| Story `awaiting-pr` | **Gate** | — | **★ PR Gate** | Story `→done`; roll-up |
| any Feature transition / `→blocked` / ADR in flight | Ceremony | **ART Sync** | — | `→blocked`/unblock |
| `done` (synthesise at Epic completion) | Ceremony | **Inspect & Adapt** | — | triage pain points; seed Features |

## Product registration (escalate to VMO)

Do not create `portfolio/` or mutate the registry from the program layer. Escalate to `@value-management-officer`.

## Program Kanban ownership

Render Program Kanban from Feature frontmatter after every Feature status flip. RTE owns `ready`, `committed`, and program `blocked` plus `awaiting-pr -> done` merge. PM owns `funnel`/`refined`. `@system-architect` owns `arch-pending`. Central Supervisor owns ★ Architecture / Demo transitions.

## Product authoring dispatch

`@product-manager` authors business Features. `@system-architect` authors enabler Features and ADRs. `@product-owner` authors Stories under `@scrum-master`.

## Architecture Gate packet (minimum)

Do not return to the Central Supervisor until: decision inventory is committed; every necessary decision is covered by a proposed ADR or explicit waiver; challenge findings are re-synthesized by `@system-architect`; runway/NFR updates or intentional absences are recorded; enabler seeds / deferrals are surfaced; every runway gap is `seed now` or `defer`.

If the architecture pass seeds a **new enabler Feature**, treat that as refinement invalidation: write the parent Feature back to `funnel` and replay **Feature Backlog Refinement**.

## State Recovery (program / ART view)

1. Read `PROJECT_BRIEF.md` and `portfolio-manifest.yaml`. Identify in-scope products.
2. Read Epics read-only from `portfolio-backlog/`; per product read `product-manifest.yaml`, `art/<art-slug>/program-backlog/`, `art/<art-slug>/pi-<pi-slug>/`, `art/<art-slug>/teams/<team-slug>/team-backlog/`.
3. Re-render Program Kanban and Team Kanban from frontmatter.
4. For each repo in `product-manifest.yaml > repos[]`, run `gh pr list` and `gh issue list` when `gh` is available.
5. Report per product: current PI/Sprint, in-flight Stories, open ADRs, Stories in `in-qa`/`awaiting-pr`, open PRs, Features awaiting ★ Demo Gate, next action.
6. Wait for Central Supervisor confirmation before dispatching.
