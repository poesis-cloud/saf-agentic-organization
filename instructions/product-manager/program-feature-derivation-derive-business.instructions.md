---
name: program-feature-derivation-derive-business
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

# Feature Derivation — derive business Feature

The Product Manager derives a business Feature from an approved Epic.

Inputs: the approved Epic / Lean Business Case, Strategic Themes, Product Vision / Roadmap.
Output: a Feature that names its parent Epic (`parentEpic`). This step **mints identity**, not NFR applicability. Leave `## NFR applicability / trace` empty or "deferred to feature-backlog-refinement".

Do not run Feature Backlog Refinement challenges here; derived items then enter `feature-backlog-refinement`.

Refuse if the user is thickening AC/WSJF or filling NFR traces on an existing Feature (that is refinement) or asking for an ADR/NFR register change (that is `architectural-runway-extension`).
