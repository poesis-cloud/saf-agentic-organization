---
description: 'the scrum-master writes the Story `cost:` block exactly once at `in-qa → awaiting-pr`, measured net-of-cache from the immutable ecosystem debug logs (matched by `S-N`) — never fabricated, never re-incremented, immutable once committed'
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


# Invariant: story_cost_snapshot_measured_once_from_logs

At the Story's terminal `in-qa → awaiting-pr` transition the **scrum-master** commits the `cost:` block **exactly once**, **measured** net-of-cache (`Σ(inputTokens − cachedTokens) + Σ outputTokens`) directly from this Story's dev + QA dispatch debug logs (matched by `S-N`) — or transparently `estimated` only when those logs are gone. The figure is **never fabricated as if measured**, **never re-incremented per dispatch**, and is **immutable** once `committed` is set. The companion CEL postcondition `story_cost_committed_once` only checks that the block exists; this invariant governs its **provenance + write-once** discipline. The full normative model is inlined below.

---

## Cost-accounting model (full normative model, inlined)

Defines how the SAFe orchestration measures the **development cost, in LLM tokens, of every
Epic / Feature / Story** — so the Central Supervisor can answer two distinct questions:

- **Point-per-point** — "how much did the agentic development of *this* Story / Feature / Epic cost
  on its own?" → the artifact's `cost.tokensSelf`.
- **End-to-end** — "how much did the agentic development of *this whole* Feature / Epic cost,
  children included?" → the artifact's `cost.tokensRolled`.

This is the portfolio-economics analogue of SAFe Lean Budgets: it puts a measurable price on the
agentic delivery of value, captured where the tokens are actually spent (subagent dispatches) and
rolled up the backlog spine **Story → Feature → Epic**.

> Companion of the GitHub sync protocol: same house style, same
> "render/rollup from frontmatter, never invent" discipline. The **ecosystem debug logs are the
> source of truth** (they already record per-request tokens); each `cost:` block is a **once-committed
> snapshot fetched from them** at the artifact's terminal status; kanban cost columns are rendered
> views. No intermediary ledger sits between the logs and the `cost:` block.

### 1. The cost model

#### 1.1 Unit of cost — the dispatch, already isolated at the source

Tokens are spent by **subagent dispatches** (`runSubagent`), never by the orchestrators' own
conducting overhead (out of scope). The ecosystem **already records each dispatch at the source**:
every model round-trip is an `llm_request` event in the Copilot Chat debug logs carrying
`attrs.inputTokens` / `attrs.outputTokens` (and `cachedTokens`), and every subagent dispatch gets its
**own** child log file `runSubagent-<agentName>-<uuid>.jsonl` linked from `main.jsonl`. So the
dispatch is the atomic cost unit **and it is already a discrete record in the source** — there is
nothing to capture by hand.

**A dispatch is itself a multi-turn loop — net out the cache.** One `runSubagent-*.jsonl` is not one
model call: it is the subagent's whole tool-calling loop, often **dozens** of `llm_request` turns, and
**every turn re-sends the growing context**, almost all of it billed back as `cachedTokens` (a re-read,
not new work). Measured on a real `@developer` dispatch: **33 turns**, `Σ inputTokens ≈ 3.99M` of which
`Σ cachedTokens ≈ 3.84M` — so a naive `Σ(in+out) ≈ 4.04M` overstates the dispatch's **net new tokens**
(`≈ 199k`) by **~20×**. Therefore a dispatch's cost is summed **net of cache**:
`Σ(inputTokens − cachedTokens) + Σ outputTokens` (§1.3, §3). That is what makes the number reflect the
work done rather than how many turns the loop happened to take.

#### 1.2 Attribution — recovered from the source, not judged by hand

Each dispatch is charged to the **lowest artifact it directly serves**:

| Dispatch serves… | Charged to | Examples |
|---|---|---|
| One Story's implementation/acceptance | that **Story** (`self`) | dev DRIVE, dev CRITIQUE, `@quality-engineer` acceptance, PO grooming of that Story |
| Feature-level work not tied to one Story | that **Feature** (`self`) | PM refinement (AC/WSJF), `@system-architect` ADR, demo staging, Feature-level docs |
| Epic-level work not tied to one Feature | that **Epic** (`self`) | BO/EA Epic shaping, runway draft, PI Planning, Inspect & Adapt |

