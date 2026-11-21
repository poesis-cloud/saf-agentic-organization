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

"""The artifact catalog: every kind with its frontmatter fields, body sections and owners.

`generate.py` turns each kind into a JSON Schema (`artifacts/`) and a template (`templates/`).
"""

# ---- tiny schema DSL ---------------------------------------------------------------------

def s(desc, sample="<text>", **kw):
    return dict(schema={"type": "string", "minLength": 1, "description": desc, **kw}, sample=sample)

def path(desc, sample):
    return dict(schema={"type": "string", "minLength": 1, "description": desc + " Workspace-relative path."}, sample=sample)

def opt_path(desc, sample=None):
    return dict(schema={"type": ["string", "null"], "description": desc + " Workspace-relative path, or null."}, sample=sample)

def opt_s(desc, sample=None):
    return dict(schema={"type": ["string", "null"], "description": desc}, sample=sample)

def e(desc, values, sample=None):
    return dict(schema={"description": desc + " One of: " + " | ".join(str(v) for v in values) + ".", "enum": list(values)},
                sample=values[0] if sample is None else sample, options=values)

def opt_e(desc, values, sample=None):
    return dict(schema={"description": desc + " One of: " + " | ".join(str(v) for v in values) + ", or null.", "enum": [*values, None]},
                sample=sample, options=[*values, "null"])

def num(desc, sample=0):
    return dict(schema={"type": "number", "description": desc}, sample=sample)

def opt_num(desc, sample=None):
    return dict(schema={"type": ["number", "null"], "description": desc}, sample=sample)

def b(desc, sample=False):
    return dict(schema={"type": "boolean", "description": desc}, sample=sample)

def strs(desc, sample=None):
    return dict(schema={"type": "array", "description": desc, "items": {"type": "string", "minLength": 1}}, sample=sample or [])

def objs(desc, props, required, sample=None):
    return dict(schema={"type": "array", "description": desc, "items": {
        "type": "object", "additionalProperties": True, "required": required,
        "properties": {k: v["schema"] for k, v in props.items()}}}, sample=sample or [])

def ref(name, desc, sample):
    return dict(schema={"description": desc, "$ref": f"#/$defs/{name}"}, sample=sample)

# ---- shared definitions (canonical copy lives in artifacts/framework-definitions.schema.json)

DEFS = {
    "stepOutcomes": {
        "description": "Step outcome record. Every workflow step that commits this artifact appends exactly one entry, so the artifact itself carries the step's decision and the agent's reply stays indicative.",
        "type": "array",
        "items": {
            "type": "object", "additionalProperties": True,
            "required": ["step", "outcome", "date", "note"],
            "properties": {
                "step": {"description": "`<workflow-slug>/<step-slug>` of the step that appended this entry.", "type": "string", "pattern": "^[a-z0-9-]+/[a-z0-9-]+$"},
                "outcome": {"description": "written (created) | revised (content changed) | confirmed (reviewed, still valid) | no-change (out of scope on this run) | none (not needed; the artifact records that decision).", "enum": ["written", "revised", "confirmed", "no-change", "none"]},
                "date": {"description": "YYYY-MM-DD of the step.", "type": "string", "minLength": 1},
                "note": {"description": "One line: what the step decided and why.", "type": "string", "minLength": 1},
                "friction": {"description": "Optional. Workflow friction the actor observed (raw input for Inspect and Adapt, never a fix).", "type": "string"},
            },
        },
    },
    "challengeLedger": {
        "description": "The owner's answer to the expert challenge. One entry per challenge packet of the latest run, written by the owner in the `revise` step: every finding is accepted, rejected or deferred with a reason. The human gate reads this ledger next to the artifact.",
        "type": "array",
        "items": {
            "type": "object", "additionalProperties": True,
            "required": ["packet", "challenger", "verdict", "responses"],
            "properties": {
                "packet": {"description": "Workspace-relative path of the challenge packet answered.", "type": "string", "minLength": 1},
                "challenger": {"description": "Agent slug of the expert who wrote the packet.", "type": "string", "minLength": 1},
                "verdict": {"description": "The packet's verdict, copied: pass | concerns | blocking | not-applicable.", "enum": ["pass", "concerns", "blocking", "not-applicable"]},
                "responses": {
                    "description": "One response per finding of the packet (empty when the packet has no finding).",
                    "type": "array",
                    "items": {
                        "type": "object", "additionalProperties": True,
                        "required": ["finding", "disposition", "note"],
                        "properties": {
                            "finding": {"description": "Finding id in the packet, e.g. F1.", "type": "string", "minLength": 1},
                            "disposition": {"description": "accepted (the artifact changed) | rejected (the owner disagrees, with the reason) | deferred (valid, handled later: say where).", "enum": ["accepted", "rejected", "deferred"]},
                            "note": {"description": "One line: what changed, or why not.", "type": "string", "minLength": 1},
                        },
                    },
                },
            },
        },
    },
    "wsjf": {
        "description": "Weighted Shortest Job First: relative cost of delay divided by relative job size. Each component is a relative estimate on the modified Fibonacci scale (1, 2, 3, 5, 8, 13, 20, 40, 100); 0 means not estimated yet.",
        "type": "object", "additionalProperties": True,
        "required": ["userBusinessValue", "timeCriticality", "riskReductionOpportunityEnablement", "jobSize", "score"],
        "properties": {
            "userBusinessValue": {"description": "Relative user and business value.", "type": "number"},
            "timeCriticality": {"description": "How the value decays with delay.", "type": "number"},
            "riskReductionOpportunityEnablement": {"description": "Risk reduction and/or opportunity enablement.", "type": "number"},
            "jobSize": {"description": "Relative job size (duration proxy), the denominator.", "type": "number"},
            "score": {"description": "(userBusinessValue + timeCriticality + riskReductionOpportunityEnablement) / jobSize; 0 while not estimated.", "type": "number"},
        },
    },
    "transitions": {
        "description": "Kanban history. One entry per state change, appended by the owner in a `*-transition` workflow after the human decided.",
        "type": "array",
        "items": {
            "type": "object", "additionalProperties": True,
            "required": ["from", "to", "date", "decidedBy", "reason"],
            "properties": {
                "from": {"description": "State left.", "type": "string", "minLength": 1},
                "to": {"description": "State entered.", "type": "string", "minLength": 1},
                "date": {"description": "YYYY-MM-DD.", "type": "string", "minLength": 1},
                "decidedBy": {"description": "The human (name or role) who decided.", "type": "string", "minLength": 1},
                "reason": {"description": "One line: why.", "type": "string", "minLength": 1},
            },
        },
    },
}

