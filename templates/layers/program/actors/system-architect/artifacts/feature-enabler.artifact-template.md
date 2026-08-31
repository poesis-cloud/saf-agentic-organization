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

# Enabler Feature Template — `art/<art-slug>/program-backlog/<feature-slug>/<feature-slug>.feature.md`

Product-scoped backlog contract for **enabler Features**. Use this template when `type: enabler`.
An enabler Feature is a first-class program backlog unit that realizes runway work needed by named
business Features, higher-order enablers, or operational constraints.

```markdown
---
id: F-12
title: <Enabler Feature title>
status: funnel           # funnel | refined | arch-pending | ready | committed | in-progress | done | blocked
type: enabler
enablerType: architectural   # exploration | architectural | infrastructure | compliance
parentEpic: E-1
epicRationale: "<why this enabler serves the Epic, or 'standalone: <reason>'>"
workItemRelations:
  dependsOn: []         # hard prerequisite Feature/Epic ids for this enabler to be actionable
  enables: []            # downstream Feature/Story ids this enabler unblocks
  relatedTo: []         # non-gating adjacency or same-runway-area relation
  supersedes: []         # Feature ids intentionally replaced by this enabler
wsjf:
  userBusinessValue: 0
  timeCriticality: 0
  riskReduction: 0
  jobSize: 0
  score: 0
structurant: false
risk: medium
complexity: involved
architectureInventory: null   # required when structurant=true;
                               # path to <adr-slug>.adr.md in the feature folder
adrs: []
pi: M
owner: SE-Architect
created: YYYY-MM-DD
openItems: []           # clarification + challenge ledger — see orchestrator "Open-item ledger".
                         # Each entry: { id, kind, raised_by, owner, blocking, status, … }; kind: clarification | challenge.
                         # status: open | resolved | withdrawn. A blocking+open entry HALTS the ★ Feature/Architecture Gate.
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

# F-12 — <title>

## Enabler intent
Describe the runway capability, engineering support, or risk reduction this Feature delivers.

### Syntax
Use a short paragraph or 2-3 bullets in this form:
- Capability: <runway or engineering capability delivered>
- Constraint removed: <blocked condition or risk reduced>
- Consumer: <named downstream Feature, Story, or delivery path>

## Acceptance criteria
### Syntax
- Use one flat bullet per criterion, labeled `AC1`, `AC2`, `AC3`, ...
- Use only one of these forms:
  - `- AC1. Given <technical context>, when <action or condition>, then <observable result>.`
  - `- AC2. <Platform/system/control> must <measurable technical, operational, or compliance result>.`
- Each criterion must state what capability is now usable or what downstream work is unblocked.

- AC1. ...
- AC2. ...

## Enablement hypothesis
Explain what future delivery, operability, compliance, or architectural decision this Feature
makes possible, safer, or cheaper.

### Syntax
Use 2-3 bullets in this form:
- Downstream change: <what can happen now>
- Risk/cost effect: <what becomes safer, cheaper, or faster>
- Evidence: <how the improvement will be observed>

## Enabler properties
- Consuming Features / enablers: ...
- Unblocked capabilities / constraints removed: ...
- Validation evidence expected before closure: ...

### Syntax
- `Consuming Features / enablers: <id list or named capability>`
- `Unblocked capabilities / constraints removed: <single sentence>`
- `Validation evidence expected before closure: <test, report, review, or artifact>`

## NFR applicability / trace
List the canonical product NFRs from `products/<product-slug>/nfr-list.md` that apply to this Feature,
plus any Feature-specific tightening or derived verification notes. Do not redefine the product's
canonical NFR set here. A missing NFR is a runway concern, not Feature AC.

## Routing classification
- Risk: low | medium | critical.
- Complexity: simple | involved | complex.
- Rationale: why these values are correct for this Feature.

## Dependencies
Other Features, ADRs, external systems.

## Work-item relations

Use typed relations to make the enabler's program effect explicit.

- `dependsOn` — hard prerequisite relation. Use when this enabler itself relies on another Epic or
  Feature outcome before it can remove the intended blocker.
- `enables` — primary enabler relation. Use to name the downstream Features or Stories whose path is
  opened by this work.
- `relatedTo` — non-gating adjacency. Use when two units share the same runway area but do not
  impose ordering on one another.
- `supersedes` — replacement relation. Use when this enabler absorbs or retires an earlier Feature.

Best-practice rules:

- At least one `enables` target is expected whenever the enabler exists to unblock named downstream
  work; if absent, explain the broad platform/operability outcome in prose.
- Do not mirror architecture artifacts here; keep `adrs` for decisions and `workItemRelations` for
  backlog-unit links only.

## Architecture decision inventory
If `structurant: true`, point to the committed architecture inventory artifact
that tracks the Feature's decision units, their coverage state, linked ADRs,
waivers, and enabler follow-up. If `structurant: false`, set
`architectureInventory: null` and omit this section.

## Open items
The human-readable companion to the `openItems:` frontmatter ledger (the [open-item
ledger](../../release-train-engineer/release-train-engineer.skill.md#open-item-ledger)) — this enabler Feature's **clarifications**
(proactive unknowns surfaced by the CE Discovery turn) and **challenges** (reactive findings from
peer review), formalized identically and routed to the owning hat. Every **blocking** item must be
resolved before the ★ Feature Gate (or the ★ Architecture Gate when `structurant: true`); non-blocking
items are resolved or explicitly deferred with a recorded default. The ledger is kept after
resolution as an audit + agent-memory trail.

### Syntax
One bullet per item, mirroring a frontmatter entry:
- `I<n> [clarification|challenge] [blocking|non-blocking] (raised_by: <hat>, owner: <SA|Security|DevOps|human>): <question or finding>` — default if unanswered: `<assumption>`; status: `open|resolved|withdrawn`.

- I1 [clarification] [non-blocking] (raised_by: <hat>, owner: ...): ... — default if unanswered: ...; status: open

## Story breakdown (filled in step 6 by PO)
- S-101 ...
```
