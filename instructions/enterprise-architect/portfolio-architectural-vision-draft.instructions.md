---
name: portfolio-architectural-vision-draft
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

# Architectural Vision — draft

The Enterprise Architect authors or thickens the cross-product Architectural Vision and the portfolio NFR backbone.

Inputs: the governing Epic / Lean Business Case (if any), Strategic Themes, Portfolio Vision / Roadmap, existing Architectural Vision.
Output: `architecture-vision`. Record Feature seeds, target ARTs, enabler-Epic seeds or explicit deferrals, and the **NFR backbone** (qualities that later products must make measurable). Do not write a product `nfr-list`.

Record every decision the Vision makes about an existing Epic or Enabler Epic under `## Decisions on Epics`, by Epic `id`: the Feature seeds it places there (MVP or not, with target ART), the size change, and every open item it closes. List each closed item in `closedItems` too (`artifact: epic | epic-enabler`, `unit:` the Epic `id`, `item:` the `openItems` id, `resolution:`). You do not write the Epics: when the Vision decides about one, `epic-vision-alignment` runs next for it, and its owner steps write the decisions. A Vision that decides about no Epic leaves both empty.

Do not author ART-level ADRs or the product NFR register (that is `architectural-runway-extension`). Do not rewrite the Epic hypothesis (that is `epic-lean-business-case`).
