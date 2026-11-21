<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Organization catalog

Reference of the roster, the workflow catalog, the challenge panels and the artifact kinds, generated from [`builds/model/`](../builds/model/) (`make generate`). How to use them is in [usage-model.md](usage-model.md).

## Roster

38 agents: 4 orchestrators, 9 SAFe roles, 25 experts.

### Orchestrators: the agents you talk to

| Agent | Authors | Challenges | SAFe anchor |
|---|---|---|---|
| `value-management-officer` | — · records: `event-record`, `gate-decision`, `kanban` | — | Value Management Office (VMO): the function that facilitates the Lean Portfolio Management process and fosters operational excellence and lean governance. |
| `solution-train-engineer` | `event-record`, `pi-objectives`, `solution-train-canvas` · records: `event-record`, `gate-decision`, `kanban` | — | Solution Train Engineer (STE): servant leader and coach who facilitates Solution Train events and processes, coordinates the work of ARTs and Suppliers. |
| `release-train-engineer` | `art-canvas`, `event-record`, `pi-objectives` · records: `event-record`, `gate-decision`, `kanban` | — | Release Train Engineer (RTE): servant leader and ART coach who facilitates ART events and processes, and supports teams in delivering value. |
| `scrum-master` | `iteration-plan`, `team-charter` · records: `event-record`, `gate-decision`, `kanban` | — | Scrum Master/Team Coach (SM/TC): servant leader and coach for an Agile team who facilitates team events and processes. |

### SAFe roles: the authors

| Agent | Authors | Challenges | SAFe anchor |
|---|---|---|---|
| `portfolio-manager` | `lean-budgets`, `portfolio-roadmap`, `portfolio-vision`, `strategic-themes`, `value-stream` | — | Lean Portfolio Management (LPM): aligns strategy and execution through strategy and investment funding, Agile portfolio operations, and lean governance. Portfolio Leadership (the human) decides. |
| `epic-owner` | `epic`, `lean-business-case` · records: `epic` | — | Epic Owner: responsible for coordinating epics through the portfolio Kanban system; defines the Epic, the Lean business case, and the MVP. |
| `enterprise-architect` | `architecture-vision` | `epic`, `lean-budgets`, `lean-business-case`, `portfolio-roadmap`, `portfolio-vision`, `strategic-themes`, `value-stream` | Enterprise Architect: responsible for establishing the portfolio's technology vision, strategy, and roadmap; typically acts as Epic Owner for enabler epics. |
| `business-owner` | — | `epic`, `lean-budgets`, `pi-objectives`, `portfolio-vision`, `product-roadmap`, `product-vision`, `solution-vision`, `strategic-themes` | Business Owners (BOs): key ART stakeholders with the primary business and technical responsibility for return on investment (ROI), governance, and compliance. |
| `solution-manager` | `capability`, `solution-roadmap`, `solution-vision` · records: `capability` | `pi-objectives` | Solution Management: the function responsible for defining desirable, viable, feasible, and sustainable large solutions; responsible for the Solution Train backlog. |
| `solution-architect` | `solution-intent` | `architecture-vision`, `capability`, `pi-objectives`, `solution-roadmap`, `solution-train-canvas`, `solution-vision`, `supplier-agreement` | Solution Architect: responsible for defining and communicating a shared technical and architectural vision for a Solution Train. |
| `product-manager` | `feature`, `product-roadmap`, `product-vision` · records: `feature` | `art-canvas`, `pi-objectives` | Product Management: the function responsible for defining desirable, viable, feasible, and sustainable solutions; responsible for the ART backlog. |
| `system-architect` | `adr`, `feature`, `nfrs` | `art-canvas`, `feature`, `pi-objectives`, `product-roadmap`, `product-vision` | System Architect: responsible for defining and communicating a shared technical and architectural vision for the solutions developed by an ART; defines enablers and outlines NFRs. |
| `product-owner` | `story` · records: `story` | `iteration-plan`, `team-charter` | Product Owner (PO): the Agile team member primarily responsible for maximizing the value delivered by the team; content authority for the team backlog. |

### Expert bench: real IT jobs