WSJF_SAMPLE = {"userBusinessValue": 0, "timeCriticality": 0, "riskReductionOpportunityEnablement": 0, "jobSize": 0, "score": 0}
ENABLER_TYPES = ["exploration", "architecture", "infrastructure", "compliance"]
FLOW_STATES = ["funnel", "analyzing", "ready", "implementing", "validating-on-staging", "deploying-to-production", "releasing", "done"]
EPIC_STATES = ["funnel", "reviewing", "analyzing", "ready", "implementing", "done"]
STORY_STATES = ["backlog", "ready", "in-progress", "in-review", "accepted"]

def main_fields(owner):
    return {
        "owner": s("Agent slug of the owning author. Only the owner writes this artifact.", owner),
        "challengeLedger": ref("challengeLedger", "The owner's answers to the expert challenge (see the definition).", []),
    }

def work_item_fields(states, first):
    return {
        "status": e("Kanban state. Changed only by the owner in the `*-transition` workflow, after the human decided.", states, first),
        "blocked": b("True while an impediment stops the item; say why under `## Open questions`."),
        "wsjf": ref("wsjf", "WSJF prioritization block.", WSJF_SAMPLE),
        "transitions": ref("transitions", "Kanban history.", []),
    }

def S(title, guide, required=False):
    return dict(title=title, guide=guide, required=required)

# ---- kinds -------------------------------------------------------------------------------
# cls: main (owner-authored, challenged, human-gated) | challenge | record (flow record)

KINDS = {}

def kind(slug, title, layer, cls, owners, purpose, fields, sections, defs=()):
    KINDS[slug] = dict(slug=slug, title=title, layer=layer, cls=cls, owners=list(owners), purpose=purpose,
                       fields=fields, sections=sections, defs=["stepOutcomes", *defs])

# -- shared ---------------------------------------------------------------------------------

kind("challenge", "Challenge packet", "shared", "challenge", [],
     "One expert's challenge of one main artifact, written before the human gate. Findings only: the expert never edits the artifact it challenges.",
     {
         "target": path("The main artifact challenged.", "<path of the challenged artifact>"),
         "targetKind": s("Artifact kind of the target.", "<artifact-kind>"),
         "challenger": s("Agent slug of the expert.", "<agent-slug>"),
         "verdict": e("pass: no finding. concerns: findings the owner should answer. blocking: the artifact should not pass the gate as is. not-applicable: the lens does not apply, with the reason in `## Summary`.",
                      ["pass", "concerns", "blocking", "not-applicable"]),
         "findings": objs("Findings, most severe first. Empty when the verdict is pass or not-applicable.",
                          {"id": s("F1, F2, …"), "severity": e("Severity.", ["blocking", "major", "minor"]),
                           "claim": s("What is wrong or missing, in one sentence."),
                           "evidence": s("Where it shows: the section, field or source that proves the claim."),
                           "ask": s("The smallest change that would resolve it.")},
                          ["id", "severity", "claim", "evidence", "ask"]),
     },
     [S("Summary", "Two or three sentences: what you checked through your lens and your verdict. If not applicable, say why in one sentence.", True),
      S("Findings", "One short paragraph per finding id when the frontmatter line is not enough. Omit when there is no finding."),
      S("Questions for the human gate", "Only what a human must decide (a trade-off, a risk appetite). Omit when there is none.")])

kind("gate-decision", "Gate decision", "shared", "record", [],
     "The human's decision at a gate, recorded by the orchestrator so that human oversight is committed evidence.",
     {
         "target": path("The main artifact decided on.", "<path of the artifact decided on>"),
         "targetKind": s("Artifact kind of the target.", "<artifact-kind>"),
         "decision": e("The human's decision.", ["accepted", "accepted-with-concerns", "rejected"]),
         "decidedBy": s("The human (name or role) who decided.", "<name or role>"),
         "date": s("YYYY-MM-DD of the decision.", "YYYY-MM-DD"),
         "concerns": strs("The human's concerns or conditions, in their words. Empty when none."),
     },
     [S("Decision", "The decision in one sentence, in the human's words.", True),
      S("Rationale", "Why, as the human stated it. Do not add your own reasons."),
      S("Follow-ups", "What must happen next and in which workflow (e.g. a rejection reiterates the authoring workflow).")])

EVENTS = ["portfolio-sync", "strategic-portfolio-review", "pre-plan", "coordinate-and-deliver", "solution-demo",
          "art-sync", "system-demo", "inspect-and-adapt", "team-sync", "iteration-review", "iteration-retrospective"]

