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

# Enabler Story Template — `art/<art-slug>/teams/<team-slug>/team-backlog/<story-slug>/<story-slug>.story.md`

Iteration-scoped backlog contract for **enabler Stories**. Use this template when `type: enabler`.
An enabler Story is a thin technical slice that advances a parent enabler or business Feature by
removing a concrete engineering, infrastructure, exploration, or compliance blocker.

```markdown
---
id: S-101
title: <Enabler Story title>
status: backlog          # backlog | ready | in-progress | in-review | in-qa | awaiting-pr | done | blocked
type: enabler
enablerType: architectural   # exploration (spike) | architectural | infrastructure | compliance
parentFeature: F-12
workItemRelations:
  dependsOn: []         # hard prerequisite Story/Feature ids for this enabler Story
  enables: []            # downstream Story/Feature ids unblocked by this Story
  relatedTo: []         # non-gating adjacency in the same enablement area
  supersedes: []         # Story ids intentionally replaced by this Story
sprint: N
pi: M
adrs: []
driver: @developer
navigator: @developer
pairSwaps: []
estimatePoints: 0
risk: medium
complexity: involved
owner: SE-Architect
created: YYYY-MM-DD
openItems: []           # clarification + challenge ledger — see orchestrator "Open-item ledger".
                         # Each entry: { id, kind, raised_by, owner, blocking, status, … }; kind: clarification | challenge.
                         # status: open | resolved | withdrawn. A blocking+open entry HALTS the ★ Story Gate (DoR).
cost:
  tokensIn: 0
  tokensOut: 0
  tokensCached: 0
  tokensSelf: 0
  tokensRolled: 0
  dispatches: 0
  source: estimated
  committed: null
github:
  issueNumber: null
  issueNodeId: null
  projectItemId: null
---

# S-101 — <title>

## Enabler story intent
This Story implements <thin technical slice>, so that <named Feature / architecture decision /
operability need> can progress.

### Syntax
Use exactly one sentence in this form:
- `This Story implements <thin technical slice>, so that <named Feature / architecture decision / operability need> can progress.`

## Definition of Ready (DoR)
- [ ] AC complete and testable
- [ ] Dependencies resolved (deps Features `ready`+, ADRs `accepted`)
- [ ] Pair assignable (Driver + Navigator named)
- [ ] Estimate set

## Acceptance criteria (Given/When/Then)
### Syntax
- Use one flat bullet per criterion, labeled `AC1`, `AC2`, `AC3`, ...
- Use only one of these forms:
  - `- AC1. Given <technical context>, when <action or condition>, then <observable result>.`
  - `- AC2. <System/control/artifact> must <measurable technical result>.`
- Each criterion must be testable and traceable to the parent Feature.

- AC1. ...
- AC2. ...

## NFR applicability / trace
Inherit the parent Feature's applicable NFRs from `products/<product-slug>/nfr-list.md`. Record
verification notes for this slice. Do not redefine the product's canonical NFR set. A missing NFR
is a runway concern (hand off to `@release-train-engineer`); do not invent one here.

## Enabler properties
- Consuming Feature / enabler: ...
- Unblocked capability / blocker removed: ...
- Validation evidence expected before closure: ...

### Syntax
- `Consuming Feature / enabler: <id or named capability>`
- `Unblocked capability / blocker removed: <single sentence>`
- `Validation evidence expected before closure: <test, report, review, or artifact>`

## Routing classification
- Risk: low | medium | critical.
- Complexity: simple | involved | complex.
- Rationale: why these values are correct for this Story.

## Work-item relations

Use typed links to show exactly what this enabler Story removes or sequences.

- `dependsOn` — hard prerequisite relation. Use when this Story itself cannot proceed before another
  Story or Feature outcome lands.
- `enables` — primary enabler relation. Use to name the downstream Story or Feature whose path is
  opened once this Story is done.
- `relatedTo` — non-gating adjacency. Use for same-runway-area work that should stay visible but not
  ordered.
- `supersedes` — replacement relation. Use when this Story intentionally absorbs prior technical
  slices.

Best-practice rules:

- At least one `enables` target is expected when the enabler exists to unblock a named downstream
  Story or Feature; otherwise explain the broader technical outcome in prose.
- Keep `adrs` for decision dependencies and `workItemRelations` for backlog-unit links.

## Open items
The human-readable companion to the `openItems:` frontmatter ledger (the [open-item
ledger](../../release-train-engineer/release-train-engineer.skill.md#open-item-ledger)) — this enabler Story's **clarifications**
(proactive unknowns surfaced by the CE Discovery turn) and **challenges** (reactive findings from
peer review), formalized identically and routed to the owning hat. Every **blocking** item must be
resolved before the ★ Story Gate (DoR); non-blocking items are resolved or explicitly deferred with a
recorded default. The ledger is kept after resolution as an audit + agent-memory trail.

### Syntax
One bullet per item, mirroring a frontmatter entry:
- `I<n> [clarification|challenge] [blocking|non-blocking] (raised_by: <hat>, owner: <SA|Security|DevOps|human>): <question or finding>` — default if unanswered: `<assumption>`; status: `open|resolved|withdrawn`.

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