| Agent | Authors | Challenges | SAFe anchor |
|---|---|---|---|
| `software-engineer` | `code-change` | `adr`, `feature`, `iteration-plan`, `pi-objectives`, `story` | Agile Team member (Builder): defines, builds, tests and delivers value with built-in quality. |
| `quality-engineer` | — | `code-change`, `delivery-pipeline`, `feature`, `iteration-plan`, `nfrs`, `release`, `story`, `team-charter` | Agile Team member: Agile testing and built-in quality (BDD, TDD, automated tests). |
| `devops-engineer` | `delivery-pipeline` | `feature` | System Team: builds and supports the Agile development environment and the Continuous Delivery Pipeline. |
| `platform-engineer` | — | `adr`, `architecture-vision`, `delivery-pipeline`, `feature` | System Team / Shared Services: platforms and environments. |
| `site-reliability-engineer` | — | `delivery-pipeline`, `feature`, `nfrs`, `release`, `solution-intent` | Shared Services: operational reliability (Continuous Deployment: Deploy, Verify, Monitor, Respond). |
| `observability-engineer` | — | `code-change`, `feature`, `nfrs`, `release` | Shared Services: monitoring and measurement (Continuous Deployment: Monitor; Release on Demand: Measure). |
| `database-administrator` | — | `code-change` | Shared Services: database administration. |
| `data-engineer` | — | `adr`, `architecture-vision` | Shared Services: data engineering (Big Data practices). |
| `ai-engineer` | — | `adr`, `nfrs` | Shared Services: AI expertise on the ART (the lens SAFe assigns to the AI Value Architect and Responsible AI practices). |
| `security-expert` | — | `adr`, `architecture-vision`, `capability`, `code-change`, `delivery-pipeline`, `feature`, `lean-business-case`, `nfrs`, `release`, `solution-intent`, `story`, `supplier-agreement` | Shared Services: security (DevSecOps). |
| `data-protection-officer` | — | `feature`, `lean-business-case`, `solution-intent` | Shared Services: privacy and data protection compliance. |
| `compliance-officer` | — | `capability`, `solution-intent`, `supplier-agreement` | Compliance: activities and artifacts that let teams apply Lean-Agile methods while meeting regulatory and industry standards (Lean QMS). |
| `legal-counsel` | — | `lean-business-case`, `supplier-agreement` | Shared Services: legal (Agile contracts, supplier relationships). |
| `financial-controller` | — | `epic`, `lean-budgets`, `lean-business-case`, `portfolio-roadmap`, `strategic-themes`, `supplier-agreement` | Lean Governance: oversight of spending, audit, compliance, expenditure, measurement, and reporting. |
| `finops-engineer` | — | `architecture-vision`, `delivery-pipeline`, `lean-budgets` | Shared Services: cloud financial management (economic view of technical choices). |
| `ux-designer` | — | `feature`, `product-vision`, `solution-vision`, `story` | Shared Services: user experience (Design Thinking, Lean UX). |
| `accessibility-specialist` | — | `code-change`, `nfrs` | Shared Services: accessibility (inclusiveness is a Responsible AI and customer-centricity attribute). |
| `business-analyst` | — | `portfolio-vision`, `solution-train-canvas`, `value-stream` | Shared Services: business analysis (operational value streams, customer and stakeholder needs). |
| `data-analyst` | — | `epic`, `inspect-and-adapt`, `strategic-themes` | Measure and Grow: outcomes, flow and competency measured with data (OKRs, KPIs, flow metrics). |
| `systems-engineer` | — | `capability`, `pi-objectives`, `solution-intent`, `solution-roadmap` | Large Solution practices: Model-Based Systems Engineering, Set-Based Design, frequent integration. |
| `release-manager` | `release` | `product-roadmap`, `solution-roadmap` | Release on Demand: making new functionality available to customers, decoupled from deployment; release governance. |
| `technical-writer` | — | `release` | Shared Services: documentation and customer training. |
| `product-marketing-manager` | — | `portfolio-roadmap`, `product-vision`, `solution-vision` | Product Marketing: go-to-market alignment with Product Management. |
| `procurement-manager` | `supplier-agreement` | — | Supplier relationships: internal or external organizations that deliver components, subsystems or services to ARTs and value streams (Lean-Agile procurement). |
| `agile-coach` | — | `art-canvas`, `inspect-and-adapt`, `solution-train-canvas`, `team-charter`, `value-stream` | Lean-Agile Center of Excellence (LACE) / SAFe Practice Consultant: coaching and relentless improvement. |