kind("event-record", "Event record", "shared", "record", [],
     "The record of one SAFe event, written by its facilitator: what was inspected, what was decided, who does what next.",
     {
         "event": e("The SAFe event recorded.", EVENTS),
         "date": s("YYYY-MM-DD of the event.", "YYYY-MM-DD"),
         "scope": path("The portfolio, Solution Train, ART or team folder the event belongs to.", "<path of the scope folder>"),
         "decisions": objs("Decisions taken, each with its owner.",
                           {"id": s("D1, D2, …"), "decision": s("The decision."), "owner": s("Agent slug or human role.")},
                           ["id", "decision", "owner"]),
         "actions": objs("Follow-up actions. An action that is really a backlog item names the workflow that will write it.",
                         {"id": s("A1, A2, …"), "action": s("What to do."), "owner": s("Agent slug or human role."), "workflow": opt_s("Workflow slug that carries it, or null.")},
                         ["id", "action", "owner"]),
         "impediments": strs("Open impediments and risks raised, one line each."),
         "challengeLedger": ref("challengeLedger", "Answers to the expert challenge, when the event's workflow has one (Inspect and Adapt).", []),
     },
     [S("Summary", "What the event inspected and concluded, in a few sentences.", True)],
     defs=("challengeLedger",))

kind("kanban", "Kanban board", "shared", "record", [],
     "The rendered board of one backlog: which item is in which state. Rendered from the items' `status`; the items stay the source of truth.",
     {
         "level": e("The backlog rendered.", ["portfolio", "solution-train", "art", "team"]),
         "scope": path("The folder whose backlog is rendered.", "<path of the scope folder>"),
         "updated": s("YYYY-MM-DD of the last rendering.", "YYYY-MM-DD"),
         "columns": objs("One entry per state, in flow order.",
                         {"state": s("State name."), "wipLimit": opt_num("Work-in-process limit, or null."), "items": strs("Paths of the items in this state.")},
                         ["state", "items"]),
     },
     [S("Board", "One line per state: the state, its WIP limit, the item titles. Flag a state over its limit.", True),
      S("Flow notes", "Bottlenecks, blocked items and aged items, one line each.")])

# -- portfolio ------------------------------------------------------------------------------

kind("strategic-themes", "Strategic Themes", "portfolio", "main", ["portfolio-manager"],
     "The portfolio's business objectives that connect it to the enterprise strategy, stated as Objectives and Key Results.",
     {
         **main_fields("portfolio-manager"),
         "horizon": s("The period the themes cover.", "<e.g. FY2027>"),
         "themes": objs("Strategic themes in OKR format: one objective, two to five key results each.",
                        {"id": s("ST1, ST2, …"), "objective": s("The business outcome to achieve."), "keyResults": strs("Measurable success criteria (two to five).")},
                        ["id", "objective", "keyResults"]),
     },
     [S("Business context", "The enterprise strategy input, the market, and what changed since the last revision.", True),
      S("Themes", "For each theme: why it differentiates, and what it changes in budgets, the vision and the backlog.", True),
      S("What we will not pursue", "The choices the themes exclude."),
      S("Influence on the portfolio", "How the themes shape value stream budgets, guardrails, the Portfolio Vision and Epic prioritization.")],
     defs=("challengeLedger",))

kind("portfolio-vision", "Portfolio Vision", "portfolio", "main", ["portfolio-manager"],
     "The future state of the portfolio's value streams and solutions: aspirational, yet realistic and achievable.",
     {**main_fields("portfolio-manager"), "horizon": s("The time horizon of the future state.", "<e.g. 3 years>")},
     [S("Vision statement", "A short, motivational description of the future state.", True),
      S("Portfolio canvas: current state", "Per development value stream: solutions, customers, channels, budget, KPIs and revenue; then key partners, activities, resources and cost structure.", True),
      S("Portfolio canvas: future state", "The same blocks, as they should be at the horizon.", True),
      S("Opportunities and threats", "A SWOT/TOWS reading that explains the chosen future state."),
      S("Path", "The Epics and changes that move the portfolio from the current to the future state.")],
     defs=("challengeLedger",))

kind("value-stream", "Development Value Stream", "portfolio", "main", ["portfolio-manager"],
     "The definition of one development value stream: what triggers it, the solutions it builds, the trains that realize it, and how it is measured.",
     {
         **main_fields("portfolio-manager"),
         "operationalValueStreams": strs("Operational value streams this development value stream supports."),
         "trains": objs("The Solution Trains and ARTs that realize the value stream.",
                        {"kind": e("Train kind.", ["solution-train", "art"]), "path": s("Path of the train folder.")}, ["kind", "path"]),
         "kpis": strs("Value stream KPIs (typically four to seven)."),
     },
     [S("Trigger and value", "What starts the flow and the value delivered at its end.", True),
      S("Solutions and customers", "The solutions built and the customers, internal or external, they serve.", True),
      S("People and trains", "The Solution Trains, ARTs and shared services, and how they map to the solutions."),
      S("KPIs", "How the value stream is evaluated against its business objectives."),
      S("Flow and bottlenecks", "Known delays, hand-offs and dependencies on other value streams.")],
     defs=("challengeLedger",))

kind("epic", "Epic", "portfolio", "main", ["epic-owner"],
     "A significant solution development initiative, stated as a hypothesis and steered through the Portfolio Kanban with an MVP.",
     {
         **main_fields("epic-owner"),
         "type": e("business: delivers customer value. enabler: extends the architectural runway or improves the value stream.", ["business", "enabler"]),
         **work_item_fields(EPIC_STATES, "funnel"),
         "implementationStage": opt_e("While implementing: mvp (testing the hypothesis) or persevere (hypothesis proven).", ["mvp", "persevere"]),
         "resolution": opt_e("Once done: how the Epic ended.", ["delivered", "no-go", "pivoted", "stopped"]),
         "strategicThemes": strs("Ids of the Strategic Themes the Epic serves."),
         "valueStreams": strs("Paths of the value streams impacted."),
         "leadingIndicators": strs("Early measures that predict the business outcome."),
     },
     [S("Epic hypothesis statement", "For <customers> who <do something>, the <solution> is a <something: the how> that <provides this value>. Unlike <the alternative>, our solution <does something better: the why>.", True),
      S("Business outcomes hypothesis", "The measurable benefits the business expects if the hypothesis holds.", True),
      S("Leading indicators", "The early measures and how they will be collected."),
      S("Nonfunctional requirements", "Qualities and constraints the Epic imposes or must respect."),
      S("Scope", "In scope, out of scope."),
      S("MVP", "The minimal version sufficient to prove or disprove the hypothesis; once run, the evidence and the pivot-or-persevere recommendation."),
      S("Open questions", "What is still unknown, who can answer, and the assumption taken meanwhile.")],
     defs=("challengeLedger", "wsjf", "transitions"))

