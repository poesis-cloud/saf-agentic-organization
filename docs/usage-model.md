# Usage model

This is how a human talks to the organization. Orchestrators are instructed from this
document; workflow `description` fields restate each catalog's purpose and mains.
Catalog rows implement SAFe; they are not themselves usage principles.

## Principles

1. **SAFe activity purpose constrains usecases.** A human concern is valid here only
   when it matches an existing catalog purpose at this layer. Orchestrators map
   speech onto that purpose; they do not invent ceremonies.
2. **Any concern, any form.** The human states a concern. They do not classify it,
   name a ceremony, or pick an act. The orchestrator maps it to one workflow, or
   hands the human the other-layer orchestrator to invoke.
3. **IT concerns stay inside SAFe grain.** Impact, bug, spike, debt, quality gap,
   constraint, decision — each maps onto an existing activity at Epic, Feature, or
   Story grain. Do not add parallel IT rituals.
4. **Workflows are challenge loops.** Specialists draft, challenge, and rewrite
   until challengers agree enough. Inner reviews are not the human loop.
5. **Human gate.** Each workflow delivers its mains to the human. The human reviews
   those artifacts and accepts, concerns, or rejects them. Challenge packets are
   evidence, not the thing the human is asked to score.

## 1. One layer, one grain

The human speaks to one layer orchestrator. That hat writes (new or thickens) work
items of **that layer's grain**, inside the matching SAFe activity:

| Hat | Grain |
|---|---|
| `@value-management-officer` | Epic (business or enabler, judged in-workflow) |
| `@release-train-engineer` | Feature (business or enabler, judged in-workflow) |
| `@scrum-master` | Story (business or enabler, judged in-workflow) |

The user does not pick business vs enabler. Sibling mains of the owning activity
are in-workflow writes. Wrong grain is a handoff: tell the human which
orchestrator to invoke. Do not mint a thinner item to absorb a thicker intent.

## 2. Workflows are challenge protocols

A workflow is how agents **exchange, collaborate, and challenge** while delivering
mains. The loop is draft → challenge → owner rewrite; a human KO reiterates the
workflow as a new instance until agreement is enough to present mains at the gate.

| Class | Role | Challenged? | Human-gated? |
|---|---|---|---|
| **Main** | The work item or decision the activity exists to produce | Yes, before owner commit | **Yes** |
| **Challenge / mediation** | Required because 1 step = 1 artifact (reviews, minutes, risks, kanban/manifests) | **No** | **No** |

Owner rewrite absorbs challenge findings. Challengers write no owner content. After the
challenge, every drafted main gets an owner step (one artifact each), so no main is left
contradicting the rewritten one: in `epic-lean-business-case`, `update-epic` and
`update-enabler-epic` align the Epic and the Enabler Epic with the rewritten Lean Business Case.

## 3. Map or hand off

The orchestrator does not require a speech-act label. It:

1. Reads the concern.
2. Loads the one workflow whose **purpose** matches, or tells the human to invoke
   another layer's orchestrator.
3. Dispatches each step the harness resolves exactly once (1 step = 1 session); a
   failed step comes back through `resolve-step`, never through an ad-hoc re-dispatch.
4. Returns the **mains** to the human gate and waits.

Humans need not name the ceremony. Purpose still constrains the usecase. The
harness `resolve-step` walks catalog order; empty preconditions pass. **No valid
step without artifact:** every step commits a change to exactly one instance of its
declared artifact kind, whatever the outcome. An out-of-scope sibling main is committed with only a `no-change`
`stepOutcomes` entry, and an unneeded enabler as a `status: not-needed` file —
never a silent skip, never an invented sibling, never a redraft of an untouched
item. Agent replies and reports are indicative; committed artifacts are the
only evidence (see [step-artifacts.md](step-artifacts.md)).

## 4. Per-workflow purpose

