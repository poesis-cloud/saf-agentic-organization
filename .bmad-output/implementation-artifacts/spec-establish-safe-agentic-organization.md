---
title: 'Establish the SAFe agentic organization'
type: 'feature'
created: '2026-08-24'
status: 'done'
baseline_commit: '63d3712c9212033435723e557b7fce886cb12372'
context:
  - '{project-root}/saf/saf-agentic-organization/README.md'
  - '{project-root}/saf/saf-agentic-harness/src/config/config_loader.py'
  - '{project-root}/saf/saf-agentic-harness/contracts/conf/framework/workflow.conf.schema.json'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `saf-agentic-organization` is published v0.1 source (14 agents, 32 skills, 15 workflows) but is not an established SAFe-for-agents application: ceremony skill/workflow pairs are incomplete, required-reading links are self-aliases, `plugin.json` is stale, the PM skill is still Poesis GitHub-sync (dirty fold in tree), and there are zero tests against harness contracts.

**Approach:** Reconcile the framework tree so this checkout is a loadable `FRAMEWORK_DIR`, SAFe-faithful for AI agents, then add an organization-owned unit+functional suite (≥95%) and `make verify`. Stay on `main` and fold the dirty PM skill into the SAFe Feature-author rewrite.

## Boundaries & Constraints

**Always:**
- Stay on `main`. Fold `skills/product-manager.skill.md`; do not revert it.
- Apache-2.0 headers on every shipped `agents|skills|instructions|conf|templates|artifacts` file.
- Workflows validate against harness `workflow.conf` v1: 1 step = 1 actor = 1 artifact; every `actor` is an ACL agent; every `artifact` has a schema; every `instructions`/`skills` slug resolves to a file.
- Three orchestrators only: VMO / RTE / SM. Human remains Central Supervisor at ★ gates. No PRD; Epic carries defining intent.
- Adapt SAFe ceremonies to agents (drop purely human-room facilitation; keep ART Sync, System Demo, Daily, Retro, I&A, PI, iteration plan/review).
- Existing defs may be sourced, improved, or redefined. Prefer smallest coherent rewrite over parallel trees.
- Organization tests cover this live tree (not only synthetic harness fixtures).

**Ask First:**
- Changing published `plugin.json` `version` away from `0.1.0`.
- Deleting a ceremony that official SAFe names if no agent analog is proposed as replacement.
- Editing `saf-agentic-harness` source (only if a contract bug blocks loading this tree).

**Never:**
- Do not invent a READ ACL or restore human-only leftovers already removed.
- Do not modify `saf-agentic-workspace` or `saf-sie-bridge`.
- Do not commit unless the human asks.
- Do not treat harness synthetic fixtures as a substitute for loading this organization.
- Do not add a second host renderer.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Live load | `FRAMEWORK_*` pointed at this checkout + sibling workspace dir | `ConfigLoader` loads layout, ACL, model-profiles, workspace, workflow catalog | `ConfigurationError` with code; test fails |
| Missing ceremony pair | skill `program-art-sync` / `team-daily-sync` / `team-retrospective` / System Demo without matching workflow | establishment tests fail | add the missing workflow (and System Demo skill) |
| Stale plugin skill | `plugin.json` path that is not `skills/<slug>.skill.md` | `render_bundle.py` and coherence tests fail | rewrite manifest to 1:1 agents + skills |
| Broken required-reading | VMO `lpm.skill.md` or RTE `art.skill.md` href missing or self-alias | coherence tests fail | distinct readable file whose title matches the label |
| Sealed / extra agent | `tools.yaml` agents ≠ `plugin.json` agents | `render_bundle.py` exits 1 | align maps |

</frozen-after-approval>

## Code Map

