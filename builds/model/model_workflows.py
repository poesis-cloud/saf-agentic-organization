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

"""The workspace layout and the workflow catalog.

Four workflow patterns: `loop` (draft, one challenge per expert, revise), `transition` (the owner
records a state change, the orchestrator re-renders the board), `event` (the orchestrator records
a SAFe event) and `gate` (the orchestrator records a human decision). `generate.py` turns each
workflow into its configuration (`workflows/`) and its brief (`instructions/<layer>/`).
"""

P = "portfolio"
ST = P + "/solution-trains/<solution-train-slug>"
ART = P + "/arts/<art-slug>"
TEAM = ART + "/teams/<team-slug>"

# (path, kind, template slug, description)
LAYOUT = []

def node(path, kind, template, description):
    LAYOUT.append((path, kind, template, description))

def scope_common(base, label, kanban):
    node(f"{base}/{kanban}.md", "kanban", f"kanbans/{kanban}", f"{label} Kanban board, rendered from the items' status.")
    node(f"{base}/challenges/<challenge-slug>.challenge.md", "challenge", "shared/challenge", f"Expert challenge packets on the {label} artifacts of this folder.")
    node(f"{base}/decisions/<decision-slug>.gate-decision.md", "gate-decision", "shared/gate-decision", f"Human gate decisions on {label} artifacts.")

def item(base, folder, var, kind, layer, label):
    node(f"{base}/{folder}/<{var}>/<{var}>.{kind}.md", kind, f"{layer}/{kind}", label)
    node(f"{base}/{folder}/<{var}>/challenges/<challenge-slug>.challenge.md", "challenge", "shared/challenge", f"Expert challenge packets on this {kind}.")

def events(base, names):
    for name in names:
        node(f"{base}/events/<event-slug>.{name}.md", "event-record", f"events/{name}", f"One {name.replace('-', ' ')} record.")

# portfolio
for k, d in (("strategic-themes", "Strategic Themes in OKR format."), ("portfolio-vision", "Portfolio Vision and canvas."),
             ("portfolio-roadmap", "Portfolio Roadmap."), ("lean-budgets", "Lean Budgets and guardrails."),
             ("architecture-vision", "Architecture Vision (technology vision, strategy, roadmap).")):
    node(f"{P}/{k}.md", k, f"portfolio/{k}", d)
scope_common(P, "portfolio", "portfolio-kanban")
events(P, ["portfolio-sync", "strategic-portfolio-review"])
item(P, "value-streams", "value-stream-slug", "value-stream", "portfolio", "One development value stream definition.")
node(f"{P}/epics/<epic-slug>/<epic-slug>.epic.md", "epic", "portfolio/epic", "One Epic (business or enabler).")
node(f"{P}/epics/<epic-slug>/<epic-slug>.lean-business-case.md", "lean-business-case", "portfolio/lean-business-case", "The Epic's Lean Business Case.")
node(f"{P}/epics/<epic-slug>/challenges/<challenge-slug>.challenge.md", "challenge", "shared/challenge", "Expert challenge packets on this Epic and its Lean Business Case.")
# large solution
for k, d in (("solution-train-canvas", "Solution Train canvas."), ("solution-vision", "Solution Vision."),
             ("solution-roadmap", "Solution Roadmap."), ("solution-intent", "Solution Intent.")):
    node(f"{ST}/{k}.md", k, f"solution/{k}", d)
scope_common(ST, "Solution Train", "solution-train-kanban")
events(ST, ["pre-plan", "coordinate-and-deliver", "solution-demo", "inspect-and-adapt"])
item(ST, "capabilities", "capability-slug", "capability", "solution", "One Capability (business or enabler).")
item(ST, "suppliers", "supplier-slug", "supplier-agreement", "solution", "One supplier agreement.")
node(f"{ST}/pis/<pi-slug>/pi-objectives.md", "pi-objectives", "art/pi-objectives", "Solution Train PI Objectives and plan for one PI.")
node(f"{ST}/pis/<pi-slug>/challenges/<challenge-slug>.challenge.md", "challenge", "shared/challenge", "Expert challenge packets on this PI plan.")
# ART
for k, d in (("art-canvas", "ART canvas."), ("product-vision", "Product Vision."), ("product-roadmap", "PI Roadmap."),
             ("nfrs", "Nonfunctional requirements register."), ("delivery-pipeline", "Continuous Delivery Pipeline map.")):
    node(f"{ART}/{k}.md", k, f"art/{k}", d)
scope_common(ART, "ART", "art-kanban")
events(ART, ["art-sync", "system-demo", "inspect-and-adapt"])
item(ART, "adrs", "adr-slug", "adr", "art", "One architecture decision.")
item(ART, "features", "feature-slug", "feature", "art", "One Feature (business or enabler).")
node(f"{ART}/pis/<pi-slug>/pi-objectives.md", "pi-objectives", "art/pi-objectives", "ART PI Objectives and plan for one PI.")
node(f"{ART}/pis/<pi-slug>/challenges/<challenge-slug>.challenge.md", "challenge", "shared/challenge", "Expert challenge packets on this PI plan.")
item(ART, "releases", "release-slug", "release", "art", "One release plan and readiness record.")
# team
node(f"{TEAM}/team-charter.md", "team-charter", "team/team-charter", "Team charter.")
scope_common(TEAM, "team", "team-kanban")
events(TEAM, ["team-sync", "iteration-review", "iteration-retrospective"])
node(f"{TEAM}/stories/<story-slug>/<story-slug>.story.md", "story", "team/story", "One Story (user or enabler).")
node(f"{TEAM}/stories/<story-slug>/<story-slug>.code-change.md", "code-change", "team/code-change", "The code change that implements the Story.")
node(f"{TEAM}/stories/<story-slug>/challenges/<challenge-slug>.challenge.md", "challenge", "shared/challenge", "Expert challenge packets on this Story and its code change.")
node(f"{TEAM}/iterations/<iteration-slug>/iteration-plan.md", "iteration-plan", "team/iteration-plan", "The team's plan for one iteration.")
node(f"{TEAM}/iterations/<iteration-slug>/challenges/<challenge-slug>.challenge.md", "challenge", "shared/challenge", "Expert challenge packets on this iteration plan.")

SCOPE = {"portfolio": P, "solution": ST, "art": ART, "team": TEAM}
KANBAN = {"portfolio": "portfolio-kanban", "solution": "solution-train-kanban", "art": "art-kanban", "team": "team-kanban"}
KANBAN_LEVEL = {"portfolio": "portfolio", "solution": "solution-train", "art": "art", "team": "team"}

WORKFLOWS = []

def _cond(kind, slug, query, predicate):
    return dict(kind=kind, slug=slug, query=query, predicate=predicate)

def exists_pre(slug, kind, states):
    return _cond("precondition", slug, f"workspace.filter(a, a.kind == '{kind}' && a.data.status in {states})", "selected.size() > 0")

def parent_post(slug, options):
    """options: [(kind, states)] the parent may be, when set."""
    alts = " || ".join(f"workspace.exists(p, p.kind == '{k}' && p.path == a.data.parent && p.data.status in {st})" for k, st in options)
    return _cond("postcondition", slug, "workspace.filter(a, a.path == step.artifact.path && a.data.parent != null)", f"selected.all(a, {alts})")

