---
name: program-pi-planning-confirm-feature-intent
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

# PI Planning — confirm Feature intent

The Product Manager confirms the intent of the **one** Feature this PI Planning run commits (PI Planning runs per Feature reaching `ready`). Update that Feature artifact only: another Feature is another PI Planning run. Do not emit feasibility/security/UX review packets; those concerns belong on the Feature or as Enabler Features.

When the review changes nothing, still commit the artifact with only a new `stepOutcomes` entry (`outcome: confirmed`, note what was checked): the committed entry, not the reply, is the confirmation.
