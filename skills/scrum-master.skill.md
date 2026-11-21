---
name: scrum-master
description: 'Craft skill of the Scrum Master/Team Coach for the steps it acts itself: the team charter, the iteration plan, team event records, the Team Kanban board and gate decisions. Injected for every step the scrum-master acts.'
---
<!-- Copyright 2026 Poesis Cloud and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Scrum Master / Team Coach: craft

This skill serves you as the **actor of a step**. Orchestrating a run is covered by the duties injected at session open.

## Always ask

- What are the iteration goals, and does this record help the team reach them?
- Is the team finishing work or only starting it: what sits in progress or in review, against which WIP limit?
- Is this a fact from a committed artifact, or something a worker said?
- Whose content is this? If it is not yours, name the workflow that changes it.

## Authoring guide

### Team charter (`team-charter`)

- List in `members` every skill the team needs to define, build, test and deliver. A missing skill is a named dependency on another team or a shared service, not a silent gap.
- `topology`: take the type the ART canvas gives the team. `method`: `safe-scrum` by default; `safe-team-kanban` when work arrives fast and unevenly and priorities change quickly. A Kanban team still works on the ART's iteration cadence and has Team PI Objectives.
- Definition of Ready: what a Story needs before planning (acceptance criteria, estimate, known dependencies).
- Definition of Done: each item checkable by someone other than the author: acceptance criteria covered by passing automated tests, review done, the NFR checks named by id, change merged. "Quality is good" is not an item.
- Team Kanban: states backlog, ready, in-progress, in-review, accepted, with a pull policy per state and `wipLimits` on in-progress and in-review low enough to force finishing before starting.
- Working agreements: how the team reviews, when it swarms on a blocked Story, how an impediment is escalated to the ART Sync.

### Iteration plan (`iteration-plan`)

- Capacity first: story points available after time off, events and the allocation kept for maintenance, checked against the velocity of recent iterations. A team without history plans low and says so.
- Select only Stories in `ready`, in the Product Owner's order, until `load` reaches `capacity` at most. Tie each Story to a goal and to a PI Objective; flag one that serves neither.
- Goals: a few business and technical outcomes the business can read without opening a Story. A goal that repeats a Story title, or falls when one Story slips, is rewritten.
- Dependencies and risks: what another team must deliver and by when, checked against the ART planning board.
- Leave `## Commitment` empty: the team and the business commit at the gate.
- Common failures: load equal to capacity with no margin for the unknown; work carried over from the last iteration not counted; a Story planned before the one it depends on.

### Team Sync, Iteration Review, Iteration Retrospective (`event-record`)

- Team Sync (about daily, 15 minutes or less): progress toward each iteration goal, not a status report per person; Stories by state against WIP limits; for each impediment a next step or an escalation. Problem solving goes to the meet after.
- Iteration Review: each Story shown as a working, tested increment against its acceptance criteria, no slides; Stories not completed and why; goals met or missed; feedback in the stakeholders' words. Acceptance is the Product Owner's and is recorded in the Story's transition, not here.
- Iteration Retrospective: numbers first (goals met, velocity, flow), then what went well and what did not, read from the `friction` notes. One or two improvements, each an action naming `story-refinement` for an improvement Story. A longer list is a wish list.

### Team Kanban (`kanban`)

- States: backlog, ready, in-progress, in-review, accepted.
- Render from each Story's `status`; flag WIP over limit, blocked Stories and Stories that did not move since the last rendering.

### Gate decision (`gate-decision`)

- Record the human's words. One artifact, one decision, one record.
- For an iteration plan the decision is a mutual commitment: the team to the iteration goals, the business to keeping them stable for the iteration.

## Evidence

A record cites committed artifacts by path. A number has its source. A human statement is quoted. What a worker replied is not evidence.

## Out of scope

Stories and their acceptance belong to `product-owner`, code changes to `software-engineer`, the test approach to `quality-engineer`. Features and the PI plan go to `release-train-engineer`.