def loop(slug, layer, title, kind, main_path, author, panel, purpose, concerns, draft, challenge, revise, gate, nxt,
         predecessors=(), draft_conditions=()):
    WORKFLOWS.append(dict(pattern="loop", slug=slug, layer=layer, title=title, kind=kind, main_path=main_path, author=author,
                          panel=list(panel), purpose=purpose, concerns=concerns, draft=draft, challenge=challenge, revise=revise,
                          gate=gate, next=nxt, predecessors=list(predecessors), draft_conditions=list(draft_conditions)))

def transition(slug, layer, title, kind, main_path, owner, states, purpose, concerns, rules, nxt, predecessors=(), conditions=()):
    WORKFLOWS.append(dict(pattern="transition", slug=slug, layer=layer, title=title, kind=kind, main_path=main_path, author=owner,
                          states=states, purpose=purpose, concerns=concerns, rules=rules, next=nxt,
                          predecessors=list(predecessors), conditions=list(conditions)))

def event(slug, layer, title, event_name, purpose, concerns, agenda, nxt, kanban=False, predecessors=()):
    WORKFLOWS.append(dict(pattern="event", slug=slug, layer=layer, title=title, event=event_name, kind="event-record",
                          main_path=f"{SCOPE[layer]}/events/<event-slug>.{event_name}.md", purpose=purpose, concerns=concerns,
                          agenda=agenda, next=nxt, kanban=kanban, predecessors=list(predecessors)))

def gate(slug, layer, title):
    WORKFLOWS.append(dict(pattern="gate", slug=slug, layer=layer, title=title, kind="gate-decision",
                          main_path=f"{SCOPE[layer]}/decisions/<decision-slug>.gate-decision.md",
                          purpose=f"Record the human's decision on a challenged {KANBAN_LEVEL[layer].replace('-', ' ')}-level artifact that is not a backlog item (backlog items move with their transition workflow).",
                          concerns="\"I accept / reject the vision, roadmap, budget, plan…\" after a gate.",
                          next="On a rejection or concerns: rerun the authoring workflow of the artifact.", predecessors=[]))

APPROVED_EPIC = "['ready', 'implementing']"
OPEN_FLOW = "['analyzing', 'ready', 'implementing']"

# =============================== PORTFOLIO ===============================================

loop("strategic-themes", "portfolio", "Strategic Themes", "strategic-themes", f"{P}/strategic-themes.md", "portfolio-manager",
     ["enterprise-architect", "business-owner", "financial-controller", "data-analyst"],
     "Formulate or revise the portfolio's Strategic Themes as Objectives and Key Results that connect the portfolio to the enterprise strategy.",
     "New or changed strategy, business objectives, OKRs for the portfolio.",
     ["Read the human's strategy input and, when they exist, the Portfolio Vision and Lean Budgets.",
      "State each theme as one objective with two to five measurable key results. A theme differentiates: business as usual is not a theme.",
      "Say what each theme changes in budgets, the vision and the backlog, and what the portfolio will not pursue."],
     ["Does each key result measure an outcome, with a baseline and a target, rather than an activity?",
      "Do the themes make choices, or could any portfolio claim them?"],
     ["Every theme has measurable key results; exclusions are explicit."],
     "Portfolio Leadership decides whether these themes are the portfolio's direction.",
     "`portfolio-gate-decision` to record the decision; then `portfolio-vision` and `strategic-investment-planning`.")

loop("portfolio-vision", "portfolio", "Portfolio Vision", "portfolio-vision", f"{P}/portfolio-vision.md", "portfolio-manager",
     ["enterprise-architect", "business-analyst", "business-owner"],
     "Describe the future state of the portfolio's value streams and solutions, from the current-state portfolio canvas to the future-state one.",
     "Where the portfolio is heading; portfolio canvas; future state.",
     ["Read the Strategic Themes and the value stream definitions.",
      "Fill the current-state canvas from facts, then the future state at the horizon. Keep it aspirational, yet realistic and achievable.",
      "Name the Epics and changes that close the gap; do not write those Epics here."],
     ["Is the future state reachable from the current state with the funding and capacity the portfolio has?",
      "Does every change trace to a Strategic Theme?"],
     ["Current and future canvas are both filled; the path names Epics by intent."],
     "Portfolio Leadership decides whether this is the future state to steer by.",
     "`portfolio-gate-decision`; then `epic-hypothesis` for each Epic on the path and `portfolio-roadmap`.",
     predecessors=["strategic-themes"])

loop("value-stream-definition", "portfolio", "Value stream definition", "value-stream",
     f"{P}/value-streams/<value-stream-slug>/<value-stream-slug>.value-stream.md", "portfolio-manager",
     ["business-analyst", "enterprise-architect", "agile-coach"],
     "Define one development value stream: the operational value streams it supports, its solutions and customers, the trains that realize it, and its KPIs.",
     "Organize around value; identify a value stream; decide which ARTs or Solution Trains exist.",
     ["Start from the operational value stream: who is served and what triggers the flow.",
      "Name the solutions, then the people needed, then trains sized to deliver with few cross-train dependencies (an ART is 50 to 125 people).",
      "Give four to seven KPIs tied to the Strategic Themes."],
     ["Can the trains named deliver end to end, or do hand-offs to other value streams remain?",
      "Are the KPIs outcomes of the value stream rather than activity counts?"],
     ["Trains and KPIs are named; known cross-value-stream dependencies are listed."],
     "Portfolio Leadership decides whether to organize and fund the value stream this way.",
     "`portfolio-gate-decision`; then `solution-train-launch` or `art-launch` with the train's orchestrator.")

loop("epic-hypothesis", "portfolio", "Epic hypothesis", "epic", f"{P}/epics/<epic-slug>/<epic-slug>.epic.md", "epic-owner",
     ["enterprise-architect", "business-owner", "data-analyst"],
     "Capture or thicken one Epic as an Epic hypothesis statement, ready for Portfolio Leadership to review.",
     "A new big initiative or idea; an enabler Epic; thicken an Epic in the funnel or under review.",
     ["One Epic per run. Create it with `status: funnel`, or thicken the existing one without changing its status.",
      "Write the hypothesis statement, the business outcomes hypothesis and leading indicators; set `type` (an enabler Epic extends the runway or improves the value stream).",
      "Estimate WSJF relatively against the other Epics. Outline the MVP in one paragraph; the Lean Business Case details it later."],
     ["Is the hypothesis falsifiable: could the leading indicators prove it wrong early?",
      "Is this an Epic, or a Capability or Feature that fits in a PI and belongs to another layer?"],
     ["Hypothesis, outcomes, leading indicators, scope and WSJF are filled; unknowns sit under Open questions with an assumption."],
     "Portfolio Leadership decides whether the Epic is worth reviewing, then analyzing.",
     "`epic-transition` to record the move (funnel → reviewing → analyzing); once analyzing, `lean-business-case`.")