kind("lean-business-case", "Lean Business Case", "portfolio", "main", ["epic-owner"],
     "The case for an Epic in the analyzing state: its MVP, cost estimate and projected value, ending in a go or no-go recommendation.",
     {
         **main_fields("epic-owner"),
         "epic": path("The Epic analyzed.", "portfolio/epics/<epic-slug>/<epic-slug>.epic.md"),
         "recommendation": e("The Epic Owner's recommendation to Portfolio Leadership.", ["pending", "go", "no-go"]),
         "mvpCostEstimate": opt_s("Estimated cost of the MVP, with its unit.", None),
         "implementationCostEstimate": opt_s("Forecast cost of the full implementation if the hypothesis is proven, with its unit.", None),
         "sponsors": strs("The human sponsors and Business Owners consulted."),
     },
     [S("Epic summary", "The hypothesis and business outcomes, restated in five lines.", True),
      S("Solution analysis", "Customers and users, impacted value streams, ARTs and solutions, and the alternatives considered.", True),
      S("MVP", "The MVP features, the hypothesis it tests and the measures that decide.", True),
      S("Cost estimate", "MVP cost, then forecast implementation cost. Budget only the period ahead: the full cost is not committed until the MVP hypothesis is proven.", True),
      S("Return", "The type of return and the expected benefits, tied to the leading indicators."),
      S("Development strategy", "Incremental path, sequencing, build or buy, suppliers."),
      S("Risks and dependencies", "What could invalidate the case."),
      S("Recommendation", "Go or no-go, and what Portfolio Leadership must decide.", True)],
     defs=("challengeLedger",))

kind("portfolio-roadmap", "Portfolio Roadmap", "portfolio", "main", ["portfolio-manager"],
     "An aggregated multi-year view of how the Portfolio Vision will be achieved across the value streams.",
     {**main_fields("portfolio-manager"), "horizon": s("The time horizon covered.", "<e.g. 2027-2029>"), "lastReviewed": s("YYYY-MM-DD of the last review.", "YYYY-MM-DD")},
     [S("Horizon overview", "The path from today to the Portfolio Vision in a few lines.", True),
      S("Near term", "Committed: Epics implementing or ready, by value stream and PI.", True),
      S("Mid term", "Forecast: Epics in analysis and expected solution milestones."),
      S("Long term", "Intent only: themes and bets, without dates that read as commitments."),
      S("Milestones and market events", "Fixed dates, regulatory deadlines, launches."),
      S("Assumptions and risks", "What the roadmap depends on.")],
     defs=("challengeLedger",))

kind("lean-budgets", "Lean Budgets", "portfolio", "main", ["portfolio-manager"],
     "The portfolio budget allocated to value streams instead of projects, with the guardrails that govern spending.",
     {
         **main_fields("portfolio-manager"),
         "budgetPeriod": s("The budgeting period (typically updated twice a year, about every two PIs).", "<e.g. 2027-H1>"),
         "totalBudget": s("The money available to fund the value streams, with its unit.", "<amount and unit>"),
         "epicThreshold": opt_s("The portfolio epic threshold: above it, an initiative needs Portfolio Leadership approval.", None),
         "valueStreamBudgets": objs("One entry per value stream.",
                                    {"valueStream": s("Path of the value stream."), "baselineSolutionInvestments": s("Cost to develop, support and operate what delivers current business capabilities."),
                                     "proposedSolutionInitiatives": s("Cost, in this period, of the Epics proposed above the threshold."), "total": s("Budget of the value stream for the period.")},
                                    ["valueStream", "baselineSolutionInvestments", "proposedSolutionInitiatives", "total"]),
     },
     [S("Business context", "Strategic Themes, Portfolio Vision and the state of the Portfolio Kanban that frame this budget.", True),
      S("Value stream budgets", "Per value stream: Baseline Solution Investments, Proposed Solution Initiatives, and the reasons.", True),
      S("Guardrails", "The four Lean budget guardrails as applied here: guiding investments by horizon; applying capacity allocation to optimize value and solution integrity; approving significant initiatives; continuous Business Owner engagement.", True),
      S("Forum insights", "What the Strategic Investment Planning forums funded, cut or left partially funded, and why. Forum results inform the decision; they do not make it."),
      S("Changes since the last period", "What moves, and what the value streams must prepare during the current PI.")],
     defs=("challengeLedger",))

kind("architecture-vision", "Architecture Vision", "portfolio", "main", ["enterprise-architect"],
     "The portfolio's technology vision, strategy and roadmap, and the architectural runway it asks for.",
     {**main_fields("enterprise-architect"), "horizon": s("The time horizon covered.", "<e.g. 3 years>"), "enablerEpics": strs("Paths of the enabler Epics this vision asks for.")},
     [S("Technology vision", "Where the portfolio's technology must be at the horizon, and why the business needs it.", True),
      S("Current state and constraints", "What exists, what limits it, what must be retired.", True),
      S("Target architecture and principles", "The intentional architecture and the few principles that guide emergent design.", True),
      S("Architectural runway", "The enabler Epics and capabilities that pave the way, in order."),
      S("Technology roadmap", "Sequencing by horizon, with the decisions that must be taken first."),
      S("Standards and guardrails", "The minimum governance: what is fixed, what is left to trains and teams."),
      S("Risks", "Technical and delivery risks, and the options kept open.")],
     defs=("challengeLedger",))