- `saf/saf-agentic-organization/agents/*.agent.md` -- 14 personas; VMO/RTE required-reading currently self-aliases
- `saf/saf-agentic-organization/skills/*.skill.md` -- 32 playbooks; PM body is Poesis-internal; dirty description already started
- `saf/saf-agentic-organization/conf/workflows/*.workflow.conf.yaml` -- 15 ceremonies; missing art-sync, system-demo, daily-sync, retrospective
- `saf/saf-agentic-organization/conf/access-control-list.conf.yaml` -- actor/role grants the harness enforces
- `saf/saf-agentic-organization/conf/model-profiles.conf.yaml` -- capability tags every step must use
- `saf/saf-agentic-organization/conf/workspace.conf.yaml` -- workspace blueprint
- `saf/saf-agentic-organization/artifacts/*.artifact.schema.json` -- one schema per workflow `artifact`
- `saf/saf-agentic-organization/instructions/` -- step/workflow instruction slugs
- `saf/saf-agentic-organization/builds/github-copilot/plugin.json` -- host manifest; skills list stale + ghost nested PM path
- `saf/saf-agentic-organization/builds/github-copilot/tools.yaml` -- must 1:1 match plugin agents
- `saf/saf-agentic-organization/builds/github-copilot/render_bundle.py` -- only Python in-repo today
- `saf/saf-agentic-harness/src/config/config_loader.py` -- live-load API (do not fork)
- `saf/saf-agentic-harness/tests/functional/` -- pattern for driving harness commands; org suite should point at this tree
- `saf/saf-agentic-organization/.github/workflows/ci.yml` -- lint + WITHHOLD only; no pytest

## Tasks & Acceptance

**Execution:**
- [x] `skills/product-manager.skill.md` -- replace Poesis GitHub-sync body with the SAFe Feature-author contract already in `agents/product-manager.agent.md` (handlers `Feature ∅→funnel` / `funnel→refined`; no enablers/gates/stories) -- fold the dirty description into that rewrite
- [x] `skills/lpm.skill.md` and `skills/art.skill.md` -- extract the procedure halves promised by VMO/RTE required-reading so each label resolves to a distinct file
- [x] `agents/value-management-officer.agent.md` and `agents/release-train-engineer.agent.md` -- point required-reading at those files; keep relative links inside `skills/`
- [x] `conf/workflows/art-sync.workflow.conf.yaml`, `system-demo.workflow.conf.yaml`, `daily-sync.workflow.conf.yaml`, `retrospective.workflow.conf.yaml` -- add schema-valid ceremonies; RTE/SM orchestrators; pair with `program-art-sync`, new `program-system-demo`, `team-daily-sync`, `team-retrospective`
- [x] `skills/program-system-demo.skill.md` -- add the missing System Demo playbook (ART increment review / Demo Gate packet; not iteration-review)
- [x] `builds/github-copilot/plugin.json` -- `agents` 1:1 with `agents/*.agent.md`; `skills` 1:1 with `skills/*.skill.md`; drop the ghost nested PM path; keep version `0.1.0` unless asked
- [x] `builds/github-copilot/tools.yaml` -- keep agent keys 1:1 with the manifest (render already fail-closes)
- [x] `tests/unit/` -- coherence: every workflow/skill/instruction/agent/schema/template slug resolves; ceremony skill↔workflow pairing; ACL actors cover every `actor`/`orchestrator`; no broken markdown skill links
- [x] `tests/functional/` -- set `FRAMEWORK_*` at this checkout, load via `ConfigLoader`, drive harness `start-session` / `resolve-step` / `check-step-*` on at least one portfolio, program, and team workflow
- [x] `tests/unit/test_render_bundle.py` -- render to tmp; injected `tools:` present; refuse stale maps
- [x] `Makefile` -- `verify` / `unit` / `functional` mirroring harness; coverage gate ≥95% on organization Python + test-asserted content loaders
- [x] `.github/workflows/ci.yml` -- add the same `make verify` job (do not rename existing `.yml`)
- [x] `README.md` -- document the ceremony set, load contract, and `make verify`

**Acceptance Criteria:**
- Given this checkout as `FRAMEWORK_DIR`, when `ConfigLoader` loads layout/ACL/profiles/workspace/workflows, then no `ConfigurationError` is raised.
- Given the four agent-adapted ceremonies (ART Sync, System Demo, Daily, Retro), when coherence tests run, then each has a workflow + skill + orchestrator step list that is schema-valid.
- Given VMO or RTE required-reading, when the agent file is parsed, then both listed skill paths exist and are not the same file under two labels.
- Given `plugin.json` and `tools.yaml`, when `render_bundle.py` runs, then it exits 0 and the skills list contains no path outside `skills/*.skill.md`.
- Given the PM skill, when an implementer loads it, then it describes SAFe business-Feature authoring only (not Poesis GitHub Project sync).
- Given `make verify`, when the suite finishes, then unit + functional tests pass and reported coverage is ≥95%.