loop("lean-business-case", "portfolio", "Lean Business Case", "lean-business-case",
     f"{P}/epics/<epic-slug>/<epic-slug>.lean-business-case.md", "epic-owner",
     ["enterprise-architect", "financial-controller", "security-expert", "data-protection-officer", "legal-counsel"],
     "Analyze one Epic in the analyzing state: define its MVP, estimate its cost and projected value, and recommend go or no-go.",
     "Business case, MVP definition, cost estimate, go/no-go for an Epic under analysis.",
     ["Read the Epic and, when they exist, the Architecture Vision and Lean Budgets. One Lean Business Case per run, for the Epic the human names.",
      "Define the MVP as the smallest solution that can prove or disprove the hypothesis. Estimate the MVP cost and the forecast implementation cost separately.",
      "End with a recommendation: `go`, `no-go`, or `pending` with the missing fact. Do not change the Epic: its status moves in `epic-transition`."],
     ["Would the MVP, as defined, actually settle the hypothesis?",
      "Are the cost estimates explained, and is the full cost left uncommitted until the MVP proves the hypothesis?"],
     ["The recommendation is `go` or `no-go`, or `pending` names the fact missing; cost and return are stated with their assumptions."],
     "Portfolio Leadership decides go or no-go.",
     "`epic-transition` to record it (analyzing → ready on go; → done with resolution no-go otherwise).",
     predecessors=["epic-hypothesis"],
     draft_conditions=[
         exists_pre("an-epic-is-under-analysis", "epic", "['analyzing', 'ready', 'implementing']"),
         _cond("postcondition", "case-names-an-epic-under-analysis", "workspace.filter(a, a.path == step.artifact.path)",
               "selected.all(a, workspace.exists(e, e.kind == 'epic' && e.path == a.data.epic && e.data.status in ['analyzing', 'ready', 'implementing']))")])

loop("epic-mvp-evaluation", "portfolio", "Epic MVP evaluation", "epic", f"{P}/epics/<epic-slug>/<epic-slug>.epic.md", "epic-owner",
     ["data-analyst", "business-owner", "financial-controller"],
     "Evaluate the MVP of one implementing Epic against its hypothesis and recommend to persevere, pivot or stop.",
     "MVP results are in; pivot or persevere; stop an Epic.",
     ["Read the Epic, its Lean Business Case, and the evidence the human or the trains provide (demos, measures, Feature outcomes).",
      "Under `## MVP`, record the evidence against each leading indicator, then the recommendation: persevere, pivot (to which new hypothesis) or stop.",
      "Do not change `status`, `implementationStage` or `resolution`: they move in `epic-transition` after the human decided."],
     ["Does the evidence measure the hypothesis, or only that work was delivered?",
      "Is the recommendation free of sunk-cost reasoning?"],
     ["Each leading indicator has a result or an explicit gap; the recommendation follows from the evidence."],
     "Portfolio Leadership decides to persevere, pivot or stop.",
     "`epic-transition` to record it; a pivot starts a new `epic-hypothesis`.",
     predecessors=["lean-business-case"],
     draft_conditions=[exists_pre("an-epic-is-implementing", "epic", "['implementing']")])

loop("portfolio-roadmap", "portfolio", "Portfolio Roadmap", "portfolio-roadmap", f"{P}/portfolio-roadmap.md", "portfolio-manager",
     ["enterprise-architect", "financial-controller", "product-marketing-manager"],
     "Build or revise the multi-year view of how the Portfolio Vision will be achieved across the value streams.",
     "Multi-year plan of the portfolio; when Epics land; portfolio milestones.",
     ["Read the Portfolio Vision, the Epics and their status, and the solution and PI roadmaps that exist.",
      "Near term is committed (Epics implementing or ready); mid term is a forecast; long term is intent without dates that read as commitments.",
      "Aggregate what the trains forecast; do not invent their dates."],
     ["Does the near term fit the funded capacity of the value streams?",
      "Which milestone is a real external date, and which is only a wish?"],
     ["The three horizons are distinct; every near-term item traces to an approved Epic."],
     "Portfolio Leadership decides whether to communicate this roadmap.",
     "`portfolio-gate-decision`.", predecessors=["portfolio-vision"])

loop("strategic-investment-planning", "portfolio", "Strategic Investment Planning", "lean-budgets", f"{P}/lean-budgets.md", "portfolio-manager",
     ["financial-controller", "enterprise-architect", "business-owner", "finops-engineer"],
     "Establish or update Lean value stream budgets and their guardrails for the coming budget period (formerly Participatory Budgeting).",
     "Budgets per value stream; funding; guardrails; capacity allocation; investment horizons.",
     ["Read the Strategic Themes, Portfolio Vision, value streams, the Epics above the threshold and any forum results the human provides.",
      "Per value stream: Baseline Solution Investments first, then Proposed Solution Initiatives, budgeting only the cost expected in the period.",
      "Apply the four guardrails and record the forum insights. Forum results inform the allocation; Portfolio Leadership finalizes it."],
     ["Do the allocations respect the guardrails, and does the sum match the total budget?",
      "Is any initiative funded beyond its MVP before its hypothesis is proven?"],
     ["Every value stream has a budget with its reasons; the four guardrails are stated as applied."],
     "Portfolio Leadership finalizes the portfolio budget.",
     "`portfolio-gate-decision`; value streams prepare during the current PI and apply the change at the next one.",
     predecessors=["strategic-themes"])

loop("architecture-vision", "portfolio", "Architecture Vision", "architecture-vision", f"{P}/architecture-vision.md", "enterprise-architect",
     ["solution-architect", "security-expert", "platform-engineer", "data-engineer", "finops-engineer"],
     "Establish or revise the portfolio's technology vision, strategy and roadmap, and the architectural runway it needs.",
     "Technology strategy; target architecture; portfolio-level runway; which enabler Epics are needed.",
     ["Read the Strategic Themes, Portfolio Vision and the Epics.",
      "Describe intentional architecture and a few principles; leave room for emergent design in the trains.",
      "Name the enabler Epics the runway needs; they are written in `epic-hypothesis`, not here."],
     ["Is the runway just enough for the near-term Epics, or built far ahead of need?",
      "Which decision must be taken now, and which can wait for learning?"],
     ["Target, principles and the ordered runway are stated; each enabler Epic is named by intent."],
     "Portfolio Leadership and the lead architects decide whether this is the technical direction.",
     "`portfolio-gate-decision`; then `epic-hypothesis` for each enabler Epic.")

transition("epic-transition", "portfolio", "Epic transition", "epic", f"{P}/epics/<epic-slug>/<epic-slug>.epic.md", "epic-owner", "funnel → reviewing → analyzing → ready → implementing (mvp, then persevere) → done",
     "Record the human's decision to move one Epic to a new Portfolio Kanban state, then re-render the Portfolio Kanban.",
     "\"Approve / reject / move / stop this Epic\" after a gate.",
     ["`ready` and `implementing` need a Lean Business Case recommending `go`.",
      "Entering `implementing` sets `implementationStage: mvp`; a persevere decision sets `persevere`.",
      "`done` sets `resolution`: delivered, no-go, pivoted or stopped."],
     "On `analyzing`: `lean-business-case`. On `ready`: the trains pull the Epic (`capability-refinement`, `feature-refinement`).",
     conditions=[
         _cond("postcondition", "challenged-before-leaving-the-funnel", "workspace.filter(a, a.path == step.artifact.path && a.data.status != 'funnel')",
               "selected.all(a, size(a.data.challengeLedger) > 0)"),
         _cond("postcondition", "approved-epic-has-a-go-business-case", "workspace.filter(a, a.path == step.artifact.path && a.data.status in ['ready', 'implementing'])",
               "selected.all(a, workspace.exists(l, l.kind == 'lean-business-case' && l.data.epic == a.path && l.data.recommendation == 'go'))")])

