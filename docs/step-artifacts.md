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

# Step artifacts — no valid step without artifact

> "A step necessarily produces an artifact. Agents collaborate on these artifacts. That's how we
> can harness a maximum of collaborative work, and trace it, on the basis of artifacts. Reports
> should be indicative. No valid step without artifact."

## Rule

- Every workflow step declares one `artifact:` (all steps in [`workflows/`](../workflows/) do).
- The step's actor commits a change to **exactly one** instance of that artifact kind on every
  run, by creating or updating it, whatever the outcome. The harness enforces this with a
  mandatory built-in postcondition (function 10): the step's session must have committed, through
  the harness, exactly one instance of the declared kind; a write identical to the committed file
  does not count. There is no opt-out and no per-step existence postcondition in this repository.
- One step = one session: the orchestrator dispatches each resolved step exactly once. A failed
  step is resolved again through `resolve-step`, never re-dispatched ad hoc.
- Every artifact write is governed: written in a registered step session, authorized by the
  harness (function 8), then checked and committed (function 9). Nothing is written "outside a
  step" on another agent's behalf.
- Agent replies, step outcomes, subagent reports and gate summaries are **indicative**. Committed
  artifacts are the only evidence.

## How a decision is recorded

Each artifact schema defines an optional `stepOutcomes` list (canonical definition in
[`artifacts/framework-definitions.schema.json`](../artifacts/framework-definitions.schema.json)),
and every template carries `stepOutcomes: []`. Each step that commits the artifact appends one
entry:

```yaml
stepOutcomes:
  - step: feature-backlog-refinement/draft-enabler   # <workflow-slug>/<step-slug>
    outcome: none        # written | revised | confirmed | no-change | none
    date: "2026-11-05"
    note: No enabler needed — the runway already provides tenant-scoped auth (ADR-12).
    friction: The Epic named no tenant boundary; had to infer it.   # optional
```

`friction` records workflow friction the actor observed. Actors never write pain points
themselves: the `release-train-engineer` turns friction notes into pain points, one per run of
the `improvement-backlog` workflow (`record-pain-point`).

| Outcome | Meaning | Typical step |
|---|---|---|
| `written` | The artifact was created. | Any draft step. |
| `revised` | Content changed. | Thicken, owner rewrite, pain-point update. |
| `confirmed` | Reviewed and still valid, content unchanged. | PI/iteration `confirm-*` steps. |
| `no-change` | Out of scope on this run; deliberately untouched. | Sibling mains, owner rewrite with nothing to absorb. |
| `none` | Not needed; the artifact records that decision. | Enabler `status: not-needed`, "no new decision" ADR, empty NFR register. |

The appended entry also guarantees a diff, so `confirmed` and `no-change` steps commit too.

## Not-needed enablers

When a Demand needs no enabler, the architect still commits the sibling enabler file beside the Demand (for example
`portfolio/portfolio-backlog/<epic-slug>/<epic-slug>.epic-enabler.md`) with
`status: not-needed`, the rationale (in `## Enablement rationale`, `## Enabler intent` or
`## Enabler story intent`) and an `outcome: none` entry. A `not-needed` enabler is a recorded decision: it
leaves the kanban flow, is not challenged as a main (a challenger may contest the decision
itself), and is presented as a decision at the human gate.

## Status transitions

Orchestrators decide and request transitions; they never write an Epic, Feature or Story. The
access-control list grants them only their flow records (kanbans, sync records, manifests,
plans, objectives, demo and I&A records, pain points for the RTE). A unit is created, with its initial `status:`,
by its authoring workflow's first step; every later change is one run of its tier's transition
workflow, whose owner steps record ONE requested transition (`revised`) or refuse it with the
reason (`no-change`):

| Workflow | Orchestrator | Steps (actor → artifact) |
|---|---|---|
| `epic-transition` | `value-management-officer` | `transition-epic` (business-owner → epic), `transition-enabler` (enterprise-architect → epic-enabler), `update-portfolio-kanban` (VMO → portfolio-kanban) |
| `feature-transition` | `release-train-engineer` | `transition-business` (product-manager → feature), `transition-enabler` (system-architect → feature-enabler), `update-program-kanban` (RTE → program-kanban) |
| `story-transition` | `scrum-master` | `transition-story` (product-owner → story), `transition-enabler` (system-architect → story-enabler); the Team Kanban is rendered in the next `team-sync` record |

