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

# Enabler Epic Template — `portfolio-backlog/<epic-slug>/<epic-slug>.epic.md`

Portfolio-scoped backlog contract for **enabler Epics**. Use this template when `type: enabler`.
An enabler Epic is a first-class portfolio backlog unit, not an architecture note: it exists to
fund and govern runway work that enables downstream product Features and program execution.

```markdown
---
id: E-1
title: <Enabler Epic title>
status: funnel            # funnel | reviewing | analyzing | portfolio-backlog | implementing | done | blocked
type: enabler
enablerType: architectural   # architectural | infrastructure | compliance
strategic_theme: <theme-id or name>
businessOwner: central-supervisor
enterpriseArchitect: central-supervisor
products: []
workItemRelations:
  dependsOn: []         # hard prerequisite Epics that must land before this enabler is actionable
  enables: []            # downstream Epic/Feature ids this enabler unblocks
  relatedTo: []         # non-gating semantic or strategic adjacency
  supersedes: []         # Epic ids intentionally replaced by this enabler Epic
wsjf:
  userBusinessValue: 0
  timeCriticality: 0
  riskReduction: 0
  jobSize: 0
  score: 0
mvpFeatures: []
risk: medium
complexity: complex
created: YYYY-MM-DD
approved: null
openItems: []           # clarification + challenge ledger — see orchestrator "Open-item ledger".
                         # Each entry: { id, kind, raised_by, owner, blocking, status, … }; kind: clarification | challenge.
                         # status: open | resolved | withdrawn. A blocking+open entry HALTS the ★ Epic Gate.
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

# E-1 — <title>

## Enablement statement
### Syntax
Use exactly one hypothesis block in this canonical form:
> To enable <products / ARTs / capabilities> to <deliver or operate something>, the <Epic name>
> provides <architectural runway / infrastructure / compliance foundation>. We will know we are
> ready when <dependent Features / ART capabilities> can proceed with reduced risk or removed
> constraints, evidenced by <leading indicators>.

## Runway outcome & leading indicators
### Syntax
- `Leading indicator: <early measurable signal>`
- `Lagging indicator: <later outcome signal>`
- Add more bullets only when each is materially distinct.

- Leading indicator: ...
- Lagging indicator: ...

## In scope / out of scope
- In: ...
- Out (non-goals): ...

## Enablement rationale
Why this runway investment matters now, and what delivery or operability risk it removes.

## Enabler properties
- Consuming products / Features: ...
- Unblocked capabilities / constraints removed: ...
- Validation evidence expected before closure: ...

### Syntax
- `Consuming products / Features: <product slug and/or work-item ids>`
- `Unblocked capabilities / constraints removed: <single sentence>`
- `Validation evidence expected before closure: <test, report, review, or artifact>`

## Enterprise-Architect runway (EA hat)
Cross-product architectural implications, NFR backbone, shared enablers, and which
products must build runway.

## Affected products & Feature seeds
### Syntax
Use one row per product seed in this form:

| Product | Feature seed (becomes F-N in that product) | Notes |
|---|---|---|
| <slug> | <one-line enabler Feature intent> | ... |

## MVP & pivot/persevere
The smallest enabler Feature set (`mvpFeatures`) that makes the blocked delivery path viable.

### Syntax
- `MVP feature set: <Feature id list or named seed list>`
- `Ready when: <evidence that the blocker is removed>`
- `Rework when: <evidence that the runway is still insufficient>`

## Dependencies / constraints
Other Epics, external systems, regulations.

## Work-item relations

Use only relation types that materially shape sequencing or runway intent.

- `dependsOn` — hard prerequisite relation. Use when this enabler Epic cannot remove its target
  constraint before another Epic produces a prerequisite decision or capability.
- `enables` — primary relation for enabler Epics. Use to name the downstream Epics or Features whose
  path becomes viable because this enabler lands.
- `relatedTo` — non-gating adjacency. Use for shared runway area or conceptual coupling that should
  remain visible but must not drive scheduling.
- `supersedes` — replacement relation. Use when this enabler Epic intentionally retires or absorbs an
  earlier runway Epic.

Best-practice rules:

- Prefer `enables` over vague prose when the value of the enabler is specifically to unblock named
  downstream work.
- Use `dependsOn` sparingly; enablers should remove blockers, not accumulate them without cause.
- Do not encode architecture references (ADR ids, runway files, NFR registers) as work-item links;
  keep this contract limited to backlog units.

## Open items
The human-readable companion to the `openItems:` frontmatter ledger (the [open-item
ledger](../../value-management-officer/value-management-officer.skill.md#open-item-ledger)) — this enabler Epic's **clarifications**
(proactive unknowns surfaced by the CE Discovery turn) and **challenges** (reactive findings from
peer review), formalized identically and routed to the owning hat. Every **blocking** item must be
resolved before the ★ Epic Gate; non-blocking items are resolved or explicitly deferred with a
recorded default. The ledger is kept after resolution as an audit + agent-memory trail.

### Syntax
One bullet per item, mirroring a frontmatter entry:
- `I<n> [clarification|challenge] [blocking|non-blocking] (raised_by: <hat>, owner: <EA|Security|DevOps|human>): <question or finding>` — default if unanswered: `<assumption>`; status: `open|resolved|withdrawn`.

- I1 [clarification] [non-blocking] (raised_by: <hat>, owner: ...): ... — default if unanswered: ...; status: open
```
