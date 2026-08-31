---
description: 'owner-rewrite precedence: only @product-manager re-synthesizes a business Feature from the routed challenge findings'
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


# Invariant: only_owner_writes_business_feature

owner-rewrite precedence: only @product-manager re-synthesizes a business Feature from the routed challenge findings.

Keep `## NFR applicability / trace` aligned with `products/<product-slug>/nfr-list.md`. Absorb architecture/security findings that say a listed NFR does not apply, or that an applicable NFR was omitted. Do not author or thicken the product NFR register here.

Surgical Demand: rewrite only if the Feature itself was in-scope and challenged. If this run's in-scope mains were only the Enabler Feature, emit explicit no-change on the business Feature rather than a second rewrite. Do not absorb ADR or NFR-register findings here.
