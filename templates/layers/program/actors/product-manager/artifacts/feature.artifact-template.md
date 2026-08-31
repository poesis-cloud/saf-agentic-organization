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

# Feature Template — `art/<art-slug>/program-backlog/<feature-slug>/<feature-slug>.feature.md`

Authored by `@product-manager` (PM hat). A Feature optionally rolls up to a portfolio **Epic**
(`parentEpic: E-N`); there is **no PRD tier** — the defining intent lives in the Epic (or, for
standalone engineering/operability Features, in the Feature itself). Lives at
`art/<art-slug>/program-backlog/<feature>/`.

```markdown
---
id: F-12
title: <Feature title>
status: funnel           # funnel | refined | arch-pending | ready | committed | in-progress | done | blocked
type: business
parentEpic: E-1         # portfolio Epic id, or null for a standalone Feature
epicRationale: "<why this Feature serves the Epic, or 'standalone: <reason>'>"
workItemRelations:
  dependsOn: []         # hard prerequisite Feature/Epic ids for sequencing or readiness
  enables: []            # downstream Feature/Story ids materially unblocked by this Feature
  relatedTo: []         # non-gating semantic adjacency; not a hidden prerequisite list
  supersedes: []         # Feature ids intentionally replaced by this Feature
wsjf:
  userBusinessValue: 0
  timeCriticality: 0
  riskReduction: 0
  jobSize: 0
  score: 0               # (UBV + TC + RR) / JS
structurant: false       # true ⇒ requires architecture decisions (one or more ADRs) ⇒ arch-pending
risk: medium             # low | medium | critical; set by PM before leaving funnel
complexity: involved     # simple | involved | complex; set by PM before leaving funnel
architectureInventory: null   # required when structurant=true;
                               # path to <adr-slug>.adr.md in the feature folder
adrs: []                 # ADR ids referenced; may contain multiple decisions for one structurant Feature
pi: M                    # set on transition to `committed`
owner: SE-Product-Manager
created: YYYY-MM-DD
openItems: []           # clarification + challenge ledger — see orchestrator "Open-item ledger".
                         # Each entry: { id, kind, raised_by, owner, blocking, status, … }; kind: clarification | challenge.
                         # status: open | resolved | withdrawn. A blocking+open entry HALTS the ★ Feature/Architecture Gate.
cost:                    # token cost accounting — see the cost-snapshot invariant instructions
  tokensIn: 0           # self: NET-NEW prompt tokens = Σ(inputTokens − cachedTokens) of THIS Feature's overhead dispatches
  tokensOut: 0          # self: Σ outputTokens of those dispatches
  tokensCached: 0       # self: Σ cachedTokens (re-sent context; not in tokensSelf — for billed-cost reconstruction)
  tokensSelf: 0         # tokensIn + tokensOut — the Feature's own net cost ("point")
  tokensRolled: 0       # tokensSelf + Σ child Story.tokensRolled — Feature end-to-end cost
  dispatches: 0          # number of subagent dispatches counted into tokensSelf (not llm_request turns)
  source: estimated      # measured | estimated | mixed
  committed: null        # YYYY-MM-DD the one-time snapshot was written (terminal status; immutable after)
github:                  # filled by portfolio/_sync (GitHub Projects board sync); null when authoring
  issueNumber: null
  issueNodeId: null
  projectItemId: null
---

# F-12 — <title>

## Description
What is this Feature, in one paragraph.

## Acceptance criteria
### Syntax
- Use one flat bullet per criterion, labeled `AC1`, `AC2`, `AC3`, ...
- Use only one of these forms:
  - `- AC1. Given <context>, when <action>, then <observable outcome>.`
  - `- AC2. <System/work item> must <measurable rule or result>.`
- Each criterion must be independently testable.
- If `parentEpic` is set, each criterion must trace to the Epic's hypothesis or in-scope items.

- AC1. ...
- AC2. ...

## Benefit hypothesis
Why this Feature delivers value (a slice of the parent Epic's outcome hypothesis, or the
Feature's own rationale when standalone).

### Syntax
Use a short paragraph or 2-3 bullets in this form:
- Beneficiary: <who receives value>
- Outcome: <what changes when the Feature lands>
- Evidence: <how the value will be observed>

## NFR applicability / trace
List the canonical product NFRs from `products/<product-slug>/nfr-list.md` that apply to this Feature,
plus any Feature-specific tightening or derived verification notes. Do not redefine the product's
canonical NFR set here. A missing NFR is a runway concern, not Feature AC.

## Routing classification
- Risk: low | medium | critical — consequence of being wrong.
- Complexity: simple | involved | complex — cognitive/structural difficulty.
- Rationale: why these values are correct for this Feature.

## Dependencies
Other Features, ADRs, external systems. Cross-product coordination is expressed via the shared
parent Epic (one Feature per product), never a single cross-product Feature.

## Work-item relations

Use typed work-item relations only when they affect flow, decomposition, or governance.

- `dependsOn` — hard prerequisite relation. Use when this Feature should not be treated as ready or
  independently executable before the referenced Epic/Feature has produced a required outcome.
- `enables` — capability-unblocking relation. Use when this Feature intentionally opens a downstream
  Feature or Story path, especially for platform or foundation work.
- `relatedTo` — non-gating adjacency. Use for semantic overlap, shared user journey, or common
  outcome area that should remain visible without imposing ordering.
- `supersedes` — replacement relation. Use when this Feature replaces an earlier Feature's scope or
  delivery path.

Best-practice rules:

- Use `parentEpic` for hierarchy, not `relatedTo`.
- Use `dependsOn` only for hard ordering; if the link is informative rather than gating, use
  `relatedTo`.
- Prefer Feature↔Feature links for program sequencing. Link to Stories only when a committed thin
  slice is the thing actually enabled.
- Keep the inverse relation only when it adds clarity; duplicate bookkeeping is optional, not
  required.

## Architecture decision inventory
If `structurant: true`, point to the committed architecture inventory artifact
that tracks the Feature's decision units, their coverage state, linked ADRs,
waivers, and enabler follow-up. If `structurant: false`, set
`architectureInventory: null` and omit this section.

## Open items
The human-readable companion to the `openItems:` frontmatter ledger (the [open-item
ledger](../../release-train-engineer/release-train-engineer.skill.md#open-item-ledger)) — this Feature's **clarifications**
(proactive unknowns surfaced by the CE Discovery turn) and **challenges** (reactive findings from
peer review), formalized identically and routed to the owning hat. Every **blocking** item must be
resolved before the ★ Feature Gate (or the ★ Architecture Gate when `structurant: true`); non-blocking
items are resolved or explicitly deferred with a recorded default. The ledger is kept after
resolution as an audit + agent-memory trail.

### Syntax
One bullet per item, mirroring a frontmatter entry:
- `I<n> [clarification|challenge] [blocking|non-blocking] (raised_by: <hat>, owner: <PM|PO|SA|Security|human>): <question or finding>` — default if unanswered: `<assumption>`; status: `open|resolved|withdrawn`.

- I1 [clarification] [non-blocking] (raised_by: <hat>, owner: ...): ... — default if unanswered: ...; status: open

## Story breakdown (filled in step 6 by PO)
- S-101 …
- S-102 …
```

