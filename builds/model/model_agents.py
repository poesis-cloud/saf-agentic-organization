# Copyright 2026 Poesis Cloud and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The roster: every agent of the organization with its title, group, home layer and SAFe anchor.

Each entry is (slug, title, group, layer, description, SAFe anchor). The prose of an agent
(`agents/<slug>.agent.md`) and its craft skill (`skills/<slug>.skill.md`) are hand-written.
"""

ORCH, ROLE, EXPERT = "orchestrator", "safe-role", "expert"

AGENTS = [
    # --- orchestrators: one per SAFe layer -------------------------------------------------
    ("value-management-officer", "Value Management Officer", ORCH, "portfolio",
     "Portfolio orchestrator. Facilitates Lean Portfolio Management for Portfolio Leadership: maps a portfolio concern to one workflow, dispatches its steps, and brings the challenged artifacts to the human gate.",
     "Value Management Office (VMO): the function that facilitates the Lean Portfolio Management process and fosters operational excellence and lean governance."),
    ("solution-train-engineer", "Solution Train Engineer", ORCH, "solution",
     "Large Solution orchestrator. Facilitates Solution Train events and coordinates ARTs and suppliers: maps a solution concern to one workflow, dispatches its steps, and brings the challenged artifacts to the human gate.",
     "Solution Train Engineer (STE): servant leader and coach who facilitates Solution Train events and processes, coordinates the work of ARTs and Suppliers."),
    ("release-train-engineer", "Release Train Engineer", ORCH, "art",
     "ART orchestrator. Facilitates ART events and flow: maps an ART concern to one workflow, dispatches its steps, and brings the challenged artifacts to the human gate.",
     "Release Train Engineer (RTE): servant leader and ART coach who facilitates ART events and processes, and supports teams in delivering value."),
    ("scrum-master", "Scrum Master / Team Coach", ORCH, "team",
     "Team orchestrator. Facilitates team events and flow: maps a team concern to one workflow, dispatches its steps, and brings the challenged artifacts to the human gate.",
     "Scrum Master/Team Coach (SM/TC): servant leader and coach for an Agile team who facilitates team events and processes."),
    # --- SAFe roles: the authors of the main artifacts -------------------------------------
    ("portfolio-manager", "Portfolio Manager", ROLE, "portfolio",
     "Lean Portfolio Management author. Drafts Strategic Themes, the Portfolio Vision and canvas, the Portfolio Roadmap, Lean Budgets with their guardrails, and value stream definitions for Portfolio Leadership to decide.",
     "Lean Portfolio Management (LPM): aligns strategy and execution through strategy and investment funding, Agile portfolio operations, and lean governance. Portfolio Leadership (the human) decides."),
    ("epic-owner", "Epic Owner", ROLE, "portfolio",
     "Epic author. Defines the Epic hypothesis, its Lean Business Case and MVP, shepherds the Epic through the Portfolio Kanban, and evaluates the MVP for the pivot-or-persevere decision.",
     "Epic Owner: responsible for coordinating epics through the portfolio Kanban system; defines the Epic, the Lean business case, and the MVP."),
    ("enterprise-architect", "Enterprise Architect", ROLE, "portfolio",
     "Portfolio technology author and challenger. Writes the Architecture Vision (technology vision, strategy and roadmap) and challenges portfolio artifacts for architectural runway, reuse and technical feasibility.",
     "Enterprise Architect: responsible for establishing the portfolio's technology vision, strategy, and roadmap; typically acts as Epic Owner for enabler epics."),
    ("business-owner", "Business Owner", ROLE, "portfolio",
     "Business value challenger. Prepares the Business Owner's view (return on investment, governance, compliance, risk trade-offs, proposed business value of PI Objectives) so the human Business Owners can decide fast.",
     "Business Owners (BOs): key ART stakeholders with the primary business and technical responsibility for return on investment (ROI), governance, and compliance."),
    ("solution-manager", "Solution Manager", ROLE, "solution",
     "Large Solution content author. Writes the Solution Vision, Solution Roadmap and Capabilities, and owns the Solution Train Backlog content.",
     "Solution Management: the function responsible for defining desirable, viable, feasible, and sustainable large solutions; responsible for the Solution Train backlog."),
    ("solution-architect", "Solution Architect", ROLE, "solution",
     "Large Solution technical author and challenger. Writes the Solution Intent (fixed and variable, interfaces, NFRs, compliance) and challenges solution artifacts for technical direction across ARTs and suppliers.",
     "Solution Architect: responsible for defining and communicating a shared technical and architectural vision for a Solution Train."),
    ("product-manager", "Product Manager", ROLE, "art",
     "ART content author. Writes the Product Vision, the PI Roadmap and business Features with benefit hypothesis, acceptance criteria and WSJF, and owns the ART Backlog content.",
     "Product Management: the function responsible for defining desirable, viable, feasible, and sustainable solutions; responsible for the ART backlog."),
    ("system-architect", "System Architect", ROLE, "art",
     "ART technical author and challenger. Writes enabler Features, architecture decisions and the NFR register, and challenges ART artifacts for architecture, runway and NFR impact.",
     "System Architect: responsible for defining and communicating a shared technical and architectural vision for the solutions developed by an ART; defines enablers and outlines NFRs."),
    ("product-owner", "Product Owner", ROLE, "team",
     "Team content author. Writes Stories with acceptance criteria, owns the Team Backlog content, and records story acceptance against the Definition of Done.",
     "Product Owner (PO): the Agile team member primarily responsible for maximizing the value delivered by the team; content authority for the team backlog."),
    # --- expert bench: real IT jobs (SAFe Shared Services, System Team, Agile Team skills) --
    ("software-engineer", "Software Engineer", EXPERT, "team",
     "Builds the change. Implements Stories with test-first practice and records the code change; challenges backlog items and plans for feasibility, size, and design simplicity.",
     "Agile Team member (Builder): defines, builds, tests and delivers value with built-in quality."),
    ("quality-engineer", "Quality Engineer", EXPERT, "team",
     "Test and quality specialist. Challenges acceptance criteria, NFRs, plans and code changes for testability, test evidence and the Definition of Done.",
     "Agile Team member: Agile testing and built-in quality (BDD, TDD, automated tests)."),
    ("devops-engineer", "DevOps Engineer", EXPERT, "art",
     "Pipeline specialist. Maps and improves the Continuous Delivery Pipeline (build, test, stage, deploy automation) and challenges enablers for deployability.",
     "System Team: builds and supports the Agile development environment and the Continuous Delivery Pipeline."),
    ("platform-engineer", "Platform Engineer", EXPERT, "art",
     "Infrastructure and platform specialist. Challenges architecture and enablers for environments, infrastructure as code, capacity, tenancy and platform reuse.",
     "System Team / Shared Services: platforms and environments."),
    ("site-reliability-engineer", "Site Reliability Engineer", EXPERT, "art",
     "Reliability specialist. Challenges designs, NFRs and releases for service level objectives, failure modes, capacity, rollback and incident readiness.",
     "Shared Services: operational reliability (Continuous Deployment: Deploy, Verify, Monitor, Respond)."),
    ("observability-engineer", "Observability Engineer", EXPERT, "art",
     "Telemetry specialist. Challenges enablers, NFRs, code changes and releases for logs, metrics, traces, alerting and the ability to measure the benefit hypothesis in production.",
     "Shared Services: monitoring and measurement (Continuous Deployment: Monitor; Release on Demand: Measure)."),
    ("database-administrator", "Database Administrator", EXPERT, "team",
     "Operational data specialist. Challenges code changes for schema migrations, query performance, data integrity, backup and restore.",
     "Shared Services: database administration."),
    ("data-engineer", "Data Engineer", EXPERT, "art",
     "Data platform specialist. Challenges architecture for data models, pipelines, lineage, quality, retention and analytical needs.",
     "Shared Services: data engineering (Big Data practices)."),
    ("ai-engineer", "AI Engineer", EXPERT, "art",
     "AI and machine learning specialist. Challenges architecture decisions and NFRs for model choice, evaluation, data needs, cost, and Responsible AI (trustworthy, explainable, human-centric).",
     "Shared Services: AI expertise on the ART (the lens SAFe assigns to the AI Value Architect and Responsible AI practices)."),
    ("security-expert", "Security Expert", EXPERT, "art",
     "Application and architecture security specialist. Challenges business cases, intents, backlog items, decisions, code changes and releases for threats, trust boundaries, identity, secrets and abuse cases.",
     "Shared Services: security (DevSecOps)."),
    ("data-protection-officer", "Data Protection Officer", EXPERT, "portfolio",
     "Privacy specialist. Challenges business cases, solution intent and Features for lawful basis, data minimization, retention, data subject rights and the need for an impact assessment.",
     "Shared Services: privacy and data protection compliance."),
    ("compliance-officer", "Compliance Officer", EXPERT, "solution",
     "Regulatory and standards specialist. Challenges capabilities, solution intent and supplier agreements for applicable regulations, standards and the objective evidence they require.",
     "Compliance: activities and artifacts that let teams apply Lean-Agile methods while meeting regulatory and industry standards (Lean QMS)."),
    ("legal-counsel", "Legal Counsel", EXPERT, "portfolio",
     "Legal specialist. Challenges business cases and supplier agreements for contractual exposure, liability, licensing, intellectual property and Agile contract terms.",
     "Shared Services: legal (Agile contracts, supplier relationships)."),
    ("financial-controller", "Financial Controller", EXPERT, "portfolio",
     "Finance specialist. Challenges themes, business cases, roadmaps, budgets and agreements for cost realism, funding by value stream, CapEx and OpEx treatment and guardrail compliance.",
     "Lean Governance: oversight of spending, audit, compliance, expenditure, measurement, and reporting."),
    ("finops-engineer", "FinOps Engineer", EXPERT, "art",
     "Cloud cost specialist. Challenges budgets, architecture and pipelines for run cost, unit economics, cost attribution and waste.",
     "Shared Services: cloud financial management (economic view of technical choices)."),
    ("ux-designer", "UX Designer", EXPERT, "art",
     "User experience specialist. Challenges visions, Features and Stories for user outcomes, Lean UX hypotheses, journeys and usability.",
     "Shared Services: user experience (Design Thinking, Lean UX)."),
    ("accessibility-specialist", "Accessibility Specialist", EXPERT, "art",
     "Accessibility specialist. Challenges NFRs and code changes for conformance to accessibility standards and inclusive design.",
     "Shared Services: accessibility (inclusiveness is a Responsible AI and customer-centricity attribute)."),
    ("business-analyst", "Business Analyst", EXPERT, "portfolio",
     "Business process specialist. Challenges the Portfolio Vision, value streams and train canvases for operational value stream fit, process impact and stakeholder coverage.",
     "Shared Services: business analysis (operational value streams, customer and stakeholder needs)."),
    ("data-analyst", "Data Analyst", EXPERT, "portfolio",
     "Measurement specialist. Challenges themes, Epics, MVP evaluations and Inspect and Adapt records for measurable outcomes, leading indicators and sound evidence.",
     "Measure and Grow: outcomes, flow and competency measured with data (OKRs, KPIs, flow metrics)."),
    ("systems-engineer", "Systems Engineer", EXPERT, "solution",
     "Large-system specialist. Challenges solution roadmaps, intent, capabilities and Solution Train plans for interfaces, set-based design, verification and validation and integration risk.",
     "Large Solution practices: Model-Based Systems Engineering, Set-Based Design, frequent integration."),
    ("release-manager", "Release Manager", EXPERT, "art",
     "Release specialist. Writes the Release plan and readiness record for Release on Demand and challenges roadmaps for release feasibility and market timing.",
     "Release on Demand: making new functionality available to customers, decoupled from deployment; release governance."),
    ("technical-writer", "Technical Writer", EXPERT, "art",
     "Documentation specialist. Challenges releases for user documentation, release notes, runbooks and enablement material.",
     "Shared Services: documentation and customer training."),
    ("product-marketing-manager", "Product Marketing Manager", EXPERT, "art",
     "Go-to-market specialist. Challenges roadmaps and visions for market rhythms, positioning, launch readiness and customer messaging.",
     "Product Marketing: go-to-market alignment with Product Management."),
    ("procurement-manager", "Procurement Manager", EXPERT, "solution",
     "Supplier specialist. Writes supplier agreements that bring suppliers into the Solution Train's cadence and quality expectations.",
     "Supplier relationships: internal or external organizations that deliver components, subsystems or services to ARTs and value streams (Lean-Agile procurement)."),
    ("agile-coach", "Agile Coach", EXPERT, "portfolio",
     "Lean-Agile practice specialist. Challenges value streams, canvases, team charters and Inspect and Adapt records for flow, team design, and conformance to SAFe principles.",
     "Lean-Agile Center of Excellence (LACE) / SAFe Practice Consultant: coaching and relentless improvement."),
]

AGENT = {a[0]: dict(slug=a[0], title=a[1], group=a[2], layer=a[3], description=a[4], anchor=a[5]) for a in AGENTS}
ORCHESTRATORS = {a[3]: a[0] for a in AGENTS if a[2] == ORCH}
