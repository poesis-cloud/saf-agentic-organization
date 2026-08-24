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

# PI Risks Template — `art/<art-slug>/pi-<pi-slug>/risks.md`

RTE-owned register of program-level risks for the PI. Append-only entries.

```markdown
---
pi: M
product: <product-slug>
updated: YYYY-MM-DD
---

# PI-M Risks — <product>

## Risk register (ROAM)

| ID | Description | Impact | Likelihood | Status | Owner | Notes |
|---|---|---|---|---|---|---|
| R-01 | ... | H/M/L | H/M/L | Resolved / Owned / Accepted / Mitigated | <role> | link to mitigation |

## New entries

### R-01 — <short title>
- Detected: YYYY-MM-DD
- Source: <Feature id / sprint / external>
- Description: ...
- Mitigation plan: ...
- ROAM decision: Resolved | Owned | Accepted | Mitigated
- Decided by: Central Supervisor / RTE
- Decision date: YYYY-MM-DD
```

## Lifecycle

Append a new R-NN block whenever a risk is identified. Update the table only when ROAM status changes. Closed at Inspect & Adapt.