event("portfolio-sync", "portfolio", "Portfolio Sync", "portfolio-sync",
      "Inspect the flow of Epics and the portfolio's operations between Strategic Portfolio Reviews, and re-render the Portfolio Kanban.",
      "Portfolio status; where the Epics are; impediments and dependencies across value streams.",
      ["Epics by state, WIP against limits, aged and blocked Epics.", "Dependencies and impediments across value streams.",
       "Backlog refinement: new Epics to capture, priorities to revisit, Epics to remove.", "Budget and guardrail signals worth a Strategic Portfolio Review."],
      "A backlog change is its own workflow: `epic-hypothesis`, `epic-transition`.", kanban=True)

event("strategic-portfolio-review", "portfolio", "Strategic Portfolio Review", "strategic-portfolio-review",
      "Review whether the portfolio is achieving its vision and themes, and record the funding and direction decisions Portfolio Leadership takes.",
      "Is the portfolio on strategy; keep, pivot or stop investments; review KPIs and OKRs.",
      ["Progress of the Strategic Themes' key results and value stream KPIs.", "Budget against guardrails; Strategic Investment Planning insights.",
       "Epics: which to accelerate, pivot or stop.", "Decisions, each with the workflow that will carry it."],
      "Each decision is carried by its workflow: `strategic-themes`, `strategic-investment-planning`, `epic-transition`, `portfolio-roadmap`.")

gate("portfolio-gate-decision", "portfolio", "Portfolio gate decision")

# =============================== LARGE SOLUTION ==========================================

loop("solution-train-launch", "solution", "Solution Train launch", "solution-train-canvas", f"{ST}/solution-train-canvas.md", "solution-train-engineer",
     ["agile-coach", "solution-architect", "business-analyst"],
     "Define or revise one Solution Train: its mission, ARTs and suppliers, roles and cadence.",
     "Set up a Solution Train; change its ARTs, suppliers, roles or cadence.",
     ["Read the value stream definition and the ART canvases that exist.",
      "Start with the foundational elements: vision owner, backlog owner, roles; the Kanban, roadmap and System Team can follow.",
      "Put every ART and supplier on one PI cadence."],
     ["Do the ARTs and suppliers named cover the whole solution, with clear interfaces?", "Is anyone accountable for integration across trains?"],
     ["Mission, members, roles and the common cadence are filled."],
     "The solution's leaders decide whether to operate the train this way.",
     "`solution-gate-decision`; then `solution-vision` and `solution-intent`.")

loop("solution-vision", "solution", "Solution Vision", "solution-vision", f"{ST}/solution-vision.md", "solution-manager",
     ["solution-architect", "business-owner", "ux-designer", "product-marketing-manager"],
     "Describe the future state of the large solution: customer and stakeholder needs and the proposed solution.",
     "What the large solution should become; who it serves; solution context.",
     ["Read the Portfolio Vision and the Epics that fund the solution.",
      "Write for alignment across ARTs and suppliers: the vision statement, customers and needs, solution context.",
      "Name key capabilities by intent; they are written in `capability-refinement`."],
     ["Would two ARTs reading this build compatible things?", "Is the solution context concrete enough to constrain design?"],
     ["Vision statement, customers and solution context are filled; exclusions are explicit."],
     "Solution Management's human lead decides whether this is the vision to align the train on.",
     "`solution-gate-decision`; then `solution-roadmap` and `capability-refinement`.", predecessors=["solution-train-launch"])

loop("solution-roadmap", "solution", "Solution Roadmap", "solution-roadmap", f"{ST}/solution-roadmap.md", "solution-manager",
     ["solution-architect", "systems-engineer", "release-manager"],
     "Forecast the solution's deliverables: a PI roadmap (one committed PI, two forecast) and a multi-year view.",
     "When capabilities land; solution milestones; multi-year plan of the solution.",
     ["Read the Solution Vision, the capabilities and their status, and the ARTs' PI roadmaps.",
      "The current PI is committed; the next two are a forecast; beyond is intent.",
      "Show integration points, Solution Demos and supplier dates."],
     ["Do the forecasts respect integration order and supplier lead times?", "Is anything shown as committed that no train committed to?"],
     ["Committed, forecast and intent are distinct; fixed dates are flagged."],
     "Solution Management's human lead decides whether to communicate this roadmap.",
     "`solution-gate-decision`.", predecessors=["solution-vision"])

loop("solution-intent", "solution", "Solution Intent", "solution-intent", f"{ST}/solution-intent.md", "solution-architect",
     ["systems-engineer", "security-expert", "compliance-officer", "data-protection-officer", "site-reliability-engineer"],
     "Record what the solution must do and how it is designed: fixed and variable intent, interfaces, NFRs, standards, verification and traceability.",
     "Solution-level requirements and design; interfaces between ARTs; compliance evidence; what is fixed and what is still open.",
     ["Read the Solution Vision, the capabilities and the Architecture Vision.",
      "Separate fixed intent (non-negotiable) from variable intent (options still explored); for each open option, say what learning or date closes it.",
      "State solution-wide NFRs with measures, the standards that apply, and how evidence is produced as the solution is built."],
     ["Is anything fixed too early that set-based design should keep open, or left open that a regulation fixes?",
      "Can each fixed requirement be verified on a working system?"],
     ["Fixed and variable intent are separated; every NFR has a measure and a verification."],
     "The solution's architects and compliance owner decide whether this intent governs the trains.",
     "`solution-gate-decision`; ARTs take the NFRs into `nfr-refinement`.", predecessors=["solution-vision"])

loop("capability-refinement", "solution", "Capability refinement", "capability",
     f"{ST}/capabilities/<capability-slug>/<capability-slug>.capability.md", "solution-manager",
     ["solution-architect", "systems-engineer", "security-expert", "compliance-officer"],
     "Write or thicken one Capability so it is ready for Pre-Plan: benefit hypothesis, acceptance criteria, WSJF and the Features each ART would take.",
     "A new capability; split an Epic into capabilities; an enabler capability; make a capability ready.",
     ["One Capability per run, sized to fit a PI. Create it with `status: funnel`, or thicken it without changing its status.",
      "Write the benefit hypothesis and testable acceptance criteria; estimate WSJF against the other capabilities.",
      "Outline the Feature split per ART and the cross-ART and supplier dependencies. Set `parent` when it splits from an Epic."],
     ["Does it fit one PI, and can its acceptance be demonstrated at a Solution Demo?", "Which Solution Intent constraints apply?"],
     ["Benefit hypothesis, acceptance criteria, WSJF and the candidate Feature split are filled."],
     "Solution Management's human lead decides whether the Capability is ready.",
     "`capability-transition` to record the move; then `pre-plan`.",
     draft_conditions=[parent_post("parent-epic-is-approved", [("epic", APPROVED_EPIC)])])

