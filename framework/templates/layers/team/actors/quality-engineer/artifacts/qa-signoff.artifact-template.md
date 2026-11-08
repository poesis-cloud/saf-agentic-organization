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

# QA Sign-off Template — `portfolio/art/<art-slug>/teams/<team-slug>/team-backlog/<story-slug>/<story-slug>.qa-signoff.md`

Authored by `@quality-engineer` (Ivy). Mandatory artifact for any Story transition `in-qa → awaiting-pr`.

```markdown
---
slug: <story-slug>-qa-signoff
story: S-1
product: <product-slug>
sprint: N
qa_engineer: '@quality-engineer'
verdict: pass                 # pass | fail
date: "YYYY-MM-DD"
test_artifacts:
  - <relative/path/to/test-run-log>
coverage:
  instruction_pct: 0          # JaCoCo or equivalent, where applicable
  line_pct: 0
stepOutcomes: []          # every step that commits this file appends one entry: { step: <workflow-slug>/<step-slug>, outcome: written | revised | confirmed | no-change | none, date: "YYYY-MM-DD", note: <what was decided and why>, friction: <optional workflow friction observed> }
---

# QA Sign-off — S-1

## Story under test
Link / id. Restate the AC verified.

## DoD verification
- [ ] Code merged to feature branch
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Coverage threshold met (>=95% where applicable)
- [ ] AC verified end-to-end
- [ ] PO confirmation recorded below
- [ ] No security regressions (if security-touching)
- [ ] Accessibility verified (if UI-touching)
- [ ] Docs updated (if applicable)

## PO confirmation
- Confirmed by: `@product-owner`
- Date: "YYYY-MM-DD"
- Notes: ...

## Verdict
**PASS** — Story is ready for the ★ PR Gate.
*(or)*
**FAIL** — bugs filed below; Story returns to `in-progress`.

## Bugs filed (if FAIL)
| Bug id | Severity | Title | GitHub issue |
|---|---|---|---|
| B-01 | High | ... | #NNN |
```

## Lifecycle

One sign-off file per Story. If FAIL, the next QA pass updates the same file and appends its own `stepOutcomes` entry.