| Workflow | Purpose | Mains presented at the human gate |
|---|---|---|
| `epic-lean-business-case` | Write a portfolio bet | `epic`, `lean-business-case`, `epic-enabler` |
| `architectural-vision` | Portfolio runway + NFR backbone; records its decisions on Epics, writes no Epic | `architecture-vision` |
| `epic-vision-alignment` | Write the Vision's decisions on ONE Epic into it (one run per Epic the Vision names) | `epic-enabler`, `epic`, `lean-business-case` (owner updates) |
| `strategic-investment-planning` | Allocate / guardrail ART funding | `budget-allocation` |
| `strategic-portfolio-review` | Keep / pivot / stop / re-rank | themes, vision, roadmap, `architecture-vision` |
| `portfolio-sync` | Portfolio snapshot; registers ONE product per run | `portfolio-sync`, `portfolio-manifest`, `product-manifest`, `portfolio-kanban` |
| `epic-transition` | Move ONE Epic (and its enabler) to a new `status:` | `epic`, `epic-enabler` (owner steps), `portfolio-kanban` |
| `feature-derivation` | Split an approved Epic into ART Features (refused while no Epic is approved) | `feature`, `feature-enabler` |
| `feature-backlog-refinement` | Write a PI-ready Feature | `feature`, `feature-enabler` |
| `architectural-runway-extension` | Extend ART runway (product NFR register before ADR); its decisions written into the Features by their owners | `nfr-list`, `adr`, `architecture-runway`, `feature`, `feature-enabler` (owner updates) |
| `feature-transition` | Move ONE Feature (and its enabler) to a new `status:` | `feature`, `feature-enabler` (owner steps), `program-kanban` |
| `pi-planning` | ART PI commit | confirm vision/roadmap/feature/runway; write `objectives` |
| `art-sync` | Mid-PI impediments | mediation record only |
| `system-demo` | Inspect the increment; demo gate | mediation / gate record |
| `inspect-and-adapt` | PI improve | `inspect-and-adapt` record (metrics, then triage). Writes no pain point; a later Feature is a later Feature |
| `improvement-backlog` | Record or update ONE pain point (one run per friction note) | `pain-point` (mediation) |
| `release-on-demand` | Ship an accepted increment | `release-on-demand` |
| `team-backlog-refinement` | Write a ready-enough Story (including Feature→Story split) | `story`, `story-enabler` |
| `story-transition` | Move ONE Story (and its enabler) to a new `status:` | `story`, `story-enabler` (owner steps) |
| `iteration-planning` | Commit the iteration | `team-manifest`, `plan` |
| `pair-programming` | Implement an already-OK Story | `code-change` |
| `verification` | Is this Story done | `qa-signoff` (challenge of Story/code-change) |
| `team-sync` / `iteration-review` / `iteration-retrospective` | Daily I&A / increment inspect / team improve | mediation records |

An impediment discovered in sync/demo that is really a Feature is a **later
Feature**, not a new workflow. Orchestrators hold no Epic/Feature/Story privilege:
the unit's author creates it in its authoring workflow, and every later `status:`
change (gate, PI commit, block, roll-up, close) is one `*-transition` run whose
owner step commits it ([step-artifacts.md](step-artifacts.md#status-transitions)).

## 5. NFR model (catalog, not a usage principle)

SAFe NFRs are enduring system qualities that constrain backlogs. This organization
encodes that as a **product register** plus traces — not as Feature AC. There is
no separate relation artifact: the bind lives on existing mains.

| Artifact | Owns | Operated in | Does not own |
|---|---|---|---|
| `architecture-vision` | Cross-product NFR **backbone** | `architectural-vision` draft | Measurable product NFRs |
| `portfolio/products/<product-slug>/nfr-list.md` | Canonical product NFRs | `architectural-runway-extension` / `author-nfrs`, `update-nfrs` | Feature AC, Stories, ADRs |
| Feature / Feature-enabler | Which NFRs **apply** (optional tightening) | `feature-backlog-refinement` draft + owner rewrite | The canonical set |
| Story / Story-enabler | Inherit parent Feature applicability; **verify** | `team-backlog-refinement` draft + owner rewrite | The canonical set |
| ADR | Design that realizes NFRs | `architectural-runway-extension` / `author-adr`, `update-adr` | The NFR register |
| `architecture-runway` | Enabler work that paves NFRs / ADRs | `architectural-runway-extension` rewrite | The NFR text |
| `architecture-review` / `security-review` | Missed or invented applicability | Feature and Story refinement challenges | The register or the work item |

Epic / Epic-enabler record **portfolio backbone implications** (EA hat), not product NFR ids.
`feature-derivation` mints Feature identity only; NFR traces stay deferred until Feature
refinement. A missing NFR discovered in refinement is a runway handoff, not Feature AC.

## 6. Splitting vs refinement

SAFe names the **work-item hierarchy** (Epic → Feature → Story) and the act of
**splitting**. It does not name a Feature-to-Story derivation ceremony.

| Split | SAFe concept | This catalog |
|---|---|---|
| Epic → Feature | Portfolio Epics split into Features on the ART backlog | `feature-derivation`, then `feature-backlog-refinement` |
| Feature → Story | Teams split Features into Stories on the Team backlog | `team-backlog-refinement` only — no `story-derivation` |

Derivation **mints** the thinner grain from an approved parent. Refinement **shapes**
that grain (AC, WSJF, NFR traces, challenges) until it is ready.

Do **not** fold Epic→Feature minting into Feature refinement. That split is
**cross-layer**: the parent is a portfolio Epic (VMO grain); Feature refinement's
hat is ART and already refuses Epic grain. Merging would either accept Epic-sized
intent inside a PI-ready Feature workflow, or silently mint Features inside a
challenge loop built for shaped items. Derivation has no challenges because the
minted files are stubs; they enter refinement next. Feature→Story stays inside
Team grain — the parent Feature already exists on the ART — so mint+shape can
share `team-backlog-refinement`. Do not invent a Story-derivation workflow.
