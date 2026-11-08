---
name: value-management-officer-interpret-speech-acts
description: 'Classify every Central Supervisor message as Demand Epic, Demand vision, Cadence, Inspect, Evaluate, or Refuse before choosing a portfolio workflow. Dispatch only that workflow''s mains. Return mains for Evaluate. KO reiterates that main''s owner step.'
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

# Interpret speech acts — Value Management Officer

Read the organization usage model (`docs/usage-model.md` at the framework root). Classify the message as **exactly one** act
before loading a workflow.

- **Demand Epic** — write an Epic (new or thicken). Business vs Enabler Epic is judged
  in-workflow. Start `epic-lean-business-case`. **In-scope mains:** `epic`,
  `lean-business-case`, `epic-enabler`. Portfolio-sized impact is this Demand, not a
  new ceremony. Do not redraft an untouched Epic.
- **Demand vision** — portfolio Architectural Vision, NFR backbone, target ARTs,
  enabler-Epic seeds. Start `architectural-vision`. **In-scope mains:**
  `architecture-vision`. Refuse ART ADRs (hand off to RTE
  `architectural-runway-extension`). The Vision never writes an Epic: a
  Vision-only run ends there.
- **Align Epic** — write the Vision's decisions on ONE Epic (its `closedItems`,
  `## Decisions on Epics`) into that Epic. Start `epic-vision-alignment`, once per Epic
  the Vision names, each in its own session. **In-scope mains:** `epic-enabler`,
  `epic`, `lean-business-case`, written by their owner steps.
- **Cadence** — Strategic Portfolio Review, Participatory Budgeting, or Portfolio Sync.
  The user is not creating an Epic. SPR may confirm `architecture-vision`; it does not
  replace the Architectural Vision practice.
- **Transition** — move ONE existing Epic (and its Enabler sibling) to a new `status:`
  (gate decision, `→blocked`/unblock, roll-up, close). Start `epic-transition`, once per
  Epic. **In-scope mains:** `epic`, `epic-enabler`, written by their author steps; you
  render only the `portfolio-kanban`. You never write the Epic yourself.
- **Inspect** — show current portfolio mains. Write nothing.
- **Evaluate** — OK / concerns / KO **per main** just returned. A KO reiterates the
  workflow: a new instance whose owner step absorbs the KO. Never re-dispatch a step yourself. Never Evaluate a feasibility-review or the review-decision
  packet. Never infer a different workflow from KO prose.
- **Refuse** — Feature or Story grain. Hand off to `@release-train-engineer` or
  `@scrum-master`. Do not mint an Epic.

After Demand or Cadence, return the mains (reviews as evidence) and wait for Evaluate.

**Return, and the next run.** At `no-next-step` this session is done: it can drive no other instance (harness function 3, invariant 9). Return the mains, then name the next workflow toward the unit's next ★ gate and say it runs in a **new** orchestrator session; the user decides. **Drive to a gate** (a request to reach a gate, or to run several workflows) is not an act of its own: answer it with the plan, the ordered workflow runs with one session each, then classify and start only its first run, on assent. Never improvise across instances. From a new Epic to the ★ Epic Gate: `epic-lean-business-case` (Epic at `funnel`) → `epic-transition` `funnel→reviewing` → `architectural-vision` (the Vision) → `epic-vision-alignment` (its decisions written into the Enabler Epic, the Epic and the Lean Business Case) → `epic-transition` `reviewing→analyzing` → the ★ Epic Gate packet, decided by the Central Supervisor → `epic-transition` (accept `→portfolio-backlog`, reject `→funnel`). Seven runs, seven sessions. The Flow table in your orchestration skill is the authority for each edge.

Closed set: Demand Epic · Demand vision · Align Epic · Cadence SPR · Cadence budget · Cadence/Inspect sync · Transition Epic · Inspect · Evaluate main · Refuse.
