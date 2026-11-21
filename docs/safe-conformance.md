<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# SAFe conformance

How the Scaled Agile Framework maps onto this organization, what was verified against the SAFe
knowledge base, and where the organization deliberately adapts SAFe to agents.

SAFe and Scaled Agile Framework are registered trademarks of Scaled Agile, Inc. This repository
is not affiliated with or endorsed by Scaled Agile, Inc.; it applies the framework as published
at <https://framework.scaledagile.com>.

## Sources

The organization was derived from the SAFe knowledge base as read on 2026-11-21:

- **Read in full:** the [glossary](https://framework.scaledagile.com/glossary) (every definition
  quoted in the agents' "SAFe anchor" comes from it),
  [Essential SAFe](https://framework.scaledagile.com/essential-safe),
  [Large Solution SAFe](https://framework.scaledagile.com/large-solution),
  [Strategic Investment Planning](https://framework.scaledagile.com/strategic-investment-planning),
  [Product Owner](https://framework.scaledagile.com/product-owner),
  [SAFe Lean-Agile Principles](https://framework.scaledagile.com/safe-lean-agile-principles),
  [Lean UX](https://framework.scaledagile.com/lean-ux),
  [Responsible AI](https://framework.scaledagile.com/responsible-ai),
  [AI-Native SAFe](https://framework.scaledagile.com/ai-native-safe),
  [Value Stream KPIs](https://framework.scaledagile.com/value-stream-kpis) and
  [What's new in SAFe](https://framework.scaledagile.com/whats-new-in-safe).
- **Read in part:** about 110 further articles (every role, event and artifact named below).
  Their body is reserved to logged-in SAFe members; only the definition and the introduction are
  public, and only those were used.
- **Not verifiable from the public text**, and therefore taken from established SAFe 6 practice:
  the state names of the Portfolio, Solution Train and ART Kanban systems; the fields of the Epic
  hypothesis statement, the Lean Business Case and the portfolio canvas; the ROAM vocabulary; the
  user-voice Story form and INVEST; the names of the Continuous Exploration and Release on Demand
  activities. If your SAFe practice names these differently, change the enums in
  [`artifacts/`](../artifacts/) and the sections in [`templates/`](../templates/); the tests will
  tell you what else must follow.

## The four layers

| SAFe configuration | Layer here | Orchestrator | Human at the gate |
|---|---|---|---|
| Portfolio SAFe | `portfolio` | `value-management-officer` (Value Management Office) | Portfolio Leadership |
| Large Solution SAFe | `solution` | `solution-train-engineer` | Solution Management, lead architects, Business Owners |
| Essential SAFe: the ART | `art` | `release-train-engineer` | Product Management, lead architect, Business Owners |
| Essential SAFe: the Agile team | `team` | `scrum-master` (Scrum Master/Team Coach) | Product Owner, the team, the pull-request reviewer |

Full SAFe is the four together. Each layer works alone: the workspace paths and the conditions
reference a parent only when one exists.

## Roles

| SAFe role or function | Agent | Note |
|---|---|---|
| Value Management Office (VMO) | `value-management-officer` | facilitates Lean Portfolio Management; decides nothing |
| Lean Portfolio Management / Portfolio Leadership | `portfolio-manager` drafts; **the human decides** | Portfolio Leadership "approves epics, funds value streams": always a human gate |
| Epic Owner | `epic-owner` (business Epics), `enterprise-architect` (enabler Epics) | Epic, Lean Business Case, MVP. SAFe: "Enterprise Architects typically act as Epic Owners for Enabler epics." |
| Enterprise Architect | `enterprise-architect` | technology vision, strategy, roadmap; leads enabler Epics through the Portfolio Kanban; challenges Epics |
| Business Owners | `business-owner` prepares; **the human decides** | proposed business value, ROI, governance view |
| Solution Train Engineer | `solution-train-engineer` | |
| Solution Management | `solution-manager` | Solution Vision, Roadmap, Capabilities |
| Solution Architect | `solution-architect` | Solution Intent, enabler Capabilities |
| Supplier | counterpart of `procurement-manager` | the supplier is outside the organization; its agreement is inside |
| Release Train Engineer | `release-train-engineer` | |
| Product Management | `product-manager` | Vision, PI Roadmap, Features |
| System Architect | `system-architect` | enabler Features, architecture decisions, NFRs (SAFe: "defining enablers") |
| Product Owner | `product-owner` | Stories, acceptance |
| Scrum Master/Team Coach | `scrum-master` | |
| Agile Team | `software-engineer`, `quality-engineer` and the experts a Story needs | |
| System Team | `devops-engineer`, `platform-engineer` | Continuous Delivery Pipeline, environments |
| Shared Services | the expert bench | "specialty roles … required for the success of an ART or Solution Train, but … not dedicated full-time" |
| LACE / SAFe Practice Consultant | `agile-coach` | |
| AI Value Architect (AI-Native SAFe) | `ai-engineer` | Responsible AI lens on decisions and NFRs |

## Artifacts

| SAFe artifact | Kind | Workflow that writes it |
|---|---|---|
| Strategic Themes (OKR format) | `strategic-themes` | `strategic-themes` |
| Portfolio Vision, portfolio canvas | `portfolio-vision` | `portfolio-vision` |
| Development value stream, Value Stream KPIs | `value-stream` | `value-stream-definition` |
| Epic, Epic hypothesis statement, MVP | `epic` | `epic-hypothesis`, `epic-mvp-evaluation` |
| Enabler Epic | `epic-enabler` | `epic-enabler-hypothesis`, `epic-enabler-mvp-evaluation` |
| Lean Business Case | `lean-business-case` | `lean-business-case`, `epic-enabler-lean-business-case` |
| Portfolio Backlog / Portfolio Kanban | `kanban` (portfolio) | `epic-transition`, `epic-enabler-transition`, `portfolio-sync` |
| Lean Budgets, guardrails, BSIs and PSIs | `lean-budgets` | `strategic-investment-planning` |
| Portfolio Roadmap | `portfolio-roadmap` | `portfolio-roadmap` |
| Enterprise architecture runway | `architecture-vision` | `architecture-vision` |
| Solution Vision, Solution Context | `solution-vision` | `solution-vision` |
| Solution Roadmap | `solution-roadmap` | `solution-roadmap` |
| Solution Intent (fixed, variable), compliance | `solution-intent` | `solution-intent` |
| Capability | `capability` | `capability-refinement` |
| Enabler Capability | `capability-enabler` | `capability-enabler-refinement` |
| Solution Train Backlog / Kanban | `kanban` (solution-train) | `capability-transition`, `capability-enabler-transition`, `coordinate-and-deliver` |
| Supplier relationship | `supplier-agreement` | `supplier-engagement`, `supplier-agreement-transition` |
| Vision (ART) | `product-vision` | `product-vision` |
| PI Roadmap | `product-roadmap` | `product-roadmap` |
| Feature, benefit hypothesis, acceptance criteria, WSJF | `feature` | `feature-refinement` |
| Enabler Feature | `feature-enabler` | `feature-enabler-refinement` |
| ART Backlog / ART Kanban | `kanban` (art) | `feature-transition`, `feature-enabler-transition`, `art-sync` |
| Architectural Runway decisions | `adr` | `architecture-decision`, `adr-transition` |
| Nonfunctional Requirements | `nfrs` | `nfr-refinement` |
| Continuous Delivery Pipeline | `delivery-pipeline` | `delivery-pipeline` |
| PI Objectives, ART planning board, ART PI risks, confidence vote | `pi-objectives` | `pi-planning`, `solution-train-pi-planning` |
| Release | `release` | `release-on-demand`, `release-transition` |
| Agile team, Definition of Done, Team Kanban | `team-charter`, `kanban` (team) | `team-formation`, `story-transition`, `team-sync` |
| Story, enabler Story, spike | `story` | `story-refinement` |
| Iteration Goals, iteration backlog | `iteration-plan` | `iteration-planning` |
| Working, tested increment | `code-change` (the record; the code lives in its repository) | `story-implementation`, `code-change-transition` |

## Events

| SAFe event | Workflow |
|---|---|
| Strategic Investment Planning (formerly Participatory Budgeting) | `strategic-investment-planning` |
| Strategic Portfolio Review | `strategic-portfolio-review` |
| Portfolio Sync | `portfolio-sync` |
| Pre-Plan | `pre-plan` |
| Solution Train PI Planning | `solution-train-pi-planning` |
| Coordinate and Deliver: Product Manager Sync, Architect Sync, RTE Sync | `coordinate-and-deliver` |
| Solution Demo | `solution-demo` |
| Inspect and Adapt (Solution Train) | `solution-train-inspect-and-adapt` |
| PI Planning | `pi-planning` |
| ART Sync (Coach Sync and PO Sync) | `art-sync` |
| System Demo | `system-demo` |
| Inspect and Adapt | `inspect-and-adapt` |
| Team Backlog Refinement | `story-refinement` |
| Iteration Planning | `iteration-planning` |
| Team Sync | `team-sync` |
| Iteration Review | `iteration-review` |
| Iteration Retrospective | `iteration-retrospective` |

## Kanban states

| Backlog | States |
|---|---|
| Portfolio Kanban (Epic, enabler Epic) | funnel → reviewing → analyzing → ready → implementing (MVP, then persevere) → done |
| Solution Train Kanban (Capability, enabler Capability) and ART Kanban (Feature, enabler Feature) | funnel → analyzing → ready → implementing → validating-on-staging → deploying-to-production → releasing → done |
| Team Kanban (Story) | backlog → ready → in-progress → in-review → accepted (a team may refine these in its charter) |

## SAFe principles in the design

| SAFe Lean-Agile Principle | Where it shows |
|---|---|
| 1. Take an economic view | WSJF on every backlog item; Lean Budgets; the Financial Controller and FinOps Engineer lenses; model routing by capability and cost |
| 2. Apply systems thinking | experts from every discipline read each main artifact before it is decided |
| 3. Assume variability; preserve options | variable Solution Intent; options in architecture decisions; uncommitted PI Objectives |
| 4. Build incrementally with fast, integrated learning cycles | one item per run; draft → challenge → revise; a rejection reiterates the workflow |
| 5. Base milestones on objective evaluation of working systems | System Demo, Solution Demo, MVP evaluation against leading indicators |
| 6. Make value flow without interruptions | Kanban boards with WIP limits; small workflows; one artifact per step |
| 7. Apply cadence, synchronize with cross-domain planning | PI Planning, Pre-Plan, the sync events |
| 8. Unlock the intrinsic motivation of knowledge workers | each agent owns its craft and its artifact; nobody rewrites another's work |
| 9. Decentralize decision-making | each layer decides at its own gate; a concern of another grain is handed off |
| 10. Organize around value | value streams, trains and teams are defined before backlogs |

## Human oversight of agents

AI-Native SAFe asks that "human judgment remains the final, non-negotiable loop for value, safety,
and purpose", and that organizations "monitor autonomous AI agents using a hierarchy of
deterministic rules, automated detection, and human oversight". The organization implements that
hierarchy literally:

| Level | Here |
|---|---|
| Deterministic rules | the harness: step resolution, access control, schema validation, conditions, promotion |
| Automated detection | the expert panel: independent agents whose only job is to find what is wrong before the gate |
| Human oversight | the gate at the end of every workflow, and the committed record of each decision |

Its three pillars for agents map the same way: **intent** stays in human hands (themes, visions
and every gate), **specifications** are "living, machine-readable artifacts" (schema-bound
artifacts with acceptance criteria and NFRs), and **context** is the committed workspace every
agent reads from. Of its four governance pillars, *Controlling AI Spend* is served by per-step
model routing and small contexts, *Enforcing Responsible AI* by the `ai-engineer`, privacy,
security and accessibility lenses, *Monitoring Agentic Behavior* by the harness logs and step
outcomes, and *Managing and Exploiting AI Risk* by the gates.

## Deliberate adaptations

- **One item per run.** A refinement workflow writes one Epic, Capability, Feature or Story. SAFe
  refines backlogs in batches; agents iterate faster on one item with a full panel.
- **Events are records.** A SAFe event is a meeting; here it is a workflow whose record states
  what was inspected, decided and assigned. A backlog change found in an event is carried by its
  own workflow.
- **Business value and commitment stay human.** In `pi-planning` the agents propose objectives,
  a planning board and risks, and the `business-owner` agent proposes business value in its
  packet; the human Business Owners assign it and the confidence vote is recorded at the gate.
- **Acceptance is explicit.** An item with a state (a backlog item, an architecture decision, a
  release, a supplier agreement, a code change) moves through a transition its owner writes; every
  other artifact through a gate decision record. SAFe leaves this to tooling.
- **Enablers are kinds of their own:** `epic-enabler`, `capability-enabler`, `feature-enabler`.
  As in SAFe they live in the same backlog as their business sibling: same folder, same Kanban,
  same states, WSJF against each other. They are separate kinds because the harness authorizes a
  write by kind and their authors differ: the Enterprise Architect (Epic Owner of enabler Epics),
  the Solution Architect and the System Architect. Each backlog kind has one writer, its states
  included. Enabler Stories stay `story` with `type: enabler`: SAFe has the team write all its
  Stories, through its Product Owner.
- **The code repository is outside the workspace.** `story-implementation` works on a branch
  there; the workspace holds the record of the change and its evidence. A human merges.
