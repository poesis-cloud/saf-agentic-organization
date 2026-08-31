---
description: 'owner-rewrite precedence: only @system-architect re-synthesizes an enabler Feature from the routed challenge findings'
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


# Invariant: only_owner_writes_enabler_feature

owner-rewrite precedence: only @system-architect re-synthesizes an enabler Feature from the routed challenge findings.

Keep `## NFR applicability / trace` aligned with `products/<product-slug>/nfr-list.md`. Do not author the product NFR register here.

Surgical Demand: rewrite only if the Enabler Feature was in-scope and challenged. If this run emitted explicit-none for the Enabler, emit explicit no-change rather than inventing one at rewrite.
