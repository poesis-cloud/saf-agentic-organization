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

# Epic Template — `portfolio-backlog/<epic-slug>/<epic-slug>.epic.md`

The portfolio-level artifact. Authored by the **Business Owner** hat (you) with the
**Enterprise Architect** hat for the architectural runway, and refined with `@business-owner`
and `@enterprise-architect` as drafters. An Epic is the **single legitimately cross-product**
artifact: it coordinates Features across one or more products. It is **portfolio-scoped**, so it
lives under `portfolio/`, never under a product slug.

There is **no PRD tier** in this methodology — the Epic carries the intent (problem, outcome
hypothesis, leading indicators) that a PRD used to hold, and it cascades to Features and Stories.

```markdown
---
id: E-1
title: <Epic title — a large outcome spanning products/capabilities>
status: funnel            # funnel | reviewing | analyzing | portfolio-backlog | implementing | done | blocked
type: business
strategic_theme: <theme-id or name>   # see strategic-themes.artifact-template.md
businessOwner: central-supervisor    # the BO-hat approver (you)
enterpriseArchitect: central-supervisor  # the EA-hat owner of the runway (you)
products: []             # product slugs this Epic spans (>=1); cross-product is allowed HERE only
workItemRelations:
  dependsOn: []         # hard prerequisite Epics that must advance/land before this Epic can realize its MVP
  enables: []            # Epic/Feature ids this Epic intentionally makes possible or materially easier
  relatedTo: []         # non-gating semantic or strategic links; never use as a hidden dependency list
  supersedes: []         # Epic ids intentionally replaced by this Epic
wsjf:
  userBusinessValue: 0
  timeCriticality: 0
  riskReduction: 0      # risk reduction / opportunity enablement
  jobSize: 0
  score: 0               # (UBV + TC + RR) / JS
mvpFeatures: []         # Feature ids that constitute the MVP (the pivot/persevere test)
risk: medium             # low | medium | critical
complexity: complex      # simple | involved | complex
created: YYYY-MM-DD
approved: null           # set to YYYY-MM-DD on ★ Epic Gate (portfolio-backlog)
openItems: []           # clarification + challenge ledger — see orchestrator "Open-item ledger".
                         # Each entry: { id, kind, raised_by, owner, blocking, status, … }; kind: clarification | challenge.
                         # status: open | resolved | withdrawn. A blocking+open entry HALTS the ★ Epic Gate.
cost:                    # token cost accounting — see the cost-snapshot invariant instructions
  tokensIn: 0           # self: NET-NEW prompt tokens = Σ(inputTokens − cachedTokens) of THIS Epic's overhead dispatches
  tokensOut: 0          # self: Σ outputTokens of those dispatches
  tokensCached: 0       # self: Σ cachedTokens (re-sent context; not in tokensSelf — for billed-cost reconstruction)
  tokensSelf: 0         # tokensIn + tokensOut — the Epic's own net cost ("point")
  tokensRolled: 0       # tokensSelf + Σ child Feature.tokensRolled — Epic end-to-end cost
  dispatches: 0          # number of subagent dispatches counted into tokensSelf (not llm_request turns)
  source: estimated      # measured | estimated | mixed
  committed: null        # YYYY-MM-DD the one-time snapshot was written (terminal status; immutable after)
github:                  # filled by portfolio/_sync (Portfolio Project); null when authoring
  issueNumber: null
  issueNodeId: null
  projectItemId: null
---

# E-1 — <title>

## Epic hypothesis statement
### Syntax
Use exactly one hypothesis block in this canonical form:
> For <customers/personas> who <do something / have a need>, the <Epic name> is a
> <class of solution> that <delivers value>. Unlike <current alternative>, our solution
> <key differentiator>. We will know we are right when we observe <leading indicators>.

(This replaces the former PRD problem/outcome sections — it IS the defined intent.)

## Outcome hypothesis & leading indicators
### Syntax
- `Leading indicator: <early measurable signal>`
- `Lagging indicator: <later outcome signal>`
- Add more bullets only when each is materially distinct.

- Leading indicator: ...
- Lagging indicator: ...

## In scope / out of scope
- In: ...
- Out (non-goals): ...

## Portfolio outcome rationale
Why this Epic matters to the portfolio in outcome terms.

## Enterprise-Architect runway (EA hat)
Cross-product architectural implications, NFR backbone, shared enablers, and which
products must build runway. Enabler Epics live mostly here. May spawn product-level ADRs
(those remain product-scoped, authored by `@system-architect`).

## Affected products & Feature seeds
### Syntax
Use one row per product seed in this form:

| Product | Feature seed (becomes F-N in that product) | Notes |
|---|---|---|
| <slug> | <one-line Feature intent> | ... |

Each seed becomes a product-scoped Feature (`parentEpic: E-1`). Cross-product work is
expressed as one Feature per product linked to this Epic — never a single cross-product Feature.

## MVP & pivot/persevere
The smallest Feature set (`mvpFeatures`) that validates the hypothesis. After the MVP,
the Business Owner decides pivot / persevere / stop at ★ Epic Gate review or Inspect & Adapt.

### Syntax
- `MVP feature set: <Feature id list or named seed list>`
- `Persevere when: <evidence threshold>`
- `Pivot or stop when: <failure signal or disconfirming evidence>`

## Dependencies / constraints
Other Epics, external systems, regulations.

## Work-item relations

Use only relation types that change planning or governance behavior.

- `dependsOn` — hard prerequisite relation. Use when this Epic cannot reach its MVP or expected
  outcome before the referenced Epic delivers a named capability, decision, or compliance outcome.
- `enables` — capability-unblocking relation. Use when this Epic creates runway or reusable product
  capability that another Epic or Feature is expected to consume.
- `relatedTo` — non-gating semantic relation. Use for overlap, shared outcome area, or adjacency
  that should be visible but must not gate ordering.
- `supersedes` — replacement relation. Use when this Epic intentionally obsoletes an earlier Epic's
  intent or delivery path.

Best-practice rules:

- Prefer the narrowest true relation: if the link is hierarchy, use `products[]` + child Features,
  not `relatedTo`; if it is a prerequisite, use `dependsOn`, not `relatedTo`.
- Keep each link specific and justified in prose here or in the affected section above.
- Avoid reciprocal bookkeeping unless it adds human clarity; one authoritative side is enough.
- Do not model external systems, repos, or ADRs as work-item relations here; capture those in the
  normal dependency/constraint prose.

## Open items
The human-readable companion to the `openItems:` frontmatter ledger (the [open-item
ledger](../../value-management-officer/value-management-officer.skill.md#open-item-ledger)) — this Epic's **clarifications**
(proactive unknowns surfaced by the CE Discovery turn) and **challenges** (reactive findings from
peer review), formalized identically and routed to the owning hat. Every **blocking** item must be
resolved before the ★ Epic Gate; non-blocking items are resolved or explicitly deferred with a
recorded default. The ledger is kept after resolution as an audit + agent-memory trail.

### Syntax
One bullet per item, mirroring a frontmatter entry:
- `I<n> [clarification|challenge] [blocking|non-blocking] (raised_by: <hat>, owner: <BO|EA|PM|Security|human>): <question or finding>` — default if unanswered: `<assumption>`; status: `open|resolved|withdrawn`.

- I1 [clarification] [non-blocking] (raised_by: <hat>, owner: ...): ... — default if unanswered: ...; status: open
```

