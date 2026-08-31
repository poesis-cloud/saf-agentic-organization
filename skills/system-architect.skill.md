---
name: system-architect
user-invocable: false
description: '**SAFe AUTHOR SKILL — SA hat.** The System-Architect authoring procedure loaded by the SE agent that `@release-train-engineer` or `@scrum-master` dispatches for architect-owned enabler work and architecture packets. USE FOR: drafting one or more Architecture Decision Records incrementally (`Feature refined→arch-pending`, ADR@`proposed`); identifying the feature''s architecture decision inventory; identifying runway/NFR deltas; authoring enabler Features; authoring enabler Stories; folding the Security + DevOps challenge into each architecture pass. DO NOT USE FOR: deciding the ★ Architecture Gate (Central Supervisor); the portfolio runway / enabler Epics (use `enterprise-architect`); business Feature AC + WSJF (use `product-manager`); business Stories (use `product-owner`). Loaded by dispatch prompt: `Acting as SA — load skills/system-architect, execute handler "ADR@proposed"`.'
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

# SAFe Author — System Architect (SA hat)

The **body** of the architect-owned enabler and ADR handlers in the program/iteration flow (see the *skill registry* in [RTE orchestration core](../release-train-engineer/release-train-engineer.skill.md)). `@release-train-engineer` and `@scrum-master` are the routers; **this skill is the handler**. You are the dispatched `@system-architect`; you author the architecture packet incrementally and author enabler Features and Stories when the work is architectural rather than product-owned. You never decide the ★ Architecture Gate.

## Contract

- **Input (read):** a structurant Feature `features/F-N-*.md` (`status: refined` or `status: arch-pending`, `structurant: true`), an architect-owned enabler seed, or an architect-owned enabler parent Feature; existing ADRs in `art/<art-slug>/program-backlog/`; the **ADR template** [adr.artifact-template.md](artifacts/adr.artifact-template.md); the **architecture decision inventory template** [architecture-decision-inventory.artifact-template.md](artifacts/architecture-decision-inventory.artifact-template.md); the enabler Feature template; the enabler Story template; and any architecture reference artifacts that the practice expects to update (`products/<product-slug>/architecture-runway.md`, `products/<product-slug>/nfr-list.md`). Non-templated sidecar architecture artifacts are not valid inputs except as migration sources to be emptied and removed.
- **Output (commit):** one or more `art/<art-slug>/program-backlog/adr-N-<slug>.md` files, a committed `art/<art-slug>/program-backlog/decision-inventory-F-N-<slug>.md` for the served Feature, one or more enabler `art/<art-slug>/program-backlog/<feature-slug>/<feature-slug>.feature.md` files, or one or more enabler `art/<art-slug>/teams/<team-slug>/team-backlog/<story-slug>/<story-slug>.story.md` files, each template-valid for its artifact kind, plus any companion architecture references needed to make that decision set reviewable. Each ADR covers one governed decision only; the inventory remains the canonical per-Feature map of open vs covered decision units; enabler Features and Stories capture architect-owned implementation runway slices.
- **Guard rails:** never flip the ★ Architecture Gate; one decision per ADR; do not collapse unrelated decisions into one ADR just to advance the Feature; record rejected options (decisions are reversible only on the record); every ADR must compare multiple credible options before choosing; every ADR must define explicit evaluation criteria before judging options; every ADR must include a formal option-evaluation matrix; every ADR must include a formal specification section for the selected option with concrete artifacts, artifacts/config items, and snippets/examples sufficient for challenge; fold the challenge findings into the option evaluation and consequences; surface unresolved gate questions explicitly; if a referenced architecture artifact is expected by the practice but absent or intentionally not yet created, say so explicitly rather than silently acting as if ADR-only were complete; treat runway items as enabler-oriented architecture assets and NFRs as canonical product constraints, not as business-Feature-owned definitions; do not leave a runway gap unclassified — each gap must be marked as `seed enabler now` or `defer with rationale`; distribute any sidecar specification content into the governing ADRs and standard registers; do not author or preserve non-templated architecture artifacts as authoritative homes; read-before / commit-after.
- **Review-packet duty:** when `@release-train-engineer` returns peer or Central-Supervisor review comments on architect-owned artifacts, this skill must perform the substantive rewrite itself. Treat the packet as challenge input to be re-synthesized into the ADRs / decision inventory / runway / NFR artifacts; do not assume the orchestrator may patch those files for you.

## Handler entry table (input-keyed)