loop("supplier-engagement", "solution", "Supplier engagement", "supplier-agreement",
     f"{ST}/suppliers/<supplier-slug>/<supplier-slug>.supplier-agreement.md", "procurement-manager",
     ["legal-counsel", "security-expert", "compliance-officer", "financial-controller", "solution-architect"],
     "Write or revise the agreement that brings one supplier into the Solution Train's cadence, quality expectations and compliance obligations.",
     "Onboard or change a supplier; contract terms for a component or service.",
     ["Read the Solution Intent, the capabilities the supplier contributes to, and the terms the human provides.",
      "Prefer terms that tolerate variable scope and base acceptance on objective evaluation of working deliverables.",
      "State how the supplier joins Pre-Plan, PI Planning, the syncs and the Solution Demo."],
     ["Do the terms let scope evolve without renegotiation at every PI?", "Which obligations (security, privacy, compliance) pass to the supplier, and how are they evidenced?"],
     ["Scope, collaboration model and acceptance are filled; obligations passed to the supplier are explicit."],
     "The human owner of the supplier relationship decides whether to proceed on these terms.",
     "`solution-gate-decision`. This artifact is a working agreement, not the signed contract; a later run records `active` once the humans signed.")

event("pre-plan", "solution", "Pre-Plan", "pre-plan",
      "Align and prepare the ARTs and suppliers of the Solution Train for PI Planning.",
      "Prepare the next PI across ARTs; which capabilities go to which ART.",
      ["Solution Vision and roadmap highlights for the PI.", "The ready capabilities, in WSJF order, and their split into Features per ART.",
       "Cross-ART and supplier dependencies, and the integration points of the PI.", "Planning context each ART takes into its own PI Planning."],
      "Each ART runs `pi-planning` with its Release Train Engineer; then `solution-train-pi-planning`.")

loop("solution-train-pi-planning", "solution", "Solution Train PI Planning", "pi-objectives", f"{ST}/pis/<pi-slug>/pi-objectives.md", "solution-train-engineer",
     ["solution-manager", "solution-architect", "systems-engineer", "business-owner"],
     "Aggregate the ARTs' PI plans into the Solution Train's PI Objectives, planning board and risks for one PI.",
     "The Solution Train's plan and objectives for the PI, after the ARTs planned.",
     ["Read the Pre-Plan record and each ART's `pi-objectives.md` for this PI. Set `scope: solution-train`.",
      "Summarize the ARTs' objectives into Solution Train objectives; show capability delivery, cross-ART dependencies and integration points on the planning board.",
      "ROAM the solution-level risks. Leave business value and the confidence vote for the human gate."],
     ["Do the ART plans, taken together, deliver each committed capability, with dependencies in a feasible order?", "Which solution-level risk has no owner?"],
     ["Objectives are split committed and uncommitted; every committed capability is on the board."],
     "The solution's Business Owners assign business value and the train commits.",
     "`solution-gate-decision` (record the commitment); then `coordinate-and-deliver` during the PI.",
     predecessors=["pre-plan"], draft_conditions=[exists_pre("a-capability-is-ready", "capability", "['ready', 'implementing']")])

event("coordinate-and-deliver", "solution", "Coordinate and Deliver", "coordinate-and-deliver",
      "Keep the ARTs and suppliers aligned during the PI (Product Manager Sync, Architect Sync, RTE Sync) and re-render the Solution Train Kanban.",
      "Cross-ART status during the PI; dependencies, design trade-offs or impediments between ARTs.",
      ["Product Manager Sync: scope and priority issues raised by the ARTs.", "Architect Sync: emerging designs and trade-offs kept consistent across the train.",
       "RTE Sync: progress, dependencies and impediments the ARTs cannot resolve alone.", "Decisions and actions, each with its owner."],
      "A backlog change is its own workflow: `capability-refinement`, `capability-transition`.", kanban=True)

event("solution-demo", "solution", "Solution Demo", "solution-demo",
      "Give stakeholders an integrated view of what the ARTs and suppliers built in the PI, as objective evidence, and collect their feedback.",
      "Demonstrate the integrated solution at the end of the PI.",
      ["What was integrated across the whole Solution Train, and what was not.", "Each capability demonstrated against its acceptance criteria.",
       "NFR and compliance evidence; overall fitness for purpose.", "Stakeholder feedback, recorded in their words."],
      "`capability-transition` for capabilities accepted; feedback feeds `capability-refinement` and the portfolio's investment decisions.")

loop("solution-train-inspect-and-adapt", "solution", "Solution Train Inspect and Adapt", "event-record", f"{ST}/events/<event-slug>.inspect-and-adapt.md", "solution-train-engineer",
     ["agile-coach", "data-analyst"],
     "Evaluate the integrated solution and the train's way of working at the end of the PI, and derive improvement backlog items.",
     "End-of-PI improvement for the Solution Train; cross-ART problems to solve.",
     ["Read the Solution Demo record, the PI Objectives with actual business value, and the ARTs' Inspect and Adapt records. Set `event: inspect-and-adapt`.",
      "Three parts: the demo result, a quantitative and qualitative measurement review, then a retrospective and problem-solving analysis of the largest cross-ART problem.",
      "State each improvement as an action that names the workflow which will write the backlog item."],
     ["Do the measures support the conclusions?", "Does the root cause analysis reach a cause the train can act on?"],
     ["Each improvement action has an owner and a carrying workflow."],
     "The train's stakeholders decide which improvements enter the Solution Train Backlog.",
     "`capability-refinement` for each improvement accepted.", predecessors=["solution-demo"])

transition("capability-transition", "solution", "Capability transition", "capability", f"{ST}/capabilities/<capability-slug>/<capability-slug>.capability.md", "solution-manager",
     "funnel → analyzing → ready → implementing → validating-on-staging → deploying-to-production → releasing → done",
     "Record the human's decision to move one Capability to a new Solution Train Kanban state, then re-render the Solution Train Kanban.",
     "\"Approve / move / accept this capability\" after a gate or a Solution Demo.",
     ["A Capability leaves `analyzing` only after it was challenged.", "`implementing` follows the PI commitment; `done` follows acceptance at a Solution Demo."],
     "On `ready`: `pre-plan`.",
     conditions=[_cond("postcondition", "challenged-before-ready", "workspace.filter(a, a.path == step.artifact.path && !(a.data.status in ['funnel', 'analyzing']))",
                       "selected.all(a, size(a.data.challengeLedger) > 0)")])

gate("solution-gate-decision", "solution", "Solution gate decision")

# =============================== ART =====================================================

loop("art-launch", "art", "ART launch", "art-canvas", f"{ART}/art-canvas.md", "release-train-engineer",
     ["agile-coach", "system-architect", "product-manager"],
     "Define or revise one Agile Release Train: its mission, teams, roles and PI cadence.",
     "Set up an ART; change its teams, roles or cadence.",
     ["Read the value stream definition and, when the ART belongs to one, the Solution Train canvas.",
      "Design teams that can deliver value with few dependencies (5 to 15 teams, each ten people or fewer) and give each a type.",
      "Set the PI calendar: iterations, the IP iteration, PI Planning, System Demo, Inspect and Adapt."],
     ["Can each team deliver a vertical slice, or does every Feature cross all teams?", "Are Product Management, System Architect and Business Owners named?"],
     ["Mission, teams with their type, roles and the PI calendar are filled."],
     "The ART's Business Owners decide whether to launch or change the train this way.",
     "`art-gate-decision`; then `team-formation` with each team's Scrum Master, and `product-vision`.")

