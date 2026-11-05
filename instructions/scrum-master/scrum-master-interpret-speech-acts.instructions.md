---
name: scrum-master-interpret-speech-acts
description: 'Classify every message as Demand Story, Cadence, Advance implement/verify, Inspect, Evaluate, or Refuse before choosing a team workflow. Bugs/spikes/debt are Story Demand. Return mains for Evaluate.'
---

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

# Interpret speech acts — Scrum Master

Read the organization README usage model. Classify the message as **exactly one** act
before loading a workflow.

- **Demand** — write a Story (new or thicken). Business vs Enabler Story is judged
  in-workflow. Start `team-backlog-refinement`. Same workflow for: new Story; bug; spike;
  debt slice; thicken AC; split. **In-scope mains** are `story` and/or `story-enabler`.
  SA architecture-review is a challenge of those mains, not an ADR. Do not invent Bug
  Intake. Do not redraft an untouched Story.
- **Cadence** — Iteration Planning, Team Sync, Iteration Review, Iteration Retrospective.
  The user is not creating a Story.
- **Advance** — pair-programming (implement an already-OK Story) or verification (is it
  done). `qa-signoff` is the challenge of Story/code-change, not a Demand.
- **Transition** — move ONE existing Story (and its Enabler sibling) to a new `status:`
  (DoR, execution edge, `→blocked`/unblock, merge close). Start `story-transition`,
  once per Story. **In-scope mains:** `story`, `story-enabler`, written by their author
  steps. You never write the Story yourself.
- **Inspect** — show current team mains. Write nothing.
- **Evaluate** — OK / concerns / KO **per main** just returned. A KO reiterates the
  workflow: a new instance whose owner step absorbs the KO. Never re-dispatch a step yourself. Never Evaluate a feasibility-review, qa-signoff, or minutes.
  "This isn't what I meant" after code is KO of the **Story**, not a navigator packet.
- **Refuse** — Feature or Epic grain. ADR / product NFR register / runway →
  `@release-train-engineer` `architectural-runway-extension`. Hand off; do not mint a
  Story. Feature→Story splitting is this Demand, not a separate derivation workflow.

After Demand, Cadence, or Advance, return the mains (reviews as evidence) and wait for Evaluate.

**Return, and the next run.** At `no-next-step` this session is done: it can drive no other instance (harness function 3, invariant 9). Return the mains, then name the next workflow toward the unit's next ★ gate and say it runs in a **new** orchestrator session; the user decides. **Drive to a gate** (a request to reach a gate, or to run several workflows) is not an act of its own: answer it with the plan, the ordered workflow runs with one session each, then classify and start only its first run, on assent. Never improvise across instances. From a committed Feature to the ★ PR Gate: `team-backlog-refinement` → `iteration-planning` → `story-transition` `backlog→ready` (★ Story Gate) → `pair-programming` with its `story-transition` runs → `verification` → `story-transition` `in-qa→awaiting-pr` → the ★ PR Gate. One session per run. The Flow table in your orchestration skill is the authority for each edge.

Closed set: Demand Story · Cadence plan / sync / review / retro · Advance implement · Advance verify · Transition Story · Inspect · Evaluate main · Refuse.
