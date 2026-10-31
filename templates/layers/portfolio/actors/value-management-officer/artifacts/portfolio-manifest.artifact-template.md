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

# Portfolio Init Template — `portfolio/`

The portfolio is the **meta-governance** tier above the ARTs (one ART per product). It is a
poesis-wide singleton, created once. The **Business Owner** + **Enterprise Architect** hats
(both you) own it; the RTE renders and maintains it.

## Folder tree (singleton)

```
portfolio/
  portfolio-manifest.yaml          # manifest (this template)
  strategic-themes.md     # strategic-themes.artifact-template.md
  epics/                  # E-N-<slug>.md (epic.artifact-template.md)
  github-sync.yaml        # Portfolio Project sync config (github-sync-config-template)
  .gitkeep in empty dirs
```

## Manifest — `portfolio-manifest.yaml`

```yaml
# portfolio-manifest.yaml
scope: portfolio
name: Poesis Portfolio
businessOwner: central-supervisor       # BO hat (Go/No-Go, value authority)
enterpriseArchitect: central-supervisor # EA hat (cross-product runway, NFR backbone)
created: YYYY-MM-DD

# Canonical global portfolio configuration and product registry.
# `products:` is authoritative; `arts:` may be retained as a derived compatibility list.
products:
  - slug: oip-web
    path: portfolio/oip-web
    topology: submodule
  - slug: sis-code-sourcer
    path: portfolio/sis-code-sourcer
    topology: submodule
  - slug: sis-blackboard-manager
    path: portfolio/sis-blackboard-manager
    topology: submodule
  - slug: sie-definition
    path: portfolio/sie-definition
    topology: submodule

# Epics may span any subset of these via their `products:` list.
arts:
  - oip-web
  - sis-code-sourcer
  - sis-blackboard-manager
  - sie-definition

github_project: null      # filled by `provision portfolio` (Portfolio Project URL)
```

## Init checklist (RTE runs this once)

- [ ] Create `portfolio/` tree with `.gitkeep` in `portfolio-backlog/`.
- [ ] Write `portfolio-manifest.yaml` with `products[]` as the authoritative registry and `arts[]` as the compatibility list where older tooling still expects it.
- [ ] Seed `strategic-themes.md` from `strategy/poesis-strategy.md` + business lines.
- [ ] Generate `github-sync.yaml` (portfolio variant) and `provision` the Portfolio Project.

## Relationship to products

- The portfolio does **not** own product code or product Features — it owns **Epics**.
- An Epic's child Features stay product-scoped (`parentEpic: E-N` in the Feature frontmatter).
- Cross-product coordination is expressed at the Epic level only; the "no cross-product Feature"
  rule is unchanged (one Feature per product, each linked to the shared Epic).