loop("product-vision", "art", "Product Vision", "product-vision", f"{ART}/product-vision.md", "product-manager",
     ["system-architect", "ux-designer", "business-owner", "product-marketing-manager"],
     "Describe the future state of the solution the ART develops: customers, their needs and the features proposed to meet them.",
     "Where the product is heading; who it is for; what problems it solves.",
     ["Read the Portfolio or Solution Vision and the Epics or capabilities that fund the ART.",
      "Ground customers and problems in evidence; write the vision statement last.",
      "List key features as candidates; they are written in `feature-refinement`."],
     ["Is each need backed by evidence from customers or usage?", "Would the vision help a team choose between two designs?"],
     ["Vision statement, customers, problems and measures of success are filled."],
     "Product Management's human lead and the Business Owners decide whether this is the vision.",
     "`art-gate-decision`; then `product-roadmap` and `feature-refinement`.", predecessors=["art-launch"])

loop("product-roadmap", "art", "PI Roadmap", "product-roadmap", f"{ART}/product-roadmap.md", "product-manager",
     ["system-architect", "business-owner", "release-manager"],
     "Forecast the ART's deliverables: the committed PI and the next two as a forecast.",
     "What ships when; the next PIs; milestones and planned releases of the ART.",
     ["Read the Product Vision, the Features and their status, and the current PI Objectives.",
      "The current PI shows what was committed at PI Planning; the next two are a forecast from WSJF and capacity.",
      "State the capacity allocation between features, enablers and maintenance."],
     ["Does the forecast leave capacity for enablers the runway needs?", "Is any forecast presented as a commitment?"],
     ["Committed and forecast PIs are distinct; capacity allocation is stated."],
     "Product Management's human lead decides whether to communicate this roadmap.",
     "`art-gate-decision`.", predecessors=["product-vision"])

FEATURE_PARENT = parent_post("parent-is-approved", [("epic", APPROVED_EPIC), ("capability", OPEN_FLOW)])

loop("feature-refinement", "art", "Feature refinement", "feature", f"{ART}/features/<feature-slug>/<feature-slug>.feature.md", "product-manager",
     ["system-architect", "software-engineer", "quality-engineer", "security-expert", "ux-designer", "data-protection-officer"],
     "Write or thicken one business Feature so it is ready for PI Planning: benefit hypothesis, acceptance criteria and WSJF.",
     "A new feature; split an Epic or Capability into features; a Feature-sized change, defect or gap; make a Feature ready.",
     ["One Feature per run, sized to fit a PI (generally under two months of total effort). Create it with `status: funnel` and `type: business`, or thicken it without changing its status.",
      "Write the benefit hypothesis and independently testable acceptance criteria; list the NFR ids that apply; estimate WSJF against the other Features.",
      "Set `parent` when it splits from an Epic or Capability. Architecture decisions and new NFRs are not written here: name them under Dependencies."],
     ["Could a team demonstrate each acceptance criterion at a System Demo?", "Does it fit one PI, or should it be split?"],
     ["Benefit hypothesis, acceptance criteria, NFR applicability and WSJF are filled; unknowns sit under Open questions."],
     "Product Management's human lead decides whether the Feature is ready for PI Planning.",
     "`feature-transition` to record the move; then `pi-planning`.", draft_conditions=[FEATURE_PARENT])

loop("enabler-feature-refinement", "art", "Enabler Feature refinement", "feature", f"{ART}/features/<feature-slug>/<feature-slug>.feature.md", "system-architect",
     ["software-engineer", "platform-engineer", "devops-engineer", "site-reliability-engineer", "observability-engineer"],
     "Write or thicken one enabler Feature that extends the architectural runway or improves the delivery pipeline.",
     "Technical work the ART needs: exploration, architecture, infrastructure or compliance enablers; technical debt at Feature size.",
     ["One enabler Feature per run, with `type: enabler` and its `enablerType`. Create it with `status: funnel`, or thicken it without changing its status.",
      "State the benefit as what it makes possible or faster for named business Features; write acceptance criteria that are demonstrable.",
      "Estimate WSJF so it competes fairly within the capacity allocated to enablers. Link the architecture decisions it implements."],
     ["Is the runway built just in time for the Features that need it?", "Can completion be demonstrated on a working system?"],
     ["`enablerType`, the Features enabled, acceptance criteria and WSJF are filled."],
     "The ART's lead architect and Product Management decide whether the enabler is ready.",
     "`feature-transition` to record the move; then `pi-planning`.", draft_conditions=[FEATURE_PARENT])

loop("architecture-decision", "art", "Architecture decision", "adr", f"{ART}/adrs/<adr-slug>/<adr-slug>.adr.md", "system-architect",
     ["software-engineer", "security-expert", "platform-engineer", "data-engineer", "ai-engineer"],
     "Take one architecture decision that Features need: context, options kept open, the decision proposed and its consequences.",
     "A design choice with lasting consequences; a technology selection; how to meet an NFR.",
     ["One decision per run. Read the Features that need it, the NFR register and the Architecture Vision.",
      "Describe at least two real options with trade-offs; decide at the last responsible moment and say what would reopen the decision.",
      "Set `status: proposed`. List the enabler Features the decision requires; they are written in `enabler-feature-refinement`."],
     ["Is this decision needed now, and is a cheaper reversible option available?", "How will a working system prove the decision right?"],
     ["Options, decision, consequences and validation are filled; `status` is `proposed`."],
     "The ART's lead architect (human) accepts or rejects the decision.",
     "`art-gate-decision`; then `enabler-feature-refinement` for the runway it requires.")

loop("nfr-refinement", "art", "NFR refinement", "nfrs", f"{ART}/nfrs.md", "system-architect",
     ["site-reliability-engineer", "observability-engineer", "security-expert", "quality-engineer", "accessibility-specialist", "ai-engineer"],
     "Create or revise the ART's register of nonfunctional requirements: each one bounded, measurable and verifiable.",
     "System qualities: security, reliability, performance, scalability, usability, accessibility, privacy, Responsible AI.",
     ["Read the Product Vision, the Solution Intent when there is one, and the current register.",
      "Give each NFR an id, a bounded statement, a measurable threshold and a verification (test, monitor or audit) with the Definition of Done that carries it.",
      "Keep the register small: an NFR that cannot be verified, or that nobody would pay for, does not belong."],
     ["Can each NFR be tested or monitored continuously?", "Which NFRs conflict, and is the trade-off economic?"],
     ["Every NFR has a measure and a verification; trade-offs are stated."],
     "The ART's lead architect and Business Owners decide whether these qualities bind the backlog.",
     "`art-gate-decision`; Features and Stories then reference NFR ids.")