# -- large solution -------------------------------------------------------------------------

kind("solution-train-canvas", "Solution Train canvas", "solution", "main", ["solution-train-engineer"],
     "The charter of a Solution Train: its mission, the solution it builds, its ARTs and suppliers, roles and cadence.",
     {
         **main_fields("solution-train-engineer"),
         "valueStream": opt_path("The development value stream served."),
         "arts": strs("Paths of the member ART folders."),
         "suppliers": strs("Paths of the supplier agreements."),
         "piLengthWeeks": opt_num("Planning Interval length shared by the ARTs (typically 8 to 12 weeks)."),
     },
     [S("Mission", "The large solution built and the customers it serves.", True),
      S("ARTs and suppliers", "Who builds what, and the main interfaces between them.", True),
      S("Roles", "Solution Train Engineer, Solution Management, Solution Architect, and the humans who decide at the gates.", True),
      S("Cadence and events", "The common PI cadence, Pre-Plan, the syncs of Coordinate and Deliver, Solution Demo, Inspect and Adapt."),
      S("Shared services and System Team", "The specialists and integration support the trains rely on."),
      S("Working agreements", "How the trains integrate, escalate and decide.")],
     defs=("challengeLedger",))

kind("solution-vision", "Solution Vision", "solution", "main", ["solution-manager"],
     "The future state of the large solution: a reflection of customer and stakeholder needs and the proposed solution.",
     {**main_fields("solution-manager"), "horizon": s("The time horizon covered.", "<e.g. 2 years>")},
     [S("Vision statement", "For <customers> who <need>, the <solution> is a <category> that <key benefit>. Unlike <alternative>, our solution <differentiator>.", True),
      S("Customers and needs", "Who is served and the problems worth solving.", True),
      S("Solution context", "The environment the solution operates in: usage, installation, operation, support, interfaces.", True),
      S("Key capabilities", "The large behaviors that realize the vision."),
      S("Nonfunctional requirements and constraints", "Qualities, regulations and standards that shape the solution."),
      S("What it is not", "Explicit exclusions.")],
     defs=("challengeLedger",))

kind("solution-roadmap", "Solution Roadmap", "solution", "main", ["solution-manager"],
     "The schedule of events and milestones that forecasts the planned solution deliverables over a time horizon.",
     {**main_fields("solution-manager"), "horizon": s("The time horizon covered.", "<e.g. 2027-2028>"), "lastReviewed": s("YYYY-MM-DD of the last review.", "YYYY-MM-DD")},
     [S("PI roadmap", "Three PIs: the current one is committed, the next two are a forecast. Capabilities per PI.", True),
      S("Multi-year view", "Larger milestones beyond the PI roadmap, as intent.", True),
      S("Milestones, releases and fixed dates", "Integration points, Solution Demos, regulatory and supplier dates."),
      S("Assumptions and risks", "What the forecast depends on.")],
     defs=("challengeLedger",))

kind("solution-intent", "Solution Intent", "solution", "main", ["solution-architect"],
     "The repository of knowledge about current and intended solution behavior and design: fixed and variable specifications, models, tests and traceability.",
     {
         **main_fields("solution-architect"),
         "standards": strs("Applicable regulations and standards."),
         "capabilities": strs("Paths of the capabilities this intent constrains."),
     },
     [S("Solution context", "The environment, users and systems the solution must fit.", True),
      S("Fixed intent", "Non-negotiable requirements and design: what is known and must hold.", True),
      S("Variable intent", "What is still open to discussion and exploration, with the options kept alive and the date or learning that will close each.", True),
      S("System model and interfaces", "Components, their responsibilities, and the interfaces between ARTs and suppliers."),
      S("Nonfunctional requirements", "Solution-wide qualities with their measures."),
      S("Standards and compliance", "What must be evidenced, to whom, and how the evidence is produced as the solution is built."),
      S("Verification and validation", "The functional and nonfunctional tests that show the solution meets its intent."),
      S("Traceability", "From needs to capabilities to tests, at the grain compliance requires."),
      S("Decisions and trade studies", "Design reasoning and experiment results that moved intent from variable to fixed.")],
     defs=("challengeLedger",))

kind("capability", "Capability", "solution", "main", ["solution-manager"],
     "Large solution functionality whose implementation often spans multiple ARTs and is sized to be delivered within a PI.",
     {
         **main_fields("solution-manager"),
         "type": e("business or enabler.", ["business", "enabler"]),
         "enablerType": opt_e("For an enabler: its category.", ENABLER_TYPES),
         **work_item_fields(FLOW_STATES, "funnel"),
         "parent": opt_path("The portfolio Epic this capability splits from."),
         "targetPi": opt_s("PI slug the capability is planned for, or null."),
         "arts": strs("Paths of the ART folders expected to contribute."),
     },
     [S("Description", "What the capability is, in one paragraph.", True),
      S("Benefit hypothesis", "The measurable benefit expected for the customer or the business.", True),
      S("Acceptance criteria", "Independently testable criteria that cover the functionality and the relevant NFRs.", True),
      S("Nonfunctional requirements", "Solution Intent constraints that apply, and any tightening."),
      S("Feature split", "The Features each ART would take, as candidates."),
      S("Dependencies and suppliers", "Cross-ART and supplier dependencies."),
      S("Open questions", "What is still unknown, who can answer, and the assumption taken meanwhile.")],
     defs=("challengeLedger", "wsjf", "transitions"))

