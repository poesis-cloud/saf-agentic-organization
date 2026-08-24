---
description: 'the Feature — including its status: — is authored by its owner (@product-manager for business, @system-architect for enabler); @release-train-engineer governs the transition in the program kanban; ADRs, decision inventory, runway/NFR registers stay @system-architect-owned'
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


# Invariant: feature_owner_owns_status_architecture_stays_sa_owned

The Feature — including its `status:` — is authored by its owner (@product-manager for business, @system-architect for enabler). @release-train-engineer governs the status transition in the @release-train-engineer-owned program kanban; it does not write the Feature. ADRs, the architecture decision inventory, and the runway/NFR registers stay @system-architect-owned — the RTE collates only flow-owned outputs.