## Status lifecycle (Portfolio Kanban columns)

```text
funnel → reviewing → analyzing → portfolio-backlog → implementing → done
                                        ↑ ★ Epic Gate (Business-Owner approval)
```

Orthogonal flag: `blocked`.

## Transition rules

| From | To | Trigger / actor |
| --- | --- | --- |
| (none) | `funnel` | BO/EA captures a raw Epic idea |
| `funnel` | `reviewing` | RTE + PM give it an Epic hypothesis + rough WSJF |
| `reviewing` | `analyzing` | EA drafts the runway; products + Feature seeds identified |
| `analyzing` | `portfolio-backlog` | **★ Epic Gate** Business Owner approves the Epic hypothesis |
| `analyzing` | `funnel` | BO defers/declines (re-shape) |
| `portfolio-backlog` | `implementing` | First child Feature enters its product Program Kanban (`funnel`) |
| `implementing` | `done` | All child Features `done` + BO accepts the outcome (at Demo Gate / I&A) |
| any | `blocked` | RTE flag (orthogonal) |

## Identity / linkage

- An Epic's id `E-N` is portfolio-unique (not per product).
- A Feature points up via `parentEpic: E-N` (optional — a Feature may exist without an Epic).
- The Epic lists its products in `products[]`; child Features remain product-scoped.
- `workItemRelations` carries only typed links to other backlog units; use it for planning-governed
  relationships, not for general documentation cross-references.