kind("supplier-agreement", "Supplier agreement", "solution", "main", ["procurement-manager"],
     "The working agreement with a supplier of solution components, subsystems or services: scope, collaboration on the train's cadence, acceptance and terms.",
     {
         **main_fields("procurement-manager"),
         "supplier": s("The supplier organization.", "<supplier name>"),
         "status": e("Agreement state.", ["draft", "negotiating", "active", "ended"]),
         "capabilities": strs("Paths of the capabilities the supplier contributes to."),
     },
     [S("Scope and deliverables", "The components, subsystems or services supplied.", True),
      S("Collaboration model", "How the supplier joins the cadence: Pre-Plan, PI Planning, syncs, Solution Demo, integration points.", True),
      S("Acceptance and quality", "Objective evaluation of working deliverables, quality expectations, compliance evidence owed.", True),
      S("Commercial terms", "Pricing model and how it tolerates variable scope."),
      S("Security, privacy and compliance", "Obligations passed to the supplier."),
      S("Intellectual property and licensing", "Ownership, licenses, open-source obligations."),
      S("Exit and continuity", "Termination, transition, continuity of service."),
      S("Risks", "Dependency and delivery risks.")],
     defs=("challengeLedger",))

kind("pi-objectives", "PI Objectives", "art", "main", ["release-train-engineer", "solution-train-engineer"],
     "The business and technical goals a train intends to achieve in the upcoming PI, committed or uncommitted, with the plan that supports them.",
     {
         **main_fields("release-train-engineer"),
         "scope": e("The train planned.", ["art", "solution-train"]),
         "pi": s("PI slug.", "<pi-slug>"),
         "confidenceVote": opt_num("Average confidence vote (1 to 5), recorded after the human commitment."),
         "objectives": objs("PI Objectives, per team or per ART.",
                            {"id": s("O1, O2, …"), "team": s("Team or ART slug that owns the objective."), "objective": s("The goal, stated as an outcome."),
                             "committed": b("False for an uncommitted objective."), "plannedBusinessValue": opt_num("1 to 10, assigned by the Business Owners (proposed until the gate)."),
                             "actualBusinessValue": opt_num("1 to 10, assigned at the end of the PI.")},
                            ["id", "team", "objective", "committed"]),
         "risks": objs("PI risks.", {"id": s("R1, R2, …"), "risk": s("What could prevent meeting the objectives."),
                                     "roam": e("ROAM state.", ["open", "resolved", "owned", "accepted", "mitigated"]), "owner": opt_s("Who owns it.")},
                       ["id", "risk", "roam"]),
     },
     [S("Business context", "The vision, roadmap and top backlog items presented for this PI.", True),
      S("Objectives", "Per team: committed objectives, then uncommitted ones, each traceable to backlog items.", True),
      S("Planning board", "Delivery iteration per Feature or capability, dependencies between teams or ARTs, milestones. Nothing is planned in the IP iteration.", True),
      S("Capacity and load", "Capacity per team and iteration against the planned load."),
      S("Risks", "ROAM: resolved, owned, accepted, mitigated."),
      S("Confidence vote", "The vote and the concerns raised, recorded after the human commitment.")],
     defs=("challengeLedger",))

# -- ART ------------------------------------------------------------------------------------

kind("art-canvas", "ART canvas", "art", "main", ["release-train-engineer"],
     "The charter of an Agile Release Train: its mission, solutions, teams, roles and cadence.",
     {
         **main_fields("release-train-engineer"),
         "valueStream": opt_path("The development value stream served."),
         "solutionTrain": opt_path("The Solution Train folder, when the ART belongs to one."),
         "teams": objs("The Agile teams of the ART (typically 5 to 15).",
                       {"slug": s("Team slug."), "topology": e("Team type.", ["stream-aligned", "complicated-subsystem", "platform", "enabling"])}, ["slug", "topology"]),
         "piLengthWeeks": opt_num("Planning Interval length (typically 8 to 12 weeks)."),
         "iterationLengthWeeks": opt_num("Iteration length (typically 2 weeks)."),
     },
     [S("Mission", "The solutions the ART develops, delivers and operates, and for whom.", True),
      S("Teams", "Each team's mission and type, and why the ART is organized this way.", True),
      S("ART leadership and roles", "Release Train Engineer, Product Management, System Architect, Business Owners (the humans who decide at the gates).", True),
      S("Cadence and events", "PI calendar: iterations, IP iteration, PI Planning, ART Sync, System Demo, Inspect and Adapt."),
      S("Shared services and System Team", "The specialists and pipeline support the teams rely on."),
      S("Working agreements", "ART-level Definition of Done, integration and release policies.")],
     defs=("challengeLedger",))

kind("product-vision", "Product Vision", "art", "main", ["product-manager"],
     "The future state of the solution the ART develops: customer needs and the features proposed to meet them.",
     {**main_fields("product-manager"), "horizon": s("The time horizon covered.", "<e.g. 12 months>")},
     [S("Vision statement", "For <customers> who <need>, the <product> is a <category> that <key benefit>. Unlike <alternative>, our product <differentiator>.", True),
      S("Customers and personas", "Who is served; the personas and their jobs to be done.", True),
      S("Problems and needs", "The problems worth solving, with the evidence.", True),
      S("Solution context", "Where and how the product is used, deployed, operated and supported."),
      S("Key features", "Candidate features that realize the vision, not yet a backlog."),
      S("Nonfunctional requirements", "Qualities the product must have."),
      S("Measures of success", "The outcomes that will show the vision is being met.")],
     defs=("challengeLedger",))

kind("product-roadmap", "PI Roadmap", "art", "main", ["product-manager"],
     "The ART's roadmap: the committed PI and a forecast of the next two.",
     {**main_fields("product-manager"), "currentPi": s("PI slug of the committed PI.", "<pi-slug>"), "lastReviewed": s("YYYY-MM-DD of the last review.", "YYYY-MM-DD")},
     [S("PI roadmap", "Current PI: the committed Features. Next two PIs: forecast only.", True),
      S("Milestones and releases", "Fixed dates, market events, planned releases (releases are decoupled from the PI cadence).", True),
      S("Capacity allocation", "The share of capacity for new features, enablers, and maintenance, and who agreed it."),
      S("Assumptions and risks", "What the forecast depends on.")],
     defs=("challengeLedger",))