## Workflow catalog

50 workflows. Every workflow ends at a human gate; a `loop` is draft → expert challenge → owner revision.

### Portfolio: `value-management-officer`

| Workflow | Purpose | Gate artifact | Author | Challenge panel | Steps |
|---|---|---|---|---|---|
| `strategic-themes` | Formulate or revise the portfolio's Strategic Themes as Objectives and Key Results that connect the portfolio to the enterprise strategy. | `strategic-themes` | `portfolio-manager` | `enterprise-architect`, `business-owner`, `financial-controller`, `data-analyst` | 6 |
| `portfolio-vision` | Describe the future state of the portfolio's value streams and solutions, from the current-state portfolio canvas to the future-state one. | `portfolio-vision` | `portfolio-manager` | `enterprise-architect`, `business-analyst`, `business-owner` | 5 |
| `value-stream-definition` | Define one development value stream: the operational value streams it supports, its solutions and customers, the trains that realize it, and its KPIs. | `value-stream` | `portfolio-manager` | `business-analyst`, `enterprise-architect`, `agile-coach` | 5 |
| `epic-hypothesis` | Capture or thicken one Epic as an Epic hypothesis statement, ready for Portfolio Leadership to review. | `epic` | `epic-owner` | `enterprise-architect`, `business-owner`, `data-analyst` | 5 |
| `lean-business-case` | Analyze one Epic in the analyzing state: define its MVP, estimate its cost and projected value, and recommend go or no-go. | `lean-business-case` | `epic-owner` | `enterprise-architect`, `financial-controller`, `security-expert`, `data-protection-officer`, `legal-counsel` | 7 |
| `epic-mvp-evaluation` | Evaluate the MVP of one implementing Epic against its hypothesis and recommend to persevere, pivot or stop. | `epic` | `epic-owner` | `data-analyst`, `business-owner`, `financial-controller` | 5 |
| `portfolio-roadmap` | Build or revise the multi-year view of how the Portfolio Vision will be achieved across the value streams. | `portfolio-roadmap` | `portfolio-manager` | `enterprise-architect`, `financial-controller`, `product-marketing-manager` | 5 |
| `strategic-investment-planning` | Establish or update Lean value stream budgets and their guardrails for the coming budget period (formerly Participatory Budgeting). | `lean-budgets` | `portfolio-manager` | `financial-controller`, `enterprise-architect`, `business-owner`, `finops-engineer` | 6 |
| `architecture-vision` | Establish or revise the portfolio's technology vision, strategy and roadmap, and the architectural runway it needs. | `architecture-vision` | `enterprise-architect` | `solution-architect`, `security-expert`, `platform-engineer`, `data-engineer`, `finops-engineer` | 7 |
| `epic-transition` | Record the human's decision to move one Epic to a new Portfolio Kanban state, then re-render the Portfolio Kanban. | `epic` | `epic-owner` | — | 2 |
| `portfolio-sync` | Inspect the flow of Epics and the portfolio's operations between Strategic Portfolio Reviews, and re-render the Portfolio Kanban. | `event-record` | `value-management-officer` | — | 2 |
| `strategic-portfolio-review` | Review whether the portfolio is achieving its vision and themes, and record the funding and direction decisions Portfolio Leadership takes. | `event-record` | `value-management-officer` | — | 1 |
| `portfolio-gate-decision` | Record the human's decision on a challenged portfolio-level artifact that is not a backlog item (backlog items move with their transition workflow). | `gate-decision` | `value-management-officer` | — | 1 |

### Large Solution: `solution-train-engineer`

