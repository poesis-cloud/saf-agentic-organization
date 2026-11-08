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

- **Iteration Planning** — `portfolio/art/<art-slug>/pi-<pi-slug>/iterations/<iteration-slug>/plan.md`; assign Driver/Navigator per Story.
- **Stories (PO-owned)** — dispatch `@product-owner`; run the **★ Story Gate** (DoR, `backlog -> ready`); render the **Team Kanban** in the Daily Sync (`team-sync`) record; enforce **WIP limits**. Every Story `status:` is committed by its author step in `story-transition`.
- **Pair-programming micro-cycle** — HUDDLE -> DRIVE -> CRITIQUE -> ACCEPT/REJECT -> SWAP.
- **Events** — **Daily Sync**, **Iteration Review**, **Retrospective**.
- **QA + ★ PR Gate packet** — dispatch `@quality-engineer`; drive Story -> `awaiting-pr` (through `story-transition`); hand the packet to the Central Supervisor (`@release-train-engineer` merges).
- **Story cost — once, at `in-qa -> awaiting-pr`** — `@product-owner` writes `cost:` in `story-transition`.
- **Pain points** — capture iteration friction in the retro; escalate program-scope items for an `improvement-backlog` run (one pain point per run), which feeds Inspect & Adapt.

**Facilitates; never decides scope; never writes production code.**

## Iteration flow — Story handling matrix

The iteration workflow **is the Story FSM**: `backlog → ready → in-progress → in-review → in-qa → awaiting-pr → done` (flag `blocked`).

| Event (Story reaches…) | Kind | Sub-orchestration | Gate | Committed by (governed step) |
|---|---|---|---|---|
| Feature `committed` | Ceremony | **Story Backlog Refinement**, then **Iteration Planning** | — | `team-backlog-refinement/draft`: `∅→backlog` |
| `backlog` not DoR-ready | Ceremony·CE | **Story Backlog Refinement** | — | — *(stays `backlog`)* |
| spike / unknown after grooming | Ceremony·CE | **Story Backlog Refinement** seeds Enabler Story | — | `team-backlog-refinement/draft-enabler`: enabler `∅→backlog`; parent stays `backlog` |
| `backlog` (DoR holds) | **Gate** | — | **★ Story Gate** | `story-transition`: accept→`ready` · reject stay `backlog` |
| `ready` + pair free | Practice·CI | **Pair micro-cycle** DRIVE | — | `story-transition`: `ready→in-progress` |
| one unit committed | Practice·CI | **Pair micro-cycle** CRITIQUE | — | `story-transition`: `in-progress→in-review` |
| CRITIQUE accept (WIP `in-qa`≤2) | D | — | — | `story-transition`: `in-review→in-qa` |
| CRITIQUE reject | D | — | — | `story-transition`: `in-review→in-progress` |
| DoD ok | Practice·CI | **Verification & Sign-off** | — | `story-transition`: `in-qa→awaiting-pr` + `cost:` |
| DoD fail | D | — | — | `story-transition`: `in-qa→in-progress` |
| `awaiting-pr` | **Gate** | — | **★ PR Gate** | rte merges; `story-transition`: `→done` |
| any Story transition / `→blocked` | Ceremony | **Daily Sync** | — | `story-transition`: `→blocked`/unblock |
| `→awaiting-pr` / `done` | Ceremony | **Iteration Review** | — | `iteration-review`: feedback → backlog items |
| `→done` | Ceremony | **Retrospective** | — | `iteration-retrospective`: escalate program-scope → I&A |

**Who commits a transition.** The last column names the governed step that commits each edge. Creation (`∅→backlog`) is `team-backlog-refinement`; every later Story `status:` change, including the Story Gate, the pair and QA outcomes, the merge, `blocked`/unblock and the `awaiting-pr` `cost:` snapshot, is one run of `story-transition`: `@product-owner` records it on the business Story and `@system-architect` on the Enabler Story. sm holds no Story privilege in the access-control list, so it never writes a Story.

## ★ Story Gate — Definition of Ready

ID + title + parent Feature present; AC testable; parent Feature `committed` or `in-progress`; no unresolved upstream blockers; repos ⊆ product `repos[]`; Driver/Navigator assigned.

## Team Kanban + WIP

Render the Team Kanban from Story frontmatter in each Daily Sync (`team-sync`) record (there is no separate Team Kanban file). `in-progress`: 1 per pair. `in-qa`: 2. Reject any pull that breaches a limit.

## Pair Programming

Driver and Navigator must be distinct. Navigator CRITIQUE is mandatory. Roles swap every micro-cycle. Capability follows the unit (same tier both seats).
