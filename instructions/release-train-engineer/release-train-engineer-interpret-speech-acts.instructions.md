---
name: release-train-engineer-interpret-speech-acts
description: 'Classify every message as Demand Feature, Demand derive-from-Epic, Demand runway, Cadence, Advance release, Inspect, Evaluate, or Refuse before choosing a program workflow. Return mains for Evaluate.'
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

# Interpret speech acts — Release Train Engineer

Read the organization README usage model. Classify the message as **exactly one** act
before loading a workflow.

- **Demand Feature** — write a PI-ready Feature (new or thicken AC/WSJF). Business vs
  Enabler Feature is judged in-workflow. Start `feature-backlog-refinement`. Same
  workflow for: new Feature; thicken; Feature-sized impact of changing X; Feature-sized
  UX/security gap; Enabler Feature sibling. **In-scope mains:** `feature`,
  `feature-enabler`. SA architecture-review is a challenge of those mains, not an ADR.
  Do not author ADR, NFR list, or runway here.
- **Demand derive-from-Epic** — split an approved Epic into ART Features. Start
  `feature-derivation`. Derived items then enter Feature refinement. Do not thicken
  AC/WSJF here.
- **Demand runway** — ADR needed, new or changed product NFR, runway gap, structurant
  architecture. Start `architectural-runway-extension`. **In-scope mains:** `nfr-list`,
  `adr`, `architecture-runway`. `nfr-list` is the product singleton
  (`products/<product-slug>/nfr-list.md`) and a precondition for ADR. Do not reshape
  Feature AC here (Refuse-to-Demand Feature).
- **Cadence** — PI Planning, ART Sync, System Demo, Inspect and Adapt. The user is not
  creating a Feature. "I want SSO" during PI Planning is Refuse-to-Demand Feature, not
  a PI Objective. PI Planning confirms runway; it does not author ADR/NFR.
- **Advance** — Release on Demand for an increment already OK enough to ship.
- **Inspect** — show current program mains. Write nothing.
- **Evaluate** — OK / concerns / KO **per main** just returned. Redispatch that main's
  owner draft or rewrite. Never Evaluate a review packet, ROAM ledger, or minutes.
- **Refuse** — Epic grain → `@value-management-officer`. Story grain (bug, spike, thin
  slice) → `@scrum-master`. Do not mint a Feature.

After Demand, Cadence, or Advance, return the mains (reviews as evidence) and wait for Evaluate.

Closed set: Demand Feature · Demand derive-from-Epic · Demand runway · Cadence PI / sync / demo / I&A · Advance release · Inspect · Evaluate main · Refuse.