| Workflow | Purpose | Gate artifact | Author | Challenge panel | Steps |
|---|---|---|---|---|---|
| `solution-train-launch` | Define or revise one Solution Train: its mission, ARTs and suppliers, roles and cadence. | `solution-train-canvas` | `solution-train-engineer` | `agile-coach`, `solution-architect`, `business-analyst` | 5 |
| `solution-vision` | Describe the future state of the large solution: customer and stakeholder needs and the proposed solution. | `solution-vision` | `solution-manager` | `solution-architect`, `business-owner`, `ux-designer`, `product-marketing-manager` | 6 |
| `solution-roadmap` | Forecast the solution's deliverables: a PI roadmap (one committed PI, two forecast) and a multi-year view. | `solution-roadmap` | `solution-manager` | `solution-architect`, `systems-engineer`, `release-manager` | 5 |
| `solution-intent` | Record what the solution must do and how it is designed: fixed and variable intent, interfaces, NFRs, standards, verification and traceability. | `solution-intent` | `solution-architect` | `systems-engineer`, `security-expert`, `compliance-officer`, `data-protection-officer`, `site-reliability-engineer` | 7 |
| `capability-refinement` | Write or thicken one Capability so it is ready for Pre-Plan: benefit hypothesis, acceptance criteria, WSJF and the Features each ART would take. | `capability` | `solution-manager` | `solution-architect`, `systems-engineer`, `security-expert`, `compliance-officer` | 6 |
| `supplier-engagement` | Write or revise the agreement that brings one supplier into the Solution Train's cadence, quality expectations and compliance obligations. | `supplier-agreement` | `procurement-manager` | `legal-counsel`, `security-expert`, `compliance-officer`, `financial-controller`, `solution-architect` | 7 |
| `pre-plan` | Align and prepare the ARTs and suppliers of the Solution Train for PI Planning. | `event-record` | `solution-train-engineer` | — | 1 |
| `solution-train-pi-planning` | Aggregate the ARTs' PI plans into the Solution Train's PI Objectives, planning board and risks for one PI. | `pi-objectives` | `solution-train-engineer` | `solution-manager`, `solution-architect`, `systems-engineer`, `business-owner` | 6 |
| `coordinate-and-deliver` | Keep the ARTs and suppliers aligned during the PI (Product Manager Sync, Architect Sync, RTE Sync) and re-render the Solution Train Kanban. | `event-record` | `solution-train-engineer` | — | 2 |
| `solution-demo` | Give stakeholders an integrated view of what the ARTs and suppliers built in the PI, as objective evidence, and collect their feedback. | `event-record` | `solution-train-engineer` | — | 1 |
| `solution-train-inspect-and-adapt` | Evaluate the integrated solution and the train's way of working at the end of the PI, and derive improvement backlog items. | `event-record` | `solution-train-engineer` | `agile-coach`, `data-analyst` | 4 |
| `capability-transition` | Record the human's decision to move one Capability to a new Solution Train Kanban state, then re-render the Solution Train Kanban. | `capability` | `solution-manager` | — | 2 |
| `solution-gate-decision` | Record the human's decision on a challenged solution train-level artifact that is not a backlog item (backlog items move with their transition workflow). | `gate-decision` | `solution-train-engineer` | — | 1 |

### ART: `release-train-engineer`