Cost roll-ups are written by the same owner steps (Epic `done`, Feature `done`, Story
`awaiting-pr`). Gate decisions and unresolved findings live as `openItems` on the unit, written by
its author. [`tests/functional/test_orchestrator_writes.py`](../tests/functional/test_orchestrator_writes.py)
keeps the catalogue, the ACL and the orchestrator prose in line: no orchestrator text describes it
committing a kind it is not granted.

## Redesigned steps

| Workflow / step | Before | Now |
|---|---|---|
| `epic-lean-business-case/draft-epic` | No-change note in the reply | Commits the existing Epic with a `no-change` entry |
| `epic-lean-business-case/discovery-and-draft` | "or explicitly none" | "No open items" recorded in the LBC's `stepOutcomes` note |
| `epic-lean-business-case/draft-enabler-epic` | explicit-none | `not-needed` Enabler Epic, `outcome: none` |
| `epic-lean-business-case/owner-rewrite` | No-change on the LBC | Commits the LBC with a `no-change` entry |
| `feature-derivation/derive-enabler` | explicit-none | `not-needed` Enabler Feature, `outcome: none` |
| `feature-backlog-refinement/draft-business` | No-change note | Commits the Feature with a `no-change` entry |
| `feature-backlog-refinement/draft-enabler` | explicit-none | `not-needed` Enabler Feature, `outcome: none` |
| `feature-backlog-refinement/owner-rewrite-business` | No-change; did not wait for the feasibility review | Commits the Feature with a `no-change` entry, after all four challenges |
| `feature-backlog-refinement/owner-rewrite-enabler` | No-change | Commits the Enabler Feature with a `no-change` entry |
| `architectural-runway-extension/author-nfrs` | explicit-none | Commits the register with `no-change` (or creates it empty with `none`) |
| `architectural-runway-extension/author-adr` | "No new decision" note | Commits an ADR whose decision is "no new decision", `outcome: none` |
| `architectural-runway-extension/owner-rewrite` | Replay named in the reply | Replay recorded in the runway register; `no-change` when nothing changes |
| `team-backlog-refinement/draft` | No-change note; "or explicitly none" | Commits the Story with a `no-change` entry; "no open items" in its note |
| `team-backlog-refinement/draft-enabler` | explicit-none | `not-needed` Enabler Story, `outcome: none` |
| `team-backlog-refinement/owner-rewrite` | No-change | Commits the Story with a `no-change` entry |
| `team-backlog-refinement/owner-rewrite-enabler` (new) | The Enabler Story was never revisited after the challenge | The System Architect rewrites it (`no-change` when not-needed or out of scope) |
| `epic-lean-business-case/update-epic`, `update-enabler-epic` (new) | The Epic and Enabler Epic could contradict the rewritten LBC (scope, `dependsOn`, first-release scope) | Their owners align each one with the LBC, one artifact per step (`no-change` when already consistent) |
| `architectural-runway-extension/update-nfrs`, `update-adr` (new) | The NFR list and the ADR were never revisited after the challenge | The System Architect updates each one before rewriting the runway register (`no-change` when no finding applies) |
| `inspect-and-adapt/metrics-review` | Several pain points per run | Creates the one `inspect-and-adapt` record (metrics + pain-point candidates) |
| `inspect-and-adapt/pi-retrospective` | Several pain points per run; priming as text | Updates that record with the triage and PI+1 priming |
| `improvement-backlog/record-pain-point` (new workflow) | Pain points written by specialists or "outside a step" | The RTE creates or updates exactly one pain point per run (`no-change` entry when it already holds) |
| `pi-planning/confirm-intent` | Several Features | Confirms the ONE Feature this PI Planning run commits |
| `portfolio-sync/update-product-manifest` | Several products | One product manifest per run |
| `feature-derivation/derive-business` | Several Features | One business Feature per run (the workflow runs once per Feature) |
| `epic-transition`, `feature-transition`, `story-transition` (new workflows) | Orchestrators flipped `status:` on Epics, Features and Stories outside any step | The unit's owner commits each transition in a governed step |
| Challenge steps (shared challenger rule) | "Not a main to challenge" | Review packet always committed (`verdict: pass` when nothing is found) |
| `pi-planning/confirm-*`, `iteration-planning/confirm-team-manifest`, `release-on-demand/confirm-deployment` | Implicit confirmation | Artifact committed with a `confirmed` entry |

Tests in [`tests/functional/test_step_artifacts.py`](../tests/functional/test_step_artifacts.py)
keep every schema and template carrying `stepOutcomes`, the enablers admitting `not-needed`, and
the instructions, skills and agents free of reply-only outcomes.
