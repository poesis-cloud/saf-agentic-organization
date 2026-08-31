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

# Story Template — `art/<art-slug>/teams/<team-slug>/team-backlog/<story-slug>/<story-slug>.story.md`

Authored by `@product-owner` from a `committed` Feature. Trace runs
Story → Feature → Epic (there is no PRD tier). Lives at `art/<art-slug>/teams/<team-slug>/team-backlog/<story>/`.

```markdown
---
id: S-101
title: <Story title>
status: backlog          # backlog | ready | in-progress | in-review | in-qa | awaiting-pr | done | blocked
type: user
parentFeature: F-12
workItemRelations:
  dependsOn: []         # hard prerequisite Story/Feature ids for DoR or execution sequencing
  enables: []            # downstream Story ids or slices made possible by this Story
  relatedTo: []         # non-gating adjacency within the same user journey or capability area
  supersedes: []         # Story ids intentionally replaced by this Story
sprint: N
pi: M
adrs: []                 # ADR ids the Story depends on
driver: @developer      # assigned at Iteration Planning
navigator: @developer   # assigned at Iteration Planning
pairSwaps: []           # log of HUDDLE→SWAP cycles
estimatePoints: 0
risk: medium             # low | medium | critical; set by PO before leaving backlog
complexity: involved     # simple | involved | complex; set by PO before leaving backlog
owner: SE-Product-Manager
created: YYYY-MM-DD
openItems: []           # clarification + challenge ledger — see orchestrator "Open-item ledger".
                         # Each entry: { id, kind, raised_by, owner, blocking, status, … }; kind: clarification | challenge.
                         # status: open | resolved | withdrawn. A blocking+open entry HALTS the ★ Story Gate (DoR).
cost:                    # token cost accounting — see the cost-snapshot invariant instructions
  tokensIn: 0           # NET-NEW prompt tokens = Σ(inputTokens − cachedTokens) of this Story's dispatches (dev D/N, QA, PO grooming)
  tokensOut: 0          # Σ outputTokens of those dispatches
  tokensCached: 0       # Σ cachedTokens (re-sent context; not in tokensSelf — for billed-cost reconstruction)
  tokensSelf: 0         # tokensIn + tokensOut — the Story's net cost (a Story is a leaf)
  tokensRolled: 0       # == tokensSelf for a Story (no children)
  dispatches: 0          # number of subagent dispatches counted into tokensSelf (not llm_request turns)
  source: estimated      # measured | estimated | mixed
  committed: null        # YYYY-MM-DD the one-time snapshot was written (terminal status; immutable after)
github:                  # filled by portfolio/_sync (GitHub Projects board sync); null when authoring
  issueNumber: null
  issueNodeId: null
  projectItemId: null
---

# S-101 — <title>

## User-facing intent
As a <persona>, I want <thin slice>, so that <benefit>.

### Syntax
Use exactly one sentence in this form:
- `As a <persona>, I want <thin slice>, so that <benefit>.`

## Definition of Ready (DoR)
- [ ] AC complete and testable
- [ ] Dependencies resolved (deps Features `ready`+, ADRs `accepted`)
- [ ] Pair assignable (Driver + Navigator named)
- [ ] Estimate set

## Acceptance criteria (Given/When/Then)
### Syntax
- Use one flat bullet per criterion, labeled `AC1`, `AC2`, `AC3`, ...
- Prefer this form: `- AC1. Given <context>, when <action>, then <observable outcome>.`
- If a scenario form is unnatural, use: `- AC2. <System/UI/API> must <measurable result>.`
- Each criterion must be independently testable.

- AC1. Given ..., when ..., then ...
- AC2. ...

## NFR applicability / trace
Inherit the parent Feature's applicable NFRs from `products/<product-slug>/nfr-list.md`. Record
verification notes for this slice. Do not redefine the product's canonical NFR set. A missing NFR
is a runway concern (hand off to `@release-train-engineer`); do not invent one here.

## Routing classification
- Risk: low | medium | critical — consequence of being wrong.
- Complexity: simple | involved | complex — cognitive/structural difficulty.
- Rationale: why these values are correct for this Story.

## Work-item relations

Use only relations that help the team decide DoR, execution order, or slice boundaries.

- `dependsOn` — hard prerequisite relation. Use when this Story should not pass DoR or should not
  start execution before the referenced Story or Feature delivers a required outcome.
- `enables` — slice-unblocking relation. Use when this Story deliberately prepares or unlocks a
  follow-on Story.
- `relatedTo` — non-gating adjacency. Use for shared workflow, common screen, or semantic coupling
  that should be visible without driving scheduling.
- `supersedes` — replacement relation. Use when this Story replaces or absorbs an older Story.

Best-practice rules:

- Use `parentFeature` for hierarchy, not `relatedTo`.
- Prefer Story↔Story links for thin-slice sequencing inside one Feature; use Feature-level links only
  when the blocker genuinely lives above the Story.
- A `dependsOn` link should normally show up in the DoR dependency check; a `relatedTo` link should
  not.

## Open items
The human-readable companion to the `openItems:` frontmatter ledger (the [open-item
ledger](../../scrum-master/scrum-master.skill.md#open-item-ledger)) — this Story's **clarifications**
(proactive unknowns surfaced by the CE Discovery turn) and **challenges** (reactive findings from
peer review), formalized identically and routed to the owning hat. Every **blocking** item must be
resolved before the ★ Story Gate (DoR); non-blocking items are resolved or explicitly deferred with a
recorded default. The ledger is kept after resolution as an audit + agent-memory trail.

### Syntax
One bullet per item, mirroring a frontmatter entry:
- `I<n> [clarification|challenge] [blocking|non-blocking] (raised_by: <hat>, owner: <PO|SA|Security|human>): <question or finding>` — default if unanswered: `<assumption>`; status: `open|resolved|withdrawn`.

- I1 [clarification] [non-blocking] (raised_by: <hat>, owner: ...): ... — default if unanswered: ...; status: open

## Definition of Done (DoD)
- [ ] Code merged behind Central Supervisor approval (★ PR Gate)
- [ ] Tests pass (unit + integration)
- [ ] Coverage maintained
- [ ] `@quality-engineer` sign-off file exists: `<qa-signoff-slug>.qa-signoff.md`
- [ ] PO confirms AC met
- [ ] Docs updated where applicable

## Notes / decisions during pair work
(appended by pair during DRIVE/CRITIQUE)
```

## Status lifecycle (Team Kanban columns)

```text
backlog → ready → in-progress → in-review → in-qa → awaiting-pr → done
                                                            ↑ ★ PR Gate
```

Orthogonal flag: `blocked`.

## Transition rules

| From | To | Trigger / actor |
| --- | --- | --- |
| (none) | `backlog` | PO decomposes from committed Feature |
| `backlog` | `ready` | PO confirms DoR satisfied |
| `ready` | `in-progress` | SM dispatches pair (DRIVE starts) |
| `in-progress` | `in-review` | Driver hands to Navigator (CRITIQUE) |
| `in-review` | `in-progress` | REJECT — back to DRIVE (log a swap) |
| `in-review` | `in-qa` | ACCEPT — pair commits, hands to QA |
| `in-qa` | `in-progress` | QA fails — bug report attached |
| `in-qa` | `awaiting-pr` | QA passes + PO confirms AC + PR opened |
| `awaiting-pr` | `done` | **★ PR Gate** Central Supervisor approves, RTE merges |
| any | `blocked` | SM flag (orthogonal) |
