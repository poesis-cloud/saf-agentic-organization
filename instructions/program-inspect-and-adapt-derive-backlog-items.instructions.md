---
description: 'Inspect & Adapt backlog-creation steps — read pain points with product-improvement resolution and create the artifacts owned by this actor.'
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


# Inspect & Adapt — Derived Backlog Item Creation

Read all `art/<art-slug>/improvement-backlog/<pain-point-slug>/<pain-point-slug>.pain-point.md` artifacts with `resolution: product-improvement` that are assigned to your actor. For each one, create the corresponding artifact using your standard template and skill.

## Actor → artifact mapping

| Actor | Item type | Artifact path |
|---|---|---|
| `@product-manager` | `feature` | `art/<art-slug>/program-backlog/<feature-slug>/<feature-slug>.feature.md` |
| `@system-architect` | `feature-enabler` | `art/<art-slug>/program-backlog/<feature-slug>/<feature-slug>.feature-enabler.md` |
| `@system-architect` | `story-enabler` | `art/<art-slug>/teams/<team-slug>/team-backlog/<story-slug>/<story-slug>.story-enabler.md` |
| `@product-owner` | `story` | `art/<art-slug>/teams/<team-slug>/team-backlog/<story-slug>/<story-slug>.story.md` |

Use the ART (and team, for team-level items) identified in the pain point or by the facilitating `@release-train-engineer`.

## Required back-links

- Link the new artifact to the source pain point (`art/<art-slug>/improvement-backlog/<pain-point-slug>/<pain-point-slug>.pain-point.md`).
- Update the pain point's `derivedFeatures` or `derivedStories` list with the new artifact id.

Do not change the pain point's `status` — that is owned by `@release-train-engineer`.