Attribution needs **no separate tagging step**: the orchestration convention already **embeds the
served artifact id in the dispatch prompt** (the routing-log prefix + the artifact path the subagent
reads/writes). So the `S-N` / `F-N` / `E-N` is present in the dispatch's `userRequest` /
`inputMessages` in the very same log that carries its tokens — attribution is a **match against the
source**, charged once at exactly one level. Story execution is where the bulk of spend lands;
Feature/Epic `self` capture the program/portfolio **overhead** of getting there.

#### 1.3 Rollup arithmetic

```text
story.tokensSelf    = Σ tokens of dispatches charged to that Story
story.tokensRolled  = story.tokensSelf                      # a Story is a leaf

feature.tokensSelf   = Σ tokens of dispatches charged to that Feature (overhead)
feature.tokensRolled = feature.tokensSelf + Σ child story.tokensRolled

epic.tokensSelf      = Σ tokens of dispatches charged to that Epic (overhead)
epic.tokensRolled    = epic.tokensSelf + Σ child feature.tokensRolled
```

- **Point-per-point** read = any artifact's `tokensSelf` (its own cost) — and `tokensRolled` for
  the subtree it heads.
- **End-to-end** read = the Epic's `tokensRolled` (the full agentic cost of the Epic), or any
  Feature's `tokensRolled`.
- A standalone Feature (`parentEpic: null`) rolls up to itself; it has no Epic parent, so it is its
  own end-to-end root.

Per-dispatch, tokens are summed **net of cache** across the loop's turns:
`tokensIn = Σ(inputTokens − cachedTokens)` (net new prompt tokens, **not** the re-sent cached
context), `tokensOut = Σ outputTokens`, `tokensSelf = tokensIn + tokensOut`. `tokensCached =
Σ cachedTokens` is recorded separately so a billed cost can be reconstructed under any cache price.
`dispatches` counts **subagent runs**, not `llm_request` turns.

**Across** dispatches the sum is intentional and correct: a Story that took two dev cycles + a QA pass
+ one rework loop is charged for **all** of them — rework is real cost, and `dispatches` exposes how
many runs it took. Because the block is **recomputed once from the immutable logs** (§5), not
incremented in place per dispatch, re-runs and double-commits cannot inflate it. The only additivity
that must be corrected is **within** a dispatch (cache, above) — not across them.

### 2. The `cost:` frontmatter block (schema)

Single source of the field definitions. Present on **Epic**, **Feature**, and **Story** frontmatter.

```yaml
cost:                    # token cost accounting — see this instruction
  tokensIn: 0           # self: NET-NEW prompt tokens = Σ(inputTokens − cachedTokens) over all turns of charged dispatches
  tokensOut: 0          # self: completion tokens = Σ outputTokens
  tokensCached: 0       # self: Σ cachedTokens (re-sent context; for billed-cost reconstruction — NOT in tokensSelf)
  tokensSelf: 0         # tokensIn + tokensOut — this artifact's own net cost ("point")
  tokensRolled: 0       # tokensSelf + Σ children.tokensRolled — subtree total ("end-to-end")
  dispatches: 0          # number of SUBAGENT DISPATCHES charged here (not llm_request turns)
  source: estimated      # measured | estimated | mixed (see §4)
  committed: null        # YYYY-MM-DD the one-time snapshot was written (terminal status; immutable after)
```

- For a **Story**, `tokensRolled == tokensSelf` always (leaf).
- `source` is the weakest of the inputs: any estimated child ⇒ parent `source: mixed` (or
  `estimated` if all inputs are estimated).
- The block is **written once**, at the artifact's terminal lifecycle status (§5), as a snapshot
  fetched from the source; `committed` records that date. A terminal artifact's cost is **immutable**
  thereafter — there is no continuous reconciliation.

### 3. The source — the ecosystem debug logs (no intermediary ledger)

There is **no hand-maintained cost ledger**. The numbers are **already logged by the ecosystem**, so
the `cost:` block is fetched **directly from that source** at the appropriate lifecycle status (§5).

**Where the data lives.** The Copilot Chat debug logs (`debug-logs/<sessionId>/`, the same source the
`troubleshoot` skill analyses):

- `main.jsonl` — every `llm_request` event: `attrs.inputTokens`, `attrs.outputTokens`,
  `attrs.cachedTokens`, `attrs.model`, plus the `userRequest` / `inputMessages` that name the served
  artifact id.
- `runSubagent-<agentName>-<uuid>.jsonl` — one file **per dispatch**; sum its `llm_request` token
  attrs to get that dispatch's cost. `main.jsonl` links each via a `child_session_ref`.