## Spec Change Log

## Design Notes

Harness `ConfigLoader` contract-validates YAML and some semantic rules (ACL roles, workflow DAG, orchestrator files, artifact schemas). It does **not** check skill/instruction file existence — that is the organization's coherence suite.

Ceremony slugs: workflow stem is the SAFe name (`art-sync`); skill keeps the existing layer prefix (`program-art-sync`). Do not rename the 15 existing workflows unless a slug is wrong for SAFe.

Functional tests may import harness `src/` by setting `PYTHONPATH` to the sibling `saf-agentic-harness` checkout (this workspace). Do not vendor harness code.

## Verification

**Commands:**
- `python3 -c "from pathlib import Path; import sys; sys.path.insert(0,'../saf-agentic-harness/src'); ... ConfigLoader(...).load_workflow_catalog(Path('.'))"` -- expected: catalog loads (also covered by `tests/functional`)
- `make verify` -- expected: pytest unit+functional green, coverage ≥95%
- `python3 builds/github-copilot/render_bundle.py . /tmp/saf-org-bundle` -- expected: exit 0
- existing markdownlint / yamllint / license-header / WITHHOLD jobs -- expected: still green

## Suggested Review Order

**Load contract**

- Checkout is a loadable `FRAMEWORK_DIR` via sibling ConfigLoader.
  [`.env:2`](../../../.env#L2)

- Live catalog + Application construct against this tree.
  [`test_live_load.py:39`](../../../tests/functional/test_live_load.py#L39)

- Portfolio / ART / Daily authorization paths are resolvable.
  [`test_live_load.py:50`](../../../tests/functional/test_live_load.py#L50)

**Ceremonies**

- ART Sync is a schema-valid RTE ceremony paired with `program-art-sync`.
  [`art-sync.workflow.conf.yaml:15`](../../../conf/workflows/art-sync.workflow.conf.yaml#L15)

- Workspace root stays `portfolio` so ART Sync lands under `art/<art>/pi-*`.
  [`workspace.conf.yaml:28`](../../../conf/workspace.conf.yaml#L28)

- PI folder now owns `art-sync.md` + `system-demo.md`.
  [`workspace.conf.yaml:256`](../../../conf/workspace.conf.yaml#L256)

- Team folder now owns Daily Sync / Retro / iteration-review.
  [`workspace.conf.yaml:222`](../../../conf/workspace.conf.yaml#L222)

- RTE required-reading is the distinct ART procedure, not a self-alias.
  [`release-train-engineer.agent.md:31`](../../../agents/release-train-engineer.agent.md#L31)

- SM required-reading is the distinct Scrum procedure, not a self-alias.
  [`scrum-master.agent.md:29`](../../../agents/scrum-master.agent.md#L29)

- VMO required-reading is the distinct LPM procedure, not a self-alias.
  [`value-management-officer.agent.md:32`](../../../agents/value-management-officer.agent.md#L32)

**Plugin + ACL**

- Plugin skills are 1:1 with `skills/*.skill.md`; version stays `0.1.0`.
  [`plugin.json:4`](../../../builds/github-copilot/plugin.json#L4)

- Writes only; `workspace-reader` still grants nothing.
  [`access-control-list.conf.yaml:346`](../../../conf/access-control-list.conf.yaml#L346)

- PM skill is Feature-author only; GitHub Project sync is a DO-NOT-USE.
  [`product-manager.skill.md:4`](../../../skills/product-manager.skill.md#L4)

**Tests + Makefile**

- Coherence suite asserts slug resolve, ceremony pairs, plugin 1:1.
  [`test_coherence.py:29`](../../../tests/unit/test_coherence.py#L29)

- Coverage gate is organization Python (`loaders` + `render_bundle`).
  [`Makefile:14`](../../../Makefile#L14)

- CI verify clones harness into `.harness` and runs the same target.
  [`ci.yml:103`](../../../.github/workflows/ci.yml#L103)

- Ceremony set and load contract are documented for operators.
  [`README.md:117`](../../../README.md#L117)
