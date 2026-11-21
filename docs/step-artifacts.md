<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Step artifacts: no valid step without artifact

> A step necessarily produces an artifact. Agents collaborate on these artifacts, and that is
> what makes their work traceable. Replies are indicative; committed artifacts are the only
> evidence.

## The rule

- Every workflow step declares one `artifact:` kind and one `actor:`.
- The step's actor commits a change to **exactly one** instance of that kind on every run,
  whatever the outcome. The harness enforces it (function 10): the step's session must have
  committed, through the harness, exactly one instance of the declared kind, and a write identical
  to the committed file does not count.
- One step is one session. The orchestrator dispatches each resolved step once; a failed step
  comes back through `resolve-step`, never through an ad hoc re-dispatch.
- Every write is governed: authorized against the access control list (function 8), validated
  against the kind's schema and committed (function 9), and promoted into the workspace only when
  the step's postconditions hold (function 10).

The rule is injected into every worker session as the
[step contract](../instructions/shared/step-contract.instructions.md).

## Artifact classes

| Class | What it is | Who writes it | Challenged | Human-gated |
|---|---|---|---|---|
| **main** | The SAFe artifact a workflow exists to produce (30 kinds: Epic, enabler Epic, Feature, PI Objectives, release…) | its owner, a SAFe role or the expert whose job it is | yes, by its expert panel | yes |
| **challenge** | One expert's findings on one main artifact | the expert | no | no: it is evidence at the gate |
| **record** | A flow record: event record, Kanban board, gate decision | the layer's orchestrator | no (Inspect and Adapt records are) | it records the gate |

Every kind has a JSON Schema under [`artifacts/`](../artifacts/), a template under
[`templates/`](../templates/) and a path in [`conf/workspace.conf.yaml`](../conf/workspace.conf.yaml).
The list is in [catalog.md](catalog.md#artifact-kinds).

## How a step records its decision: `stepOutcomes`

Every artifact carries a `stepOutcomes` list. Each step that commits the artifact appends one
entry:

```yaml
stepOutcomes:
  - step: feature-refinement/revise      # <workflow-slug>/<step-slug>
    outcome: revised                     # written | revised | confirmed | no-change | none
    date: "2026-11-21"
    note: Accepted 4 findings, rejected 1 (AC6 is out of scope for this PI), deferred 1 to nfr-refinement.
    friction: The NFR register has no accessibility entry yet.   # optional
```

| Outcome | Meaning | Typical step |
|---|---|---|
| `written` | The artifact was created. | a first draft, a challenge packet, an event record |
| `revised` | Its content changed. | a thickened draft, an owner revision, a state change |
| `confirmed` | Reviewed and still valid, content unchanged. | a revision with nothing to change, a board that did not move |
| `no-change` | Deliberately untouched, with the reason. | a refused state change |
| `none` | Not needed; the artifact records that decision. | reserved for an artifact that states its own absence |

The appended entry guarantees a change, so `confirmed` and `no-change` steps still deliver.
`friction` is raw input for Inspect and Adapt and the Iteration Retrospective, which read it.

## How a challenge is recorded

An expert writes one **challenge packet** beside the artifact it challenges, at
`<folder of the artifact>/challenges/<workflow-slug>-<agent-slug>.challenge.md`:

```yaml
target: portfolio/arts/billing/features/invoice-pdf/invoice-pdf.feature.md
targetKind: feature
challenger: security-expert
verdict: concerns          # pass | concerns | blocking | not-applicable
findings:
  - id: F1
    severity: major        # blocking | major | minor
    claim: Any authenticated user can export any invoice by guessing its id.
    evidence: AC2 checks the session, no criterion checks ownership of the invoice.
    ask: Add a criterion that an export of another customer's invoice is refused.
```

The owner answers in the artifact's **challenge ledger**, one entry per packet of the run:

```yaml
challengeLedger:
  - packet: portfolio/arts/billing/features/invoice-pdf/challenges/feature-refinement-security-expert.challenge.md
    challenger: security-expert
    verdict: concerns
    responses:
      - finding: F1
        disposition: accepted    # accepted | rejected | deferred
        note: AC7 added: exporting an invoice of another customer returns "not found".
```

On a rerun the expert updates its packet in place and the owner replaces the ledger; Git keeps
the history.

## How a human decision is recorded

- **Items with a state:** backlog items (Epic, Capability, Feature, their enablers, Story) and
  architecture decisions, releases, supplier agreements and code changes. The owner appends an
  entry to `transitions` and sets `status`, in the item's `*-transition` workflow. For a backlog
  item the orchestrator then re-renders the Kanban board from the items; the items stay the
  source of truth. An owner who finds the move illegal records a refusal (`no-change`), which is
  a valid step.
- **Every other main artifact:** the orchestrator writes a `gate-decision` record in its layer's
  gate-decision workflow, with the decision and the human's concerns in their words.

Orchestrators never write a backlog item; the access control list does not grant it to them.

## Tests

[`tests/functional/test_workflow_runs.py`](../tests/functional/test_workflow_runs.py) runs every
workflow of the catalog to its gate through the real harness and proves each refusal;
[`tests/functional/test_artifacts.py`](../tests/functional/test_artifacts.py) keeps schemas,
templates and the layout in agreement.