loop("delivery-pipeline", "art", "Continuous Delivery Pipeline", "delivery-pipeline", f"{ART}/delivery-pipeline.md", "devops-engineer",
     ["platform-engineer", "security-expert", "quality-engineer", "site-reliability-engineer", "finops-engineer"],
     "Map the ART's Continuous Delivery Pipeline from ideation to on-demand release, find its bottlenecks and propose the enablers that remove them.",
     "How work flows to production; pipeline bottlenecks; DevOps improvements; lead time.",
     ["Map what actually happens today, step by step, with lead time, process time and percent complete and accurate.",
      "Cover the four aspects: Continuous Exploration, Continuous Integration (Develop, Build, Test end-to-end, Stage), Continuous Deployment (Deploy, Verify, Monitor, Respond), Release on Demand.",
      "Name the largest delays and the enabler Features that would remove them; they are written in `enabler-feature-refinement`."],
     ["Where does work wait the longest, and is that where the improvement is aimed?", "Which quality, security or compliance check is still manual?"],
     ["The four aspects are mapped; the top bottlenecks each have a proposed enabler."],
     "The ART's leaders decide which pipeline improvements to fund.",
     "`art-gate-decision`; then `enabler-feature-refinement`.")

loop("pi-planning", "art", "PI Planning", "pi-objectives", f"{ART}/pis/<pi-slug>/pi-objectives.md", "release-train-engineer",
     ["product-manager", "system-architect", "software-engineer", "business-owner"],
     "Plan one PI for the ART: team and ART PI Objectives, the planning board and the PI risks.",
     "Plan the next PI; commit Features; PI Objectives; dependencies and risks.",
     ["Read the Product Vision, PI Roadmap, the ready Features in WSJF order, the ART canvas and team charters. Set `scope: art`.",
      "Per team: objectives stated as outcomes, committed or uncommitted, within capacity; plan no work in the IP iteration.",
      "Place Features and dependencies on the planning board and list the PI risks. Propose business value; the Business Owners assign it at the gate."],
     ["Is each team's load within its capacity, with uncommitted objectives absorbing the uncertainty?", "Is every cross-team dependency placed before the iteration that needs it?"],
     ["Objectives are split committed and uncommitted per team; risks are listed with a ROAM state."],
     "The Business Owners assign business value and the ART commits with a confidence vote.",
     "`art-gate-decision` (record the commitment and the vote); `feature-transition` for each committed Feature; then `iteration-planning` with each team.",
     draft_conditions=[exists_pre("a-feature-is-ready", "feature", "['ready', 'implementing']")])

loop("release-on-demand", "art", "Release on Demand", "release", f"{ART}/releases/<release-slug>/<release-slug>.release.md", "release-manager",
     ["site-reliability-engineer", "observability-engineer", "security-expert", "quality-engineer", "technical-writer"],
     "Plan one release and assemble its readiness evidence: what is made available to which customers, how, and how its outcome will be measured.",
     "Ship to customers; release readiness; rollout and rollback plan.",
     ["Read the Features released, their acceptance evidence, the NFR register and the pipeline map.",
      "Describe how release is decoupled from deployment, the audience, the rollout steps and a tested rollback.",
      "Link the evidence, do not restate it. Say which outcome will be measured for each Feature's benefit hypothesis."],
     ["Is the rollback tested, and who decides to trigger it?", "Can the benefit hypothesis be measured after release?"],
     ["Scope, strategy, evidence links, rollout and rollback are filled; `status` is `ready` or says what is missing."],
     "Product Management's human lead and the Business Owners decide to release.",
     "`art-gate-decision`; then `feature-transition` (releasing → done) for each Feature released. A later run of this workflow records the result (`released` or `rolled-back`) and the measured outcomes.",
     draft_conditions=[exists_pre("a-feature-is-built", "feature", "['implementing', 'validating-on-staging', 'deploying-to-production', 'releasing']")])

event("art-sync", "art", "ART Sync", "art-sync",
      "Inspect the ART's progress toward its PI Objectives (Coach Sync and PO Sync combined), handle dependencies and impediments, and re-render the ART Kanban.",
      "ART status during the PI; dependencies, impediments or scope adjustments between teams.",
      ["Coach Sync: progress, dependencies and impediments across teams.", "PO Sync: progress toward the PI Objectives and scope adjustments.",
       "Risks to revisit (ROAM).", "Decisions and actions, each with its owner."],
      "A backlog change is its own workflow: `feature-refinement`, `feature-transition`.", kanban=True)

event("system-demo", "art", "System Demo", "system-demo",
      "Show the integrated work of all teams for the iteration from a production-like environment, as an objective measure of progress, and collect feedback.",
      "Demonstrate the integrated increment; what the ART built this iteration.",
      ["What was integrated and demonstrated, per Feature and acceptance criterion.", "What was not ready and why.",
       "NFR verification results.", "Feedback from Business Owners and stakeholders, recorded in their words."],
      "`feature-transition` for Features accepted; feedback feeds `feature-refinement`.")

loop("inspect-and-adapt", "art", "Inspect and Adapt", "event-record", f"{ART}/events/<event-slug>.inspect-and-adapt.md", "release-train-engineer",
     ["agile-coach", "data-analyst"],
     "Evaluate the PI's result and the ART's way of working at the end of the PI, and derive improvement backlog items.",
     "End-of-PI improvement; PI metrics; a recurring problem to solve at ART level.",
     ["Read the PI Objectives with actual business value, the System Demo records, the Kanban and the `friction` notes of the PI's artifacts. Set `event: inspect-and-adapt`.",
      "Three parts: the PI System Demo result, a quantitative and qualitative measurement review (predictability, flow), then a retrospective and problem-solving analysis of the largest problem.",
      "State each improvement as an action that names the workflow which will write the backlog item."],
     ["Do the measures support the conclusions?", "Does the root cause analysis reach a cause the ART can act on?"],
     ["Each improvement action has an owner and a carrying workflow."],
     "The ART's stakeholders decide which improvements enter the ART Backlog.",
     "`enabler-feature-refinement` or `feature-refinement` for each improvement accepted.", predecessors=["system-demo"])

transition("feature-transition", "art", "Feature transition", "feature", f"{ART}/features/<feature-slug>/<feature-slug>.feature.md", "product-manager",
     "funnel → analyzing → ready → implementing → validating-on-staging → deploying-to-production → releasing → done",
     "Record the human's decision to move one Feature (business or enabler) to a new ART Kanban state, then re-render the ART Kanban.",
     "\"Approve / commit / move / accept this Feature\" after a gate, PI Planning, a System Demo or a release.",
     ["A Feature leaves `analyzing` only after it was challenged.", "`implementing` follows the PI commitment and sets `targetPi`.",
      "`done` follows release and the evaluation of the benefit hypothesis."],
     "On `ready`: `pi-planning`. On `implementing`: `story-refinement` with the team's Scrum Master.",
     conditions=[_cond("postcondition", "challenged-before-ready", "workspace.filter(a, a.path == step.artifact.path && !(a.data.status in ['funnel', 'analyzing']))",
                       "selected.all(a, size(a.data.challengeLedger) > 0)")])

gate("art-gate-decision", "art", "ART gate decision")

# =============================== TEAM ====================================================