**Per-task drill-down is preserved (after-the-fact granularity).** Because every dispatch is its **own**
file — `agentName` in the filename, `tool_call(runSubagent).args` carrying the role/prompt, the artifact
id in that prompt — the source already holds a **per-subagent-task** breakdown: for any artifact you can
recover, per dispatch, *(agent, role, net-of-cache cost, turns, artifact)* without any extra
bookkeeping. The committed `cost:` block is deliberately the **aggregate** (point + end-to-end +
`dispatches` count), **not** the per-task split — the split is recomputed from the source on demand, not
stored in frontmatter. So per-task analysis is available **for as long as the source (or its durable
projection, §8) is retained**; once logs rotate, only the aggregate survives in the artifact unless the
§8 reindex has captured the per-dispatch rows.

**The fetch (conceptual).** To materialise an artifact's `self` cost at its terminal status:

1. Select the dispatch logs whose prompt names the artifact id (`S-N` / `F-N` / `E-N`).
2. Across those dispatches' `llm_request` turns, sum **net of cache**:
   `tokensIn = Σ(inputTokens − cachedTokens)`, `tokensOut = Σ outputTokens`,
   `tokensCached = Σ cachedTokens`; `tokensSelf = tokensIn + tokensOut`; `dispatches` = number of
   dispatch files (not turns). **Never sum raw `inputTokens`** — a loop re-sends its context every
   turn (measured: one 33-turn dispatch summed 3.99M raw input, 3.84M of it cached, ≈199k net), so raw
   summation over-counts ~20×.
3. Add child rollups (§1.3) for a Feature/Epic; write the `cost:` block **once**; `source: measured`.

The durable projection of these logs is the session store (`session_store_sql`, reindexed from the
same debug logs). It does **not yet** expose token columns (§8) — so today the fetch reads the debug
logs directly; when the session store carries tokens, the same fetch becomes a single SQL query. No
intermediary file is introduced in either case.

### 4. Data source & honesty rules (mandatory)

Token figures MUST be either truthfully **measured** from the source or transparently **estimated** —
never fabricated as if measured.

- **`measured`** — summed directly from the dispatch debug logs, **net of cache**
  (`Σ(inputTokens − cachedTokens) + Σ outputTokens`, §3; never raw `Σ inputTokens`). This is the
  **primary path and is available today**; use it whenever the logs for the artifact's dispatches are
  still present.
- **`estimated`** — fallback **only** when the source logs are unavailable (rotated / cleared / a
  different machine) before the terminal-status snapshot is taken. Derive from the heuristic below and
  flag it. Estimates are legitimate; they are simply marked.
- **`mixed`** — a rollup combining measured and estimated inputs.

**Estimation heuristic (deterministic, documented):** `tokens_total ≈ context_in + completion_out`,
where `context_in` ≈ dispatched prompt + named blackboard inputs (≈ 1 token / 4 chars) and
`completion_out` ≈ produced artifact/diff size, floored by a per-tier baseline (`tier-fast` ≥ 2k,
`tier-balanced` ≥ 6k, `tier-high` ≥ 12k total). **Never** invent a precise-looking measured number;
round estimates to the nearest 100.

### 5. When the snapshot is committed (once, at the terminal lifecycle status)

Each `cost:` block is written **exactly once**, when its artifact reaches its terminal `done`-class
status — at which point all of that artifact's dispatches are complete and logged. No per-dispatch
capture, no continuous reconciliation; the block is **immutable** once written (a terminal artifact
does not change).

| Lifecycle moment (commit once) | Owner | One-shot action — fetch from the source (§3) |
|---|---|---|
| Story `in-qa → awaiting-pr` (execution complete) | scrum-master | Fetch this Story's dev + QA dispatch tokens from the session debug logs (matched by `S-N`); write the Story `cost:` block once; `source: measured` (or `estimated` if logs gone) |
| Feature `in-progress → done` (★ Demo Gate) | release-train-engineer | Fetch the Feature's own overhead dispatches (PM / ADR / PI, matched by `F-N`); add Σ child Story `tokensRolled`; write the Feature `cost:` once; refresh the Program kanban cost column |
| Epic `implementing → done` (outcome acceptance) | value-management-officer | Fetch the Epic's own overhead dispatches (BO/EA shaping / PI / I&A, matched by `E-N`); add Σ child Feature `tokensRolled`; write the Epic `cost:` once; refresh the Portfolio kanban cost column |