| Workflow | Purpose | Gate artifact | Author | Challenge panel | Steps |
|---|---|---|---|---|---|
| `art-launch` | Define or revise one Agile Release Train: its mission, teams, roles and PI cadence. | `art-canvas` | `release-train-engineer` | `agile-coach`, `system-architect`, `product-manager` | 5 |
| `product-vision` | Describe the future state of the solution the ART develops: customers, their needs and the features proposed to meet them. | `product-vision` | `product-manager` | `system-architect`, `ux-designer`, `business-owner`, `product-marketing-manager` | 6 |
| `product-roadmap` | Forecast the ART's deliverables: the committed PI and the next two as a forecast. | `product-roadmap` | `product-manager` | `system-architect`, `business-owner`, `release-manager` | 5 |
| `feature-refinement` | Write or thicken one business Feature so it is ready for PI Planning: benefit hypothesis, acceptance criteria and WSJF. | `feature` | `product-manager` | `system-architect`, `software-engineer`, `quality-engineer`, `security-expert`, `ux-designer`, `data-protection-officer` | 8 |
| `enabler-feature-refinement` | Write or thicken one enabler Feature that extends the architectural runway or improves the delivery pipeline. | `feature` | `system-architect` | `software-engineer`, `platform-engineer`, `devops-engineer`, `site-reliability-engineer`, `observability-engineer` | 7 |
| `architecture-decision` | Take one architecture decision that Features need: context, options kept open, the decision proposed and its consequences. | `adr` | `system-architect` | `software-engineer`, `security-expert`, `platform-engineer`, `data-engineer`, `ai-engineer` | 7 |
| `nfr-refinement` | Create or revise the ART's register of nonfunctional requirements: each one bounded, measurable and verifiable. | `nfrs` | `system-architect` | `site-reliability-engineer`, `observability-engineer`, `security-expert`, `quality-engineer`, `accessibility-specialist`, `ai-engineer` | 8 |
| `delivery-pipeline` | Map the ART's Continuous Delivery Pipeline from ideation to on-demand release, find its bottlenecks and propose the enablers that remove them. | `delivery-pipeline` | `devops-engineer` | `platform-engineer`, `security-expert`, `quality-engineer`, `site-reliability-engineer`, `finops-engineer` | 7 |
| `pi-planning` | Plan one PI for the ART: team and ART PI Objectives, the planning board and the PI risks. | `pi-objectives` | `release-train-engineer` | `product-manager`, `system-architect`, `software-engineer`, `business-owner` | 6 |
| `release-on-demand` | Plan one release and assemble its readiness evidence: what is made available to which customers, how, and how its outcome will be measured. | `release` | `release-manager` | `site-reliability-engineer`, `observability-engineer`, `security-expert`, `quality-engineer`, `technical-writer` | 7 |
| `art-sync` | Inspect the ART's progress toward its PI Objectives (Coach Sync and PO Sync combined), handle dependencies and impediments, and re-render the ART Kanban. | `event-record` | `release-train-engineer` | — | 2 |
| `system-demo` | Show the integrated work of all teams for the iteration from a production-like environment, as an objective measure of progress, and collect feedback. | `event-record` | `release-train-engineer` | — | 1 |
| `inspect-and-adapt` | Evaluate the PI's result and the ART's way of working at the end of the PI, and derive improvement backlog items. | `event-record` | `release-train-engineer` | `agile-coach`, `data-analyst` | 4 |
| `feature-transition` | Record the human's decision to move one Feature (business or enabler) to a new ART Kanban state, then re-render the ART Kanban. | `feature` | `product-manager` | — | 2 |
| `art-gate-decision` | Record the human's decision on a challenged art-level artifact that is not a backlog item (backlog items move with their transition workflow). | `gate-decision` | `release-train-engineer` | — | 1 |

### Team: `scrum-master`

| Workflow | Purpose | Gate artifact | Author | Challenge panel | Steps |
|---|---|---|---|---|---|
| `team-formation` | Define or revise one Agile team: its mission, members, working agreements, Definition of Done and Kanban. | `team-charter` | `scrum-master` | `agile-coach`, `product-owner`, `quality-engineer` | 5 |
| `story-refinement` | Write or thicken one Story so it is ready for Iteration Planning: user voice, acceptance criteria and an estimate. | `story` | `product-owner` | `software-engineer`, `quality-engineer`, `security-expert`, `ux-designer` | 6 |
| `iteration-planning` | Plan one iteration: the iteration goals, the Stories selected and the capacity behind them. | `iteration-plan` | `scrum-master` | `product-owner`, `software-engineer`, `quality-engineer` | 5 |
| `story-implementation` | Implement one ready Story test-first in its code repository and record the change with its evidence; experts review it before the human merges. | `code-change` | `software-engineer` | `quality-engineer`, `security-expert`, `observability-engineer`, `database-administrator`, `accessibility-specialist` | 7 |
| `team-sync` | Inspect progress toward the iteration goals, adjust the plan for the coming day, and re-render the Team Kanban. | `event-record` | `scrum-master` | — | 2 |
| `iteration-review` | Inspect the iteration increment with stakeholders, assess progress toward the iteration goals and PI Objectives, and adjust the Team Backlog. | `event-record` | `scrum-master` | — | 1 |
| `iteration-retrospective` | Review the team's practices at the end of the iteration and choose the improvements to try next. | `event-record` | `scrum-master` | — | 1 |
| `story-transition` | Record the human's decision to move one Story to a new Team Kanban state, then re-render the Team Kanban. | `story` | `product-owner` | — | 2 |
| `team-gate-decision` | Record the human's decision on a challenged team-level artifact that is not a backlog item (backlog items move with their transition workflow). | `gate-decision` | `scrum-master` | — | 1 |

