---
name: program-release-on-demand-confirm-deployment
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

# Release on Demand — confirm deployment

The Operator records Continuous Deployment readiness for this release subject.

Inputs: the System Demo increment, pipeline / Helm / environment surface, rollback path.
Output: the operability-review for `art/<art-slug>/releases/<release-slug>/`. Do not author the business release decision. Do not flip Feature or Story status.
