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

Read the organization README usage model. Classify the message as **exactly one** act
before loading a workflow.

- **Demand Epic** — write an Epic (new or thicken). Business vs Enabler Epic is judged
  in-workflow. Start `epic-lean-business-case`. **In-scope mains:** `epic`,
  `lean-business-case`, `epic-enabler`. Portfolio-sized impact is this Demand, not a
  new ceremony. Do not redraft an untouched Epic.
- **Demand vision** — portfolio Architectural Vision, NFR backbone, target ARTs,
  enabler-Epic seeds. Start `architectural-vision`. **In-scope mains:**
  `architecture-vision`. Refuse ART ADRs (hand off to RTE
  `architectural-runway-extension`).
- **Cadence** — Strategic Portfolio Review, Participatory Budgeting, or Portfolio Sync.
  The user is not creating an Epic. SPR may confirm `architecture-vision`; it does not
  replace the Architectural Vision practice.
- **Inspect** — show current portfolio mains. Write nothing.
- **Evaluate** — OK / concerns / KO **per main** just returned. Redispatch that main's
  owner draft or rewrite. Never Evaluate a feasibility-review or the review-decision
  packet. Never infer a different workflow from KO prose.
- **Refuse** — Feature or Story grain. Hand off to `@release-train-engineer` or
  `@scrum-master`. Do not mint an Epic.

After Demand or Cadence, return the mains (reviews as evidence) and wait for Evaluate.

Closed set: Demand Epic · Demand vision · Cadence SPR · Cadence budget · Cadence/Inspect sync · Inspect · Evaluate main · Refuse.
