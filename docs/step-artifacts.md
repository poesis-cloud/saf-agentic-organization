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
- The step's actor commits an instance of that artifact on every run, whatever the outcome. The
  harness enforces this with a mandatory built-in postcondition: the declared artifact must have
  an instance committed by that step's session. There is no opt-out and no per-step existence
  postcondition in this repository.
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
    date: 2026-11-05
    note: No enabler needed — the runway already provides tenant-scoped auth (ADR-12).
```

| Outcome | Meaning | Typical step |
|---|---|---|
| `written` | The artifact was created. | Any draft step. |
| `revised` | Content changed. | Thicken, owner rewrite, pain-point update. |
| `confirmed` | Reviewed and still valid, content unchanged. | PI/iteration `confirm-*` steps. |
| `no-change` | Out of scope on this run; deliberately untouched. | Sibling mains, owner rewrite with nothing to absorb. |
| `none` | Not needed; the artifact records that decision. | Enabler `status: not-needed`, "no new decision" ADR, empty NFR register. |

The appended entry also guarantees a diff, so `confirmed` and `no-change` steps commit too.

## Not-needed enablers

When a Demand needs no enabler, the architect still commits the sibling file
(`<slug>.epic-enabler.md`, `<slug>.feature-enabler.md`, `<slug>.story-enabler.md`) with
`status: not-needed`, the rationale (`## Overview`, or one `## Acceptance Criteria` bullet for a
Story enabler) and an `outcome: none` entry. A `not-needed` enabler is a recorded decision: it
leaves the kanban flow, is not challenged as a main (a challenger may contest the decision
itself), and is presented as a decision at the human gate.

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
| `feature-backlog-refinement/owner-rewrite-business` | No-change | Commits the Feature with a `no-change` entry |
| `feature-backlog-refinement/owner-rewrite-enabler` | No-change | Commits the Enabler Feature with a `no-change` entry |
| `architectural-runway-extension/author-nfrs` | explicit-none | Commits the register with `no-change` (or creates it empty with `none`) |
| `architectural-runway-extension/author-adr` | "No new decision" note | Commits an ADR whose decision is "no new decision", `outcome: none` |
| `architectural-runway-extension/owner-rewrite` | Replay named in the reply | Replay recorded in the runway register; `no-change` when nothing changes |
| `team-backlog-refinement/draft` | No-change note; "or explicitly none" | Commits the Story with a `no-change` entry; "no open items" in its note |
| `team-backlog-refinement/draft-enabler` | explicit-none | `not-needed` Enabler Story, `outcome: none` |
| `team-backlog-refinement/owner-rewrite` | No-change | Commits the Story with a `no-change` entry |
| `inspect-and-adapt/metrics-review` | User-facing output only | Top deviations committed as `origin: metrics-review` pain points (or one "within plan" record) |
| `inspect-and-adapt/pi-retrospective` | PI+1 priming as text | Priming is indicative only; decisions stay on the pain points |
| Challenge steps (shared challenger rule) | "Not a main to challenge" | Review packet always committed (`verdict: pass` when nothing is found) |
| `pi-planning/confirm-*`, `iteration-planning/confirm-team-manifest`, `release-on-demand/confirm-deployment` | Implicit confirmation | Artifact committed with a `confirmed` entry |

Tests in [`tests/functional/test_step_artifacts.py`](../tests/functional/test_step_artifacts.py)
keep every schema and template carrying `stepOutcomes`, the enablers admitting `not-needed`, and
the instructions, skills and agents free of reply-only outcomes.
