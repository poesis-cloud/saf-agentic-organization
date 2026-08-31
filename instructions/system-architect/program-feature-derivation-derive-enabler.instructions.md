---
name: program-feature-derivation-derive-enabler
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

# Feature Derivation — derive Enabler Feature

The System Architect derives the sibling Enabler Feature from the approved Epic after the business Feature exists.

Inputs: the approved Epic, the just-derived business Feature, Architectural Vision.
Output: `feature-enabler` naming the consuming Feature. This step **mints identity**, not NFR applicability. Leave `## NFR applicability / trace` empty or "deferred to feature-backlog-refinement". If no Enabler is required, emit explicit-none rather than inventing one.

Do not author an ADR or NFR list here.
