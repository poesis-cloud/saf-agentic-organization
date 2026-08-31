---
description: 'the challenger records findings into the open-item ledger only (kind: challenge, routed to the owning author); it does not rewrite owner content'
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


# Invariant: challenger_writes_no_owner_content

the challenger records findings into the open-item ledger only (kind: challenge, routed to the owning author); it does not rewrite owner content.

Review the mains that were actually written or thickened on this run. An explicit-none / no-change sibling is not a main to challenge. Never Evaluate this packet.

When the main is a Feature, Feature-enabler, Story, or Story-enabler: check `## NFR applicability / trace` against `products/<product-slug>/nfr-list.md`. Flag omitted applicable NFRs, invented NFRs, or a missing product register (runway handoff). Do not rewrite the register or the owner's work item.