kind("feature", "Feature", "art", "main", ["product-manager", "system-architect"],
     "Solution functionality that delivers business value, fulfills a stakeholder need, and is sized to be delivered by an ART within a PI.",
     {
         **main_fields("product-manager"),
         "type": e("business: authored by the Product Manager. enabler: authored by the System Architect.", ["business", "enabler"]),
         "enablerType": opt_e("For an enabler: its category.", ENABLER_TYPES),
         **work_item_fields(FLOW_STATES, "funnel"),
         "parent": opt_path("The Epic or Capability this Feature splits from; null for a Feature from the ART's local context."),
         "targetPi": opt_s("PI slug the Feature is planned for, or null."),
     },
     [S("Description", "What the Feature is, in one paragraph.", True),
      S("Benefit hypothesis", "The measurable benefit expected for the customer or the business, and how it will be observed.", True),
      S("Acceptance criteria", "One bullet per criterion (AC1, AC2, …), independently testable, covering the functionality and the relevant NFRs. Given/When/Then where it helps.", True),
      S("Nonfunctional requirements", "The NFR ids from the ART's register that apply, and any tightening. A missing NFR is an `nfr-refinement` concern, not an acceptance criterion."),
      S("Stories", "Candidate split into Stories, each a vertical slice."),
      S("Dependencies", "Other Features, teams, ARTs, suppliers, architecture decisions."),
      S("Open questions", "What is still unknown, who can answer, and the assumption taken meanwhile.")],
     defs=("challengeLedger", "wsjf", "transitions"))

kind("adr", "Architecture decision", "art", "main", ["system-architect"],
     "One architecture decision that extends the architectural runway: the context, the options kept open, the decision and its consequences.",
     {
         **main_fields("system-architect"),
         "status": e("Decision state.", ["proposed", "accepted", "superseded", "rejected"]),
         "decisionDate": opt_s("YYYY-MM-DD the human accepted the decision, or null."),
         "supersedes": strs("Paths of the decisions this one replaces."),
         "features": strs("Paths of the Features that need or implement this decision."),
     },
     [S("Context", "The forces at play: the Features that need the decision, the NFRs, the constraints.", True),
      S("Options considered", "At least two real options with their trade-offs. Prefer keeping options open until the last responsible moment.", True),
      S("Decision", "The option chosen and why, in a few sentences.", True),
      S("Consequences", "What becomes easier, what becomes harder, what must now be true.", True),
      S("Runway impact", "The enabler Features and Stories this decision requires."),
      S("Validation", "How the decision will be proven on a working system, and what would reopen it.")],
     defs=("challengeLedger",))

kind("nfrs", "Nonfunctional requirements", "art", "main", ["system-architect"],
     "The ART's register of system qualities that constrain the backlog: each one measurable and verifiable.",
     {
         **main_fields("system-architect"),
         "nfrs": objs("The register.",
                      {"id": s("NFR-1, NFR-2, …"), "category": s("e.g. security, reliability, performance, maintainability, scalability, usability, accessibility, privacy, responsible-ai."),
                       "statement": s("The quality required, bounded and unambiguous."), "measure": s("The measurable threshold."),
                       "verification": s("How and when it is verified (test, monitor, audit), and in which Definition of Done.")},
                      ["id", "category", "statement", "measure", "verification"]),
     },
     [S("Scope", "The solution and the context the register applies to.", True),
      S("Register", "Why each NFR exists and what it costs; the frontmatter holds the canonical list.", True),
      S("Verification approach", "How NFRs are tested continuously and which ones are revisited per iteration, PI or release."),
      S("Trade-offs", "NFRs in tension and the economic choice made.")],
     defs=("challengeLedger",))

kind("delivery-pipeline", "Continuous Delivery Pipeline", "art", "main", ["devops-engineer"],
     "The map of the ART's Continuous Delivery Pipeline: the workflows, activities and automation from ideation to an on-demand release, with its bottlenecks.",
     {
         **main_fields("devops-engineer"),
         "leadTime": opt_s("Total lead time from idea to release, with its unit."),
         "stages": objs("Pipeline steps in order.",
                        {"name": s("Step name."), "aspect": e("Pipeline aspect.", ["continuous-exploration", "continuous-integration", "continuous-deployment", "release-on-demand"]),
                         "automated": b("True when the step runs without a manual hand-off."), "leadTime": opt_s("Lead time of the step."), "processTime": opt_s("Process time of the step.")},
                        ["name", "aspect", "automated"]),
     },
     [S("Value stream map", "The current steps with lead time, process time and percent complete and accurate; where work waits.", True),
      S("Continuous Exploration", "How ideas become prioritized Features in the ART Backlog.", True),
      S("Continuous Integration", "Develop, Build, Test end-to-end, Stage: what is automated, what is not.", True),
      S("Continuous Deployment", "Deploy, Verify, Monitor, Respond: what is automated, what is not.", True),
      S("Release on Demand", "How releases are decoupled from deployment, and how outcomes are measured."),
      S("Bottlenecks and improvements", "The largest delays and the enablers proposed to remove them."),
      S("Security and compliance controls", "The automated checks built into the pipeline.")],
     defs=("challengeLedger",))

