---
name: portfolio-epic-transition-update-portfolio-kanban
description: 'Epic Transition — Value Management Officer refreshes the Portfolio Kanban from Epic frontmatter after the owner transition.'
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

# Epic Transition — update Portfolio Kanban

The Value Management Officer refreshes the Portfolio Kanban from current Epic and Enabler Epic frontmatter, after their authors recorded the transition.

Inputs: the Epic and Enabler Epic just committed by this run, and Epic frontmatter on the Portfolio Backlog.
Output: the portfolio-kanban artifact, with one new `stepOutcomes` entry (`revised` when a column changed, `no-change` otherwise). Do not rewrite Epics, Themes, Vision or the Lean Business Case.
