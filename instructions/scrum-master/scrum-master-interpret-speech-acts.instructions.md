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
- **Inspect** — show current team mains. Write nothing.
- **Evaluate** — OK / concerns / KO **per main** just returned. Redispatch that main's
  owner draft or rewrite. Never Evaluate a feasibility-review, qa-signoff, or minutes.
  "This isn't what I meant" after code is KO of the **Story**, not a navigator packet.
- **Refuse** — Feature or Epic grain. ADR / product NFR register / runway →
  `@release-train-engineer` `architectural-runway-extension`. Hand off; do not mint a
  Story. Feature→Story splitting is this Demand, not a separate derivation workflow.

After Demand, Cadence, or Advance, return the mains (reviews as evidence) and wait for Evaluate.

Closed set: Demand Story · Cadence plan / sync / review / retro · Advance implement · Advance verify · Inspect · Evaluate main · Refuse.