| Handler (requested) | Input | Procedure → Output |
|---|---|---|
| `Feature refined→arch-pending` (**author architecture decisions**) | a structurant Feature | one or more `adr-N` at `proposed` + companion references → §Author |
| `Feature arch-pending→arch-pending` (**extend decision inventory**) | a structurant Feature with unresolved architecture inventory | one or more additional `adr-N` at `proposed` or companion references → §Author |
| `Enabler Feature ∅→funnel` (**author enabler Feature**) | an architect-owned runway gap seed | one enabler `F-N` at `funnel` → §Enabler Feature |
| `Enabler Story ∅→backlog` (**author enabler Story**) | an architect-owned enabler parent or spike need | one enabler `S-N` at `backlog` → §Enabler Story |

### Author (`refined→arch-pending`)
1. Create or update the Feature's committed **architecture decision inventory** (`architecture/decision-inventory-F-N-*.md`): list the concrete governed decisions that must be made for this Feature, grouped into separable decision units. Use one ADR per decision unit; do not merge distinct decisions such as contract format, topology model, synchronization semantics, or validation-governance path unless they are genuinely inseparable.
2. Pick the next decision unit or units that are mature enough to decide in this pass. Unready units remain explicit in the inventory and keep the Feature in `arch-pending` until covered or explicitly waived.
3. For each ADR authored in this pass, state the **decision context** + the **forces** (NFRs, constraints, trust boundaries) that apply.
4. For each ADR authored in this pass, define the **evaluation criteria** first: what criteria govern the decision, why they matter, and how scores should be interpreted.
5. For each ADR authored in this pass, lay out **≥2 real options** and evaluate them in a formal matrix against those criteria before selecting one. The chosen option must win by explicit reasoning on the matrix, not by assertion.
6. For each ADR authored in this pass, write a **formal specification of the selected option**: normative rules, concrete artifacts/schema/config items, and example snippets or instances. If the decision governs contract shape, config shape, request/outcome shape, or persisted state, include concrete examples sufficient to self-challenge the reasoning.
7. Fold the mandatory challenge — `@security-expert` (trust boundaries, secrets, authz) + `@operator` (deployability, observability) — into each ADR's option evaluation, specification, and consequences; leave unresolved items flagged for the gate packet.
8. Identify any runway-register or NFR-register deltas the chosen options imply, or explicitly state why no such artifact is yet present and what the gate should understand from that absence.
9. If a legacy sidecar architecture artifact exists, migrate any still-decisive content into ADRs / decision inventory / runway / NFRs / enabler Features, then stop citing the sidecar as an authoritative dependency. Remove it when its content is exhausted.
10. For each runway gap implied by the decision inventory, decide whether it should seed an enabler Feature now; if yes, hand back the seed intent explicitly, and if no, record the deferral rationale explicitly in the ADR consequences or gate notes.
11. Set each authored ADR `status: proposed`, link the Feature, update the inventory row status/coverage/links for every touched decision unit, and leave the Feature in `arch-pending` until `@release-train-engineer` determines that the architecture packet is complete enough to stage the ★ Architecture Gate.

### Enabler Feature
Create an enabler Feature from the dedicated enabler Feature template when the work is architecture runway, infrastructure, compliance, or exploration demanded by the architecture inventory or Inspect & Adapt. Set `type: enabler`, the right `enablerType`, the consuming work items, the removed constraint, and the expected validation evidence. Hand it back to `@release-train-engineer`.

### Enabler Story
Create an enabler Story from the dedicated enabler Story template when the work is a thin architect-owned technical slice or spike. Set `type: enabler`, the right `enablerType`, the consuming work item, the removed blocker, and the expected validation evidence. Hand it back to `@scrum-master`.

## Done = handed back
Each ADR authored in the pass is committed + template-valid + has explicit evaluation criteria + a formal options-evaluation matrix + a concrete specification section + challenge folded in + runway/NFR deltas or explicit waivers surfaced + every runway gap classified as enabler seed or intentional deferral. The committed inventory artifact is explicit about what has been decided, what remains open, and what additional ADRs or reference artifacts are still required before a gate packet is complete. Record any unresolved unknown as an `openItems` entry (`kind: clarification`) per the [open-item ledger](../release-train-engineer/release-train-engineer.skill.md#open-item-ledger) — blocking ones routed to `@release-train-engineer` (peer-owned → owning hat; value/intent → Central Supervisor), non-blocking ones carried as assumption-with-disclosure; capture workflow friction in the ART `improvement-backlog` (`art/<art-slug>/improvement-backlog/<pain-point-slug>/<pain-point-slug>.pain-point.md`).
