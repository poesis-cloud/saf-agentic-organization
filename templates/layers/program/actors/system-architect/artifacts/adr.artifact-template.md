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

# ADR Template — `art/<art-slug>/program-backlog/<feature-slug>/<adr-slug>.adr.md`

Authored by `@system-architect` for any Feature flagged `structurant: true`.

```markdown
---
id: ADR-1
title: <short decision title>
status: proposed              # proposed | accepted | rejected | superseded
product: <product-slug>
parentFeature: F-12
decision_scope: <single governed decision unit>
deciders:
  - central-supervisor                  # ★ Architecture Gate decider
  - SE-Architect
consulted:
  - SE-Security
  - SE-DevOps-CI
created: YYYY-MM-DD
decided: null                 # set on ★ Architecture Gate accept/reject
supersedes: null              # ADR id, if applicable
superseded_by: null
related_adrs: []              # sibling, cross-product, or predecessor/successor
                              # ADR ids
dependsOn: []                # prerequisite ADR ids that must be understood
                              # first
---

# ADR-1 — <title>

## Context
Forces at play. What is structurant about the parent Feature.

## Decision scope
Name the one decision unit this ADR governs and why it is separable from
neighboring decisions.

## Linked enablers and served artifacts
- Enabler follow-up: <F-N ...>
- Served artifacts/specifications: <artifact ids, schema ids, config items, refs>
- Companion references absorbed here: <what from other standard artifacts (decision inventory / runway / NFR context) is made concrete in this ADR>

## Option evaluation criteria

Define the criteria that govern this decision before evaluating options.

| Criterion | Why it matters for this decision | Weight | How to read the score |
| --- | --- | --- | --- |
| <criterion-1> | <reason> | H/M/L or 1-5 | <higher/lower is better> |
| <criterion-2> | <reason> | H/M/L or 1-5 | <higher/lower is better> |

## Options evaluation

List only credible options.

| Option | <criterion-1> | <criterion-2> | ... | Summary assessment |
| --- | --- | --- | --- | --- |
| Option A | <score + short rationale> | <score + short rationale> | ... | <net read> |
| Option B | <score + short rationale> | <score + short rationale> | ... | <net read> |
| Option C | <score + short rationale> | <score + short rationale> | ... | <net read> |

After the matrix, explain the decision logic explicitly:

1. **<Option A>** — strengths / weaknesses under the chosen criteria.
2. **<Option B>** — strengths / weaknesses under the chosen criteria.
3. **<Option C — chosen>** — strengths / weaknesses under the chosen criteria.

## Decision
State the selected option in active voice and explain why it wins under the defined criteria.

## Formal specification of the selected option

Make the chosen option concrete enough to challenge and implement.

### Normative rules
- <rule 1>
- <rule 2>

### Concrete artifacts / schemas / snippets
- Artifact: `<artifact-name>` — purpose and authoritative owner.
- Schema/config item: `<schema-or-config-id>` — required fields and validation rule.

~~~yaml
# Example snippet or minimal concrete instance
<example>
~~~

If the decision governs request/response or persisted state, include at least one full example.
If the decision governs configuration, include the normative artifact location and required fields.
If the decision governs an interface, request/outcome contract, persisted artifact bundle, or
configuration surface, distribute the relevant specification into this ADR rather than leaving it
in a separate sidecar document.

## Consequences

- Positive: ...
- Negative: ...
- Follow-up Features or ADRs to file.

## Implementation hooks

Repos and code areas impacted (must intersect parent product's `repos[]`).
```

## Status lifecycle

`proposed → ★ Architecture Gate → accepted | rejected`. `accepted` may later flip to `superseded` by a newer ADR.

Architecture Gate transition: parent Feature flips `arch-pending → ready` on `accepted`, or back to `refined` on `rejected`.
