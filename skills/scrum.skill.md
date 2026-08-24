---
name: scrum
user-invocable: false
description: '**SAFe PROCEDURE SKILL — team / iteration layer.** The Scrum / Team Coach procedure loaded by `@scrum-master` on every invocation. USE FOR: Iteration Planning, Story grooming + ★ Story Gate, pair-programming micro-cycle, Team Kanban, WIP limits, Daily Sync, Iteration Review, Retrospective, QA acceptance, ★ PR Gate packet prep. DO NOT USE FOR: Feature derivation (use `art`); Epic approval (use `lpm`); authoring Stories (use `product-owner`). Shared orchestration core lives in `scrum-master.skill.md`.'
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

# Scrum procedure (team / iteration layer)

Layer-specific procedure for **`@scrum-master`**. Load this file as the second required-reading item. The shared **Orchestration core** lives in [scrum-master.skill.md](scrum-master.skill.md).

## What the scrum-master governs

The SM **polices** the iteration layer. It does **not** author or own the backlog.

- **Iteration Planning** — `products/<product-slug>/<plan-slug>.plan.md`; assign Driver/Navigator per Story.
- **Stories (PO-owned)** — dispatch `@product-owner`; police the **★ Story Gate** (DoR, `backlog -> ready`); render the **Team Kanban**; enforce **WIP limits**.
- **Pair-programming micro-cycle** — HUDDLE -> DRIVE -> CRITIQUE -> ACCEPT/REJECT -> SWAP.
- **Events** — **Daily Sync**, **Iteration Review**, **Retrospective**.
- **QA + ★ PR Gate packet** — dispatch `@quality-engineer`; drive Story -> `awaiting-pr`; hand the packet to the Central Supervisor (`@release-train-engineer` merges).
- **Story cost — once, at `in-qa -> awaiting-pr`**.
- **Pain points** — capture iteration friction in the retro; escalate program-scope items to Inspect & Adapt.

**Facilitates; never decides scope; never writes production code.**

## Iteration flow — Story handling matrix

The iteration workflow **is the Story FSM**: `backlog → ready → in-progress → in-review → in-qa → awaiting-pr → done` (flag `blocked`).

| Event (Story reaches…) | Kind | Sub-orchestration | Gate | → sm commits |
|---|---|---|---|---|
| Feature `committed` | Ceremony | **Iteration Planning** | — | `∅→backlog` |
| `backlog` not DoR-ready | Ceremony·CE | **Story Backlog Refinement** | — | stays `backlog` |
| spike / unknown after grooming | Ceremony·CE | **Story Backlog Refinement** seeds Enabler Story | — | enabler `∅→backlog`; parent stays `backlog` |
| `backlog` (DoR holds) | **Gate** | — | **★ Story Gate** | accept→`ready` · reject stay `backlog` |
| `ready` + pair free | Practice·CI | **Pair micro-cycle** DRIVE | — | `ready→in-progress` |
| one unit committed | Practice·CI | **Pair micro-cycle** CRITIQUE | — | `in-progress→in-review` |
| CRITIQUE accept (WIP `in-qa`≤2) | D | — | — | `in-review→in-qa` |
| CRITIQUE reject | D | — | — | `in-review→in-progress` |
| DoD ok | Practice·CI | **Verification & Sign-off** | — | `in-qa→awaiting-pr`; commit `cost:` |
| DoD fail | D | — | — | `in-qa→in-progress` |
| `awaiting-pr` | **Gate** | — | **★ PR Gate** | rte merges `→done` |
| any Story transition / `→blocked` | Ceremony | **Daily Sync** | — | `→blocked`/unblock |
| `→awaiting-pr` / `done` | Ceremony | **Iteration Review** | — | feedback → backlog items |
| `→done` | Ceremony | **Retrospective** | — | escalate program-scope → I&A |

## ★ Story Gate — Definition of Ready

ID + title + parent Feature present; AC testable; parent Feature `committed` or `in-progress`; no unresolved upstream blockers; repos ⊆ product `repos[]`; Driver/Navigator assigned.

## Team Kanban + WIP

Render Team Kanban from Story frontmatter after every flip. `in-progress`: 1 per pair. `in-qa`: 2. Reject any pull that breaches a limit.

## Pair Programming

Driver and Navigator must be distinct. Navigator CRITIQUE is mandatory. Roles swap every micro-cycle. Capability follows the unit (same tier both seats).
