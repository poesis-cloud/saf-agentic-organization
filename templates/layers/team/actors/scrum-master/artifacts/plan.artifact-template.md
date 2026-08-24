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

# Plan Template

## Plan File

Save as `products/<product-slug>/<plan-slug>.plan.md`:

```markdown
---
sprint: N
pi: M
product: <product-slug>
---

# Sprint N — [Name]

> Sprint Goal: [one sentence describing the deliverable]
> PI: M | Branch: feature/sprint-N
> Estimated effort: [time estimate]

## Prioritized Story List

| # | Story | Feature | ADRs | Driver | Navigator | Est | Description |
|---|-------|---------|------|--------|-----------|-----|-------------|
| S-1 | [story] | F-N | [adr ids] | default-dev | default-dev | 1h | [what to build] |
| S-2 | [story] | F-N | [adr ids] | default-dev | @security-expert | 2h | [trust-boundary work] |
| S-3 | [story] | F-N | [adr ids] | @ux-designer | default-dev | 1h | [UX-driven work] |

Pair convention: first-named = initial Driver, second-named = initial Navigator.
Roles swap each pair-programming micro-cycle (see the scrum-master skill § Pair Programming).

## Work Schedule

### Phase 1: [Name] (S-1 .. S-3)
- Dispatch pairs sequentially
- Checkpoint commit after phase

### Phase 2: [Name] (S-4 .. S-6)
- Dispatch pairs sequentially
- Checkpoint commit after phase

### Phase 3: Acceptance & Polish
- RTE runs acceptance against every Story DoD (QA duty)
- File blockers as GitHub Issues
- Open PR for the ★ PR Gate only when no blockers remain

## Success Criteria

- [ ] Every Story meets its DoD
- [ ] Every commit carries pair attribution + Copilot trailer
- [ ] All dependent ADRs are `accepted`
- [ ] CI green
- [ ] Per-Story QA sign-off files exist in `art/<art-slug>/teams/<team-slug>/team-backlog/<story-slug>/<qa-signoff-slug>.qa-signoff.md`

## What's NOT in This Sprint

| Story / Feature | Reason |
|-----------------|--------|
| [deferred item] | [why — scope, ADR pending, dependency] |

## RTE Dispatch Prompt

> @release-train-engineer — Read PROJECT_BRIEF.md and products/<product-slug>/<plan-slug>.plan.md. Execute Sprint N.
>
> First: git pull origin main && git checkout -b feature/sprint-N
>
> For each Story, dispatch the named Driver/Navigator pair as subagents.
> Pairs run the pair-programming micro-cycle and commit on feature/sprint-N.
> Close GitHub Issues in commits: "fix: description (Fixes #NN)".
> Update the Progress section of this same plan.md after each Story.
> When all Stories pass acceptance, push and open a PR.
> Wait for the ★ PR Gate (human approval) before merging.
> Follow Sections 12-14 of PROJECT_BRIEF.md.

## Progress

Updated daily by the SM directly in this same plan.md — there is no separate progress artifact.

### Burn-down
| Day | Stories not-done | Points remaining | Notes |
|---|---|---|---|
| D1 | 6 | 21 | start |
| D2 | 6 | 19 | |

### Story status snapshot
| Story | Status | Pair | Notes |
|---|---|---|---|
| S-101 | in-qa | dev/dev | |
| S-102 | in-progress | dev/SE-Security | |

### Open blockers
(Roll-up from daily stand-up inputs)
| ID | Story | Description | Owner | Age (days) |
|---|---|---|---|---|

### Gate decision backlog
(Roll-up from unresolved gate decisions; unresolved entries must be included in every gate packet)
| ID | Story/Feature | Decision needed | Options | Owner | Status |
|---|---|---|---|---|---|
| GD-001 | S-101 | Approve PR scope variance | accept / rework / defer | Central Supervisor | open |

### Notes / scope changes
Append-only log of mid-sprint clarifications (PO-confirmed).

## Done

Appended at sprint end, in this same plan.md.

### What Was Built
- S-1 — [Story] (pair: default-dev / default-dev)
- S-2 — [Story] (pair: default-dev / @security-expert)

### What's NOT Done
- [Deferred Story — why]

### Files Changed/Created
- `src/components/NewComponent.tsx` — [purpose]
- `api/src/functions/newEndpoint.ts` — [purpose]

### Manual Setup Required
- [Any env vars, config, or manual steps needed]

### Known Issues
- [Issue — tracked as GitHub Issue #NN]

### ADRs Referenced
- ADR-N — [title] (status: accepted)

## QA Sign-off Roll-up

Per-Story QA sign-off is captured in `art/<art-slug>/teams/<team-slug>/team-backlog/<story-slug>/<qa-signoff-slug>.qa-signoff.md`. The sprint-level roll-up is appended here, in this same plan.md:

### Stories Accepted

| Story | DoD met? | Notes |
|-------|----------|-------|
| S-1 | ✅ | |
| S-2 | ✅ | |
| S-3 | ❌ | blocker #NN open |

### Test Results
- Tests run: X
- Tests passed: X
- Tests failed: 0

### Blockers
NONE   (or: list of GitHub Issues with severity:blocker)

### Issues Filed
- #NN — [description] (severity: minor)

### Result
✅ PASS — No blockers. Sprint N ready to open PR for the ★ PR Gate.
   (or: ❌ HOLD — blockers must clear before the ★ PR Gate)
```

## Lifecycle

Created at Iteration Planning; updated by SM at every Daily Sync (Progress section) and at Iteration Review (Done + QA Sign-off Roll-up sections). One file per iteration — there is no separate progress artifact/file.