## Status lifecycle (Program Kanban columns)

```text
funnel → refined → arch-pending → ready → committed → in-progress → done
                 ↑ ★ Feature Gate  ↑ ★ Architecture Gate              ↑ ★ Demo Gate
                        (skip arch-pending if structurant=false)
```

Orthogonal flag: `blocked`.

## Transition rules

| From | To | Trigger / actor |
| --- | --- | --- |
| (none) | `funnel` | PM derives from an Epic (`parentEpic`) or files a standalone Feature |
| `funnel` | `refined` | Feature Backlog Refinement (PM completes AC + WSJF + `structurant`) |
| `refined` | `arch-pending` | **★ Feature Gate** accept + `structurant: true` + committed architecture inventory |
| `refined` | `ready` | **★ Feature Gate** accept + `structurant: false` |
| `refined` | `funnel` | **★ Feature Gate** reject (re-refine) |
| `arch-pending` | `ready` | **★ Architecture Gate** architecture packet accepted (one or more ADRs may be accepted together) |
| `arch-pending` | `refined` | Architecture packet rejected (one or more ADRs may be rejected or require reconsideration) |
| `ready` | `committed` | RTE at PI Planning |
| `committed` | `in-progress` | First child Story passes the **★ Story Gate** → enters Team Kanban `ready` |
| `in-progress` | `done` | **★ Demo Gate** Central Supervisor accepts at Demo Gate |
| any | `blocked` | SM/RTE flag (orthogonal) |

## Relation discipline at this layer

- `dependsOn` is the authoritative program-level gating relation and should align with PI Planning
  and readiness decisions.
- `enables` captures the intended downstream unlock created by this Feature; use it to explain why a
  foundation or enabler Feature exists.
- `relatedTo` must never be used to smuggle a sequencing rule past refinement or planning.
