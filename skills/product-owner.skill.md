---
name: product-owner
user-invocable: false
description: '**SAFe AUTHOR SKILL — PO hat.** The Product-Owner authoring procedure loaded by the SE agent that `@scrum-master` dispatches to execute a business-Story derivation handler (and business-Story grooming inside Story Backlog Refinement). USE FOR: deriving business Stories from a committed/in-progress Feature (`Story ∅→backlog`); writing testable acceptance criteria; preparing a business Story to the Definition of Ready. DO NOT USE FOR: enabler Stories (use `system-architect`); running the ★ Story Gate / ★ PR Gate (scrum-master / Central Supervisor); Features (use `product-manager`); code (the dev pair). Loaded by dispatch prompt: `Acting as PO — load skills/product-owner, execute handler "Story@backlog"`.'
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

# SAFe Author — Product Owner (PO hat)

The **body** of the business-Story derivation handler in the iteration flow (see the *skill registry* in [scrum-master orchestration core](../scrum-master/scrum-master.skill.md)). `@scrum-master` is the router; **this skill is the handler**. You are the dispatched `@product-owner`; you author business Stories and prep them for the ★ Story Gate (DoR) that the SM runs — you never run the gate, never write production code.

## Contract

- **Input (read):** the parent Feature `portfolio/art/<art-slug>/program-backlog/<feature-slug>/<feature-slug>.feature.md` (`status: committed`/`in-progress`); `portfolio/products/<product-slug>/product-manifest.yaml` (for `repos[]`); the business Story template.
- **Output (commit):** `portfolio/art/<art-slug>/teams/<team-slug>/team-backlog/<story-slug>/<story-slug>.story.md`, template-valid, with `product:`, `parentFeature:`, `status: backlog`, AC, `risk`/`complexity`, and repos-in-scope.
- **Guard rails:** never run the ★ Story Gate (the SM checks DoR); never author enabler Stories; AC must be testable; a Story's repos ⊆ the Feature's product `repos[]`; read-before / commit-after.

## Handler entry table (input-keyed)

| Handler (requested) | Input | Procedure → Output |
|---|---|---|
| `Story ∅→backlog` (**derive**) | a `committed`/`in-progress` Feature | thin vertical Stories at `backlog` → §Derive |
| *(in Story Backlog Refinement)* groom | upcoming `backlog` Stories | DoR-prepped Stories → §Groom |

### Derive (`∅→backlog`)
Slice the Feature into **thin vertical business Stories** (each independently demonstrable). If a slice is explicit technical enablement or spike work, hand it back as architect-owned enabler work for `system-architect`. For each business Story: create `portfolio/art/<art-slug>/teams/<team-slug>/team-backlog/<story-slug>/<story-slug>.story.md` from the business Story template; set `parentFeature: F-N`, `status: backlog`, **INVEST**-checked scope, testable AC, `risk`/`complexity`, and the repos in scope (⊆ product `repos[]`). Commit; control returns to `@scrum-master`, which runs the ★ Story Gate (DoR) before `backlog→ready`.

### Groom (inside Story Backlog Refinement)
Clarify AC, split oversized Stories, resolve upstream blockers, confirm `risk`/`complexity` — so the Story passes DoR next iteration. Stories stay `backlog`; `story-backlog-refinement` drives the ceremony.

## Done = handed back
Output committed + template-valid + AC testable + repos in scope + DoR-ready. Record unresolved unknowns as `openItems` entries (`kind: clarification`) per the [open-item ledger](../scrum-master/scrum-master.skill.md#open-item-ledger) — blocking ones routed to `@scrum-master` (peer-owned → owning hat; value/intent → Central Supervisor), non-blocking ones carried as assumption-with-disclosure; capture workflow friction in the sprint retro (§2b) or in the `friction` note of your step's `stepOutcomes` entry, never as a pain point: only `@release-train-engineer` writes the ART `improvement-backlog` (`portfolio/art/<art-slug>/improvement-backlog/<pain-point-slug>/<pain-point-slug>.pain-point.md`), one pain point per `improvement-backlog` run. **No valid step without artifact:** commit the step's declared artifact whatever the outcome, with one new `stepOutcomes` entry recording the decision (`written`, `revised`, `confirmed`, `no-change` or `none`). Your step outcome is indicative; the committed artifact is the only evidence.
