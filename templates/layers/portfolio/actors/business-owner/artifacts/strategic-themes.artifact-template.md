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

# Strategic Themes Template — `strategic-themes.md`

Portfolio-scoped singleton. The **Business Owner** hat (you) owns it; it is the top of the
backlog spine (`Strategic Themes → Epic → Feature → Story`). Strategic Themes are the
differentiating business objectives that connect the Poesis portfolio to enterprise strategy —
in systemics terms, the **teleological attractors** (system purpose) the governance loop steers
toward. Sourced from `strategy/poesis-strategy.md` (business model).

```markdown
---
owner: central-supervisor      # Business-Owner hat
updated: YYYY-MM-DD
source: strategy/poesis-strategy.md
---

# Poesis Strategic Themes

## Themes

| Theme id | Name | Description | Business line | Horizon |
|---|---|---|---|---|
| ST-1 | <name> | <one-line strategic objective> | theory \| commercial \| infra | <quarter/year> |

## Per-theme detail

### ST-1 — <name>
- **Objective:** what enterprise outcome this theme advances.
- **Why now:** market timing / regulatory / technical driver.
- **Linked Epics:** E-N, E-N (Epics that advance this theme).
- **Guardrails:** budget/scope guardrails (lightweight — single-supervisor portfolio).
```

## Usage

- Every Epic carries `strategic_theme:` referencing a theme id here.
- The Business Owner reviews themes at Inspect & Adapt; themes change slowly (portfolio horizon),
  unlike Epics (PI horizon) and Features (iteration horizon).
- This is a thin governance artifact, not a budgeting system; Lean Budgets / Value Streams are
  intentionally out of scope for the single-supervisor portfolio.