loop("team-formation", "team", "Team formation", "team-charter", f"{TEAM}/team-charter.md", "scrum-master",
     ["agile-coach", "product-owner", "quality-engineer"],
     "Define or revise one Agile team: its mission, members, working agreements, Definition of Done and Kanban.",
     "Set up a team; change its working agreements, Definition of Done or WIP limits.",
     ["Read the ART canvas and its working agreements.",
      "Keep the team cross-functional and small (ten or fewer), with a Product Owner and a Scrum Master/Team Coach.",
      "Write a Definition of Done that includes the NFR checks, and Team Kanban states with WIP limits."],
     ["Can the team define, build, test and deliver without waiting on another team?", "Is every item of the Definition of Done checkable?"],
     ["Mission, roles, Definition of Done and Kanban states with WIP limits are filled."],
     "The team's human lead decides whether the team works this way.",
     "`team-gate-decision`; then `story-refinement`.")

loop("story-refinement", "team", "Story refinement", "story", f"{TEAM}/stories/<story-slug>/<story-slug>.story.md", "product-owner",
     ["software-engineer", "quality-engineer", "security-expert", "ux-designer"],
     "Write or thicken one Story so it is ready for Iteration Planning: user voice, acceptance criteria and an estimate.",
     "A new story; split a Feature into stories; a spike; a Story-sized defect or debt item; make a Story ready.",
     ["One Story per run, a vertical slice that fits in an iteration. Create it with `status: backlog`, or thicken it without changing its status.",
      "User stories use the user-voice form; an enabler Story (a spike is an exploration enabler) says what must be learned or built.",
      "Write Given/When/Then acceptance criteria and the NFR ids that apply. Set `parent` to the Feature it splits from. Leave `estimate` to the team's challenge."],
     ["Is it independent, negotiable, valuable, estimable, small and testable?", "Does each acceptance criterion describe an observable outcome?"],
     ["The Story statement and acceptance criteria are filled; `estimate` is set from the Software Engineer's packet."],
     "The Product Owner (human) decides whether the Story is ready.",
     "`story-transition` to record the move; then `iteration-planning`.",
     draft_conditions=[parent_post("parent-feature-is-approved", [("feature", "['ready', 'implementing']")])])

loop("iteration-planning", "team", "Iteration Planning", "iteration-plan", f"{TEAM}/iterations/<iteration-slug>/iteration-plan.md", "scrum-master",
     ["product-owner", "software-engineer", "quality-engineer"],
     "Plan one iteration: the iteration goals, the Stories selected and the capacity behind them.",
     "Plan the iteration; what the team commits to; iteration goals.",
     ["Read the team charter, the ready Stories in priority order, the PI Objectives and the last iteration's review.",
      "Select Stories within capacity, then summarize them as iteration goals aligned to the PI Objectives.",
      "The commitment is to the goals, not to the Stories."],
     ["Is the load within capacity, given past velocity?", "Do the goals still make sense if one Story slips?"],
     ["Goals, selected Stories, capacity and load are filled."],
     "The team and the business commit to the iteration goals.",
     "`team-gate-decision` (record the commitment); then `story-implementation` per Story.",
     draft_conditions=[exists_pre("a-story-is-ready", "story", "['ready', 'in-progress']")])

loop("story-implementation", "team", "Story implementation", "code-change", f"{TEAM}/stories/<story-slug>/<story-slug>.code-change.md", "software-engineer",
     ["quality-engineer", "security-expert", "observability-engineer", "database-administrator", "accessibility-specialist"],
     "Implement one ready Story test-first in its code repository and record the change with its evidence; experts review it before the human merges.",
     "Build a story; write the code; fix a defect.",
     ["One Story per run. Read the Story, its Feature, the team's Definition of Done and the architecture decisions that apply.",
      "Work test-first in the code repository on a branch; the code lives there, not in the workspace. Never merge.",
      "Record the change: repository, branch, pull request, summary, the tests and their result, the Definition of Done checked item by item. Set `status: ready-for-review`."],
     ["Do the tests pin down each acceptance criterion, and do they pass?", "Is the change the smallest one that satisfies the Story?"],
     ["Review findings are fixed in the code or answered; tests pass; `status` is `ready-for-review`."],
     "The human reviewer approves and merges the pull request.",
     "`story-transition` (in-review → accepted, by the Product Owner).",
     draft_conditions=[
         exists_pre("a-story-is-ready", "story", "['ready', 'in-progress']"),
         _cond("postcondition", "change-implements-a-planned-story", "workspace.filter(a, a.path == step.artifact.path)",
               "selected.all(a, workspace.exists(s, s.kind == 'story' && s.path == a.data.story && s.data.status in ['ready', 'in-progress', 'in-review']))")])

event("team-sync", "team", "Team Sync", "team-sync",
      "Inspect progress toward the iteration goals, adjust the plan for the coming day, and re-render the Team Kanban.",
      "Daily status of the team; what is blocked; progress toward the iteration goals.",
      ["Progress toward each iteration goal.", "Stories by state, WIP against limits, blocked Stories.",
       "Impediments: next step or escalation for each.", "Items for a 'meet after', not solved here."],
      "A backlog change is its own workflow: `story-refinement`, `story-transition`.", kanban=True)

event("iteration-review", "team", "Iteration Review", "iteration-review",
      "Inspect the iteration increment with stakeholders, assess progress toward the iteration goals and PI Objectives, and adjust the Team Backlog.",
      "End of iteration: what was done; demo the team's increment.",
      ["Each Story demonstrated as a working, tested increment against its acceptance criteria.", "Stories not completed and why.",
       "Iteration goals met or missed; progress toward the PI Objectives.", "Feedback and the backlog adjustments it suggests."],
      "`story-transition` for Stories accepted; then `iteration-retrospective`.")

event("iteration-retrospective", "team", "Iteration Retrospective", "iteration-retrospective",
      "Review the team's practices at the end of the iteration and choose the improvements to try next.",
      "How the team can improve; what went well or badly this iteration.",
      ["Quantitative review: goals met, velocity, flow.", "Qualitative review: what went well, what did not, from the `friction` notes of the iteration's artifacts.",
       "One or two improvements to try, each an improvement Story to write."],
      "`story-refinement` for each improvement Story.", predecessors=["iteration-review"])

transition("story-transition", "team", "Story transition", "story", f"{TEAM}/stories/<story-slug>/<story-slug>.story.md", "product-owner",
     "backlog → ready → in-progress → in-review → accepted",
     "Record the human's decision to move one Story to a new Team Kanban state, then re-render the Team Kanban.",
     "\"This story is ready / started / accepted\".",
     ["A Story leaves `backlog` only after it was challenged.", "`in-progress` sets `iteration`.",
      "`accepted` means the acceptance criteria and the Definition of Done are met and the change is merged."],
     "On `ready`: `iteration-planning`. On `in-progress`: `story-implementation`.",
     conditions=[_cond("postcondition", "challenged-before-ready", "workspace.filter(a, a.path == step.artifact.path && a.data.status != 'backlog')",
                       "selected.all(a, size(a.data.challengeLedger) > 0)")])

gate("team-gate-decision", "team", "Team gate decision")

WF = {w["slug"]: w for w in WORKFLOWS}