kind("release", "Release", "art", "main", ["release-manager"],
     "The plan and readiness record of one release: what is made available to which customers, when, and with what evidence.",
     {
         **main_fields("release-manager"),
         "status": e("Release state.", ["planned", "ready", "released", "rolled-back", "cancelled"]),
         "features": strs("Paths of the Features released."),
         "targetDate": opt_s("YYYY-MM-DD targeted, or null for on demand."),
         "strategy": s("How the release is exposed (e.g. full, canary, feature toggle, dark launch).", "<release strategy>"),
     },
     [S("Scope", "The Features released and the customers who get them.", True),
      S("Release strategy", "How release is decoupled from deployment, the audience, and the order of exposure.", True),
      S("Readiness evidence", "Acceptance, NFR verification, security and compliance evidence, with links.", True),
      S("Rollout and rollback", "Steps, checkpoints, the rollback trigger and its tested procedure.", True),
      S("Operations readiness", "Monitoring, alerts, service level objectives, runbooks, support."),
      S("Communication and enablement", "Release notes, documentation, training, customer messaging."),
      S("Measure", "The outcomes to observe after release to evaluate each Feature's benefit hypothesis."),
      S("Risks", "What could go wrong and who decides to stop.")],
     defs=("challengeLedger",))

# -- team -----------------------------------------------------------------------------------

kind("team-charter", "Team charter", "team", "main", ["scrum-master"],
     "The charter of an Agile team: its mission, members, working agreements, Definition of Done and Kanban.",
     {
         **main_fields("scrum-master"),
         "topology": e("Team type.", ["stream-aligned", "complicated-subsystem", "platform", "enabling"]),
         "method": e("How the team plans its work.", ["safe-scrum", "safe-team-kanban"]),
         "members": strs("Roles on the team (agent slugs and human roles); ten or fewer."),
         "wipLimits": objs("Work-in-process limit per Team Kanban state.", {"state": s("State name."), "limit": num("WIP limit.")}, ["state", "limit"]),
     },
     [S("Mission", "The value the team delivers and to whom.", True),
      S("Members and roles", "Product Owner, Scrum Master/Team Coach, the skills on the team, and the human who decides at the team's gates.", True),
      S("Working agreements", "How the team collaborates, reviews and escalates.", True),
      S("Definition of Ready", "What a Story needs before it can be planned."),
      S("Definition of Done", "What every Story must satisfy to be accepted, including the NFR checks.", True),
      S("Team Kanban", "The workflow states, their policies and WIP limits."),
      S("Cadence and events", "Iteration Planning, Team Sync, Backlog Refinement, Iteration Review, Iteration Retrospective.")],
     defs=("challengeLedger",))

kind("story", "Story", "team", "main", ["product-owner"],
     "A short description of a small piece of desired functionality written from the user's perspective, small enough for one iteration.",
     {
         **main_fields("product-owner"),
         "type": e("user: end-user value. enabler: exploration, architecture, infrastructure or compliance work.", ["user", "enabler"]),
         "enablerType": opt_e("For an enabler: its category (a spike is an exploration enabler).", ENABLER_TYPES),
         **work_item_fields(STORY_STATES, "backlog"),
         "parent": opt_path("The Feature this Story splits from; null for a Story from the team's local context."),
         "estimate": opt_num("Story points (modified Fibonacci), set by the team."),
         "iteration": opt_s("Iteration slug the Story is planned in, or null."),
     },
     [S("Story", "As a <user role>, I want to <activity>, so that <business value>. For an enabler: what must be learned or built, and why now.", True),
      S("Acceptance criteria", "One bullet per criterion (AC1, AC2, …): Given <context>, when <action>, then <observable outcome>.", True),
      S("Nonfunctional requirements", "The NFR ids that apply to this Story and how they are checked."),
      S("Notes", "Design notes, examples, links."),
      S("Open questions", "What is still unknown, who can answer, and the assumption taken meanwhile.")],
     defs=("challengeLedger", "wsjf", "transitions"))

kind("iteration-plan", "Iteration plan", "team", "main", ["scrum-master"],
     "The team's plan for one iteration: its goals, the Stories it selected and the capacity behind them.",
     {
         **main_fields("scrum-master"),
         "iteration": s("Iteration slug.", "<iteration-slug>"),
         "capacity": opt_num("Team capacity in story points."),
         "load": opt_num("Planned load in story points."),
         "goals": objs("Iteration goals.", {"id": s("G1, G2, …"), "goal": s("A business or technical goal for the iteration.")}, ["id", "goal"]),
         "stories": strs("Paths of the Stories selected."),
     },
     [S("Iteration goals", "A short summary of what the team agrees to accomplish; the commitment is to the goals, not to the Stories.", True),
      S("Selected stories", "The Stories, in order, each tied to a goal and to a PI Objective.", True),
      S("Capacity and load", "Capacity, velocity history and the load planned against them.", True),
      S("Dependencies and risks", "What other teams must deliver, and the risks to the goals."),
      S("Commitment", "The mutual commitment recorded after the human decision.")],
     defs=("challengeLedger",))

kind("code-change", "Code change", "team", "main", ["software-engineer"],
     "The record of the change that implements one Story: what changed, where, and the evidence that it meets the Definition of Done.",
     {
         **main_fields("software-engineer"),
         "story": path("The Story implemented.", "<path of the story>"),
         "repository": s("The code repository changed.", "<repository>"),
         "branch": s("The branch that holds the change.", "<branch>"),
         "pullRequest": opt_s("Pull request link, or null."),
         "status": e("Change state.", ["in-progress", "ready-for-review", "changes-requested", "approved", "merged"]),
         "testsPassing": b("True when the automated tests of the change pass."),
     },
     [S("Summary", "What changed and why, in a few lines a reviewer can check against the diff.", True),
      S("Design notes", "The approach, the alternatives dropped, and any deviation from an architecture decision."),
      S("Tests", "The tests written first and the behaviors they pin down; how to run them; the result.", True),
      S("Definition of Done", "Each item of the team's Definition of Done, checked or explained.", True),
      S("How to verify", "The steps for a human to see the acceptance criteria met."),
      S("Risks and rollback", "What could break and how to undo the change.")],
     defs=("challengeLedger",))