## Artifact kinds

31 kinds. A **main** is owner-authored, challenged by experts and decided by a human; a **challenge** is an expert's packet; a **record** is a flow record.

| Kind | Class | Layer | Owner | Workspace path | Purpose |
|---|---|---|---|---|---|
| `challenge` | challenge | Shared | the challenging expert | `<folder of the challenged artifact>/challenges/<workflow-slug>-<agent-slug>.challenge.md` | One expert's challenge of one main artifact, written before the human gate. Findings only: the expert never edits the artifact it challenges. |
| `gate-decision` | record | Shared | the layer's orchestrator | `<layer scope>/decisions/<decision-slug>.gate-decision.md` | The human's decision at a gate, recorded by the orchestrator so that human oversight is committed evidence. |
| `event-record` | record | Shared | the layer's orchestrator | `<layer scope>/events/<event-slug>.<event>.md` | The record of one SAFe event, written by its facilitator: what was inspected, what was decided, who does what next. |
| `kanban` | record | Shared | the layer's orchestrator | `portfolio/portfolio-kanban.md`<br>`portfolio/solution-trains/<solution-train-slug>/solution-train-kanban.md`<br>`portfolio/arts/<art-slug>/art-kanban.md`<br>`portfolio/arts/<art-slug>/teams/<team-slug>/team-kanban.md` | The rendered board of one backlog: which item is in which state. Rendered from the items' `status`; the items stay the source of truth. |
| `strategic-themes` | main | Portfolio | `portfolio-manager` | `portfolio/strategic-themes.md` | The portfolio's business objectives that connect it to the enterprise strategy, stated as Objectives and Key Results. |
| `portfolio-vision` | main | Portfolio | `portfolio-manager` | `portfolio/portfolio-vision.md` | The future state of the portfolio's value streams and solutions: aspirational, yet realistic and achievable. |
| `value-stream` | main | Portfolio | `portfolio-manager` | `portfolio/value-streams/<value-stream-slug>/<value-stream-slug>.value-stream.md` | The definition of one development value stream: what triggers it, the solutions it builds, the trains that realize it, and how it is measured. |
| `epic` | main | Portfolio | `epic-owner` | `portfolio/epics/<epic-slug>/<epic-slug>.epic.md` | A significant solution development initiative, stated as a hypothesis and steered through the Portfolio Kanban with an MVP. |
| `lean-business-case` | main | Portfolio | `epic-owner` | `portfolio/epics/<epic-slug>/<epic-slug>.lean-business-case.md` | The case for an Epic in the analyzing state: its MVP, cost estimate and projected value, ending in a go or no-go recommendation. |
| `portfolio-roadmap` | main | Portfolio | `portfolio-manager` | `portfolio/portfolio-roadmap.md` | An aggregated multi-year view of how the Portfolio Vision will be achieved across the value streams. |
| `lean-budgets` | main | Portfolio | `portfolio-manager` | `portfolio/lean-budgets.md` | The portfolio budget allocated to value streams instead of projects, with the guardrails that govern spending. |
| `architecture-vision` | main | Portfolio | `enterprise-architect` | `portfolio/architecture-vision.md` | The portfolio's technology vision, strategy and roadmap, and the architectural runway it asks for. |
| `solution-train-canvas` | main | Large Solution | `solution-train-engineer` | `portfolio/solution-trains/<solution-train-slug>/solution-train-canvas.md` | The charter of a Solution Train: its mission, the solution it builds, its ARTs and suppliers, roles and cadence. |
| `solution-vision` | main | Large Solution | `solution-manager` | `portfolio/solution-trains/<solution-train-slug>/solution-vision.md` | The future state of the large solution: a reflection of customer and stakeholder needs and the proposed solution. |
| `solution-roadmap` | main | Large Solution | `solution-manager` | `portfolio/solution-trains/<solution-train-slug>/solution-roadmap.md` | The schedule of events and milestones that forecasts the planned solution deliverables over a time horizon. |
| `solution-intent` | main | Large Solution | `solution-architect` | `portfolio/solution-trains/<solution-train-slug>/solution-intent.md` | The repository of knowledge about current and intended solution behavior and design: fixed and variable specifications, models, tests and traceability. |
| `capability` | main | Large Solution | `solution-manager` | `portfolio/solution-trains/<solution-train-slug>/capabilities/<capability-slug>/<capability-slug>.capability.md` | Large solution functionality whose implementation often spans multiple ARTs and is sized to be delivered within a PI. |
| `supplier-agreement` | main | Large Solution | `procurement-manager` | `portfolio/solution-trains/<solution-train-slug>/suppliers/<supplier-slug>/<supplier-slug>.supplier-agreement.md` | The working agreement with a supplier of solution components, subsystems or services: scope, collaboration on the train's cadence, acceptance and terms. |
| `pi-objectives` | main | ART | `release-train-engineer`, `solution-train-engineer` | `portfolio/arts/<art-slug>/pis/<pi-slug>/pi-objectives.md`<br>`portfolio/solution-trains/<solution-train-slug>/pis/<pi-slug>/pi-objectives.md` | The business and technical goals a train intends to achieve in the upcoming PI, committed or uncommitted, with the plan that supports them. |
| `art-canvas` | main | ART | `release-train-engineer` | `portfolio/arts/<art-slug>/art-canvas.md` | The charter of an Agile Release Train: its mission, solutions, teams, roles and cadence. |
| `product-vision` | main | ART | `product-manager` | `portfolio/arts/<art-slug>/product-vision.md` | The future state of the solution the ART develops: customer needs and the features proposed to meet them. |
| `product-roadmap` | main | ART | `product-manager` | `portfolio/arts/<art-slug>/product-roadmap.md` | The ART's roadmap: the committed PI and a forecast of the next two. |
| `feature` | main | ART | `product-manager`, `system-architect` | `portfolio/arts/<art-slug>/features/<feature-slug>/<feature-slug>.feature.md` | Solution functionality that delivers business value, fulfills a stakeholder need, and is sized to be delivered by an ART within a PI. |
| `adr` | main | ART | `system-architect` | `portfolio/arts/<art-slug>/adrs/<adr-slug>/<adr-slug>.adr.md` | One architecture decision that extends the architectural runway: the context, the options kept open, the decision and its consequences. |
| `nfrs` | main | ART | `system-architect` | `portfolio/arts/<art-slug>/nfrs.md` | The ART's register of system qualities that constrain the backlog: each one measurable and verifiable. |
| `delivery-pipeline` | main | ART | `devops-engineer` | `portfolio/arts/<art-slug>/delivery-pipeline.md` | The map of the ART's Continuous Delivery Pipeline: the workflows, activities and automation from ideation to an on-demand release, with its bottlenecks. |
| `release` | main | ART | `release-manager` | `portfolio/arts/<art-slug>/releases/<release-slug>/<release-slug>.release.md` | The plan and readiness record of one release: what is made available to which customers, when, and with what evidence. |
| `team-charter` | main | Team | `scrum-master` | `portfolio/arts/<art-slug>/teams/<team-slug>/team-charter.md` | The charter of an Agile team: its mission, members, working agreements, Definition of Done and Kanban. |
| `story` | main | Team | `product-owner` | `portfolio/arts/<art-slug>/teams/<team-slug>/stories/<story-slug>/<story-slug>.story.md` | A short description of a small piece of desired functionality written from the user's perspective, small enough for one iteration. |
| `iteration-plan` | main | Team | `scrum-master` | `portfolio/arts/<art-slug>/teams/<team-slug>/iterations/<iteration-slug>/iteration-plan.md` | The team's plan for one iteration: its goals, the Stories it selected and the capacity behind them. |
| `code-change` | main | Team | `software-engineer` | `portfolio/arts/<art-slug>/teams/<team-slug>/stories/<story-slug>/<story-slug>.code-change.md` | The record of the change that implements one Story: what changed, where, and the evidence that it meets the Definition of Done. |