Child costs are already committed and immutable by the time a parent closes (Stories close before
their Feature's Demo Gate; Features close before their Epic's acceptance), so each parent rollup reads
**committed child snapshots + a one-shot fetch of its own overhead** — never a recomputation of the
children.

> **Harness enforcement.** Each row above is bound, on the owning step of its orchestration, as a
> `content` **invariant** (`story_cost_snapshot_measured_once_from_logs` ·
> `feature_cost_snapshot_measured_once_from_logs` · `epic_cost_snapshot_measured_once_from_logs`) — the
> non-CEL residue (measured-from-logs / never-fabricated / written-once / immutable) that the companion
> `has(unit.cost)` postcondition cannot see. This model stays the rationale source those bound
> invariants point back to.

### 6. Rendering — kanban cost columns

The rendered kanbans (`kanban/*.md`) MAY annotate each card with its rolled cost, since cost now
lives in frontmatter and the "never invent" render rule is satisfied:

- **Team Kanban** — annotate a Story with its `tokensSelf` (e.g. `S-101 [23.7k tk]`).
- **Program Kanban** — annotate a Feature with its `tokensRolled`, and add a *Cost rollup (tokens)*
  mini-section listing the top-N Features by `tokensRolled`.
- **Portfolio Kanban** — annotate an Epic with its `tokensRolled`, and add a *Cost rollup (tokens)*
  section (per Epic and per Strategic Theme).

Cost annotations render the committed `cost:` block; they appear once the artifact reaches the
terminal status that commits its cost (§5) and do not change afterward.

### 7. Worked example

```text
E-5  cost.self   =  40k          (BO/EA shaping + PI Planning + I&A)
 ├─ F-11 cost.self =  18k         (PM refinement + ADR-3 + demo)
 │   ├─ S-101 cost.self = 23.7k
 │   └─ S-102 cost.self = 31.0k
 └─ F-12 cost.self =  9k          (standalone-style overhead)
     └─ S-110 cost.self = 12.4k

F-11.tokensRolled = 18k + 23.7k + 31.0k          = 72.7k     (end-to-end, Feature F-11)
F-12.tokensRolled =  9k + 12.4k                  = 21.4k
E-5.tokensRolled = 40k + 72.7k + 21.4k          = 134.1k    (end-to-end, Epic E-5)

Point-per-point: S-102 cost 31.0k; F-11 own overhead 18k; E-5 own overhead 40k.
```

> All `cost.self` figures above are **net of cache** (§1.1) — i.e. `Σ(inputTokens − cachedTokens) +
> Σ outputTokens` over each charged dispatch's turns — not raw input sums.

### 8. Known limitation & path to automation

The token data **is logged by the ecosystem** — every `llm_request` in the debug logs carries
`inputTokens` / `outputTokens` / `cachedTokens` (§3), so a **measured**, cache-netted snapshot is
achievable today. Two real limits remain, both about *durability*, not *existence* of the data:

1. **Debug logs are local + ephemeral.** They can be rotated or cleared, and live on the machine that
   ran the dispatch. If they are gone before an artifact reaches its terminal status, that snapshot
   falls back to `source: estimated` (§4).
2. **The durable projection drops tokens.** The session store (`session_store_sql`), reindexed from
   the same debug logs, indexes sessions / turns / files but exposes **no token columns** — so the
   one-shot fetch (§3) cannot yet be a durable SQL query.

This is logged as a standing workflow pain point in the portfolio
`improvement-backlog` (`art/<art-slug>/improvement-backlog/<pain-point-slug>/<pain-point-slug>.pain-point.md`). The improvement (a future
workflow change, not a product Feature):

1. Reindex per-request `inputTokens` / `outputTokens` / `cachedTokens` from the debug logs into the
   session store (`turns.tokensIn` / `turns.tokensOut` / `turns.tokensCached`, or a `usage` table),
   exposed via `session_store_sql`, so the durable query can net cache exactly as §3 does.
2. Keep **per-dispatch identity** on those rows — *(agentName, role, served artifact id)*, e.g. a
   `dispatch_id` column + `session_refs(ref_type='artifact')` — so the durable store answers not just
   per-artifact totals but **per-subagent-task** queries (which agent/role cost what on which artifact),
   surviving log rotation. This also makes the §3 attribution exact rather than a prompt-text scan.
3. The terminal-status snapshot (§5) then becomes a durable one-shot query, `source: measured`,
   independent of debug-log retention, and the per-task drill-down (§3) stays queryable forever. Still
   no intermediary file — the source remains the logs / their durable projection.
