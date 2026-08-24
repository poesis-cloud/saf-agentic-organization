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

# Product manifest template — `products/<product-slug>/product-manifest.yaml`

```yaml
# products/<product-slug>/product-manifest.yaml
slug: <slug>                          # kebab-case; matches folder name
name: <Human readable name>
description: <one-line>
business_line: commercial             # theory | commercial | infra
status: active                        # active | paused | sunset | exploration
owner: central-supervisor                       # always 'central-supervisor' in single-user mode
created: YYYY-MM-DD

# Repos attached to this product (workspace-relative paths).
# Only these repos may receive commits from Stories of this product.
repos:
  - <relative/path/to/repo>

# Cross-product relationships (referenced by `dependsOn:` in Feature/Story frontmatter).
upstream: []                          # products this one consumes
downstream: []                        # products that consume this one

# Optional pointers.
project_brief: <path/to/PROJECT_BRIEF.md or null>
github_project: <url or null>
```

## Status lifecycle

`exploration → active → paused → sunset` (one-way after sunset).

## Init checklist (RTE runs this in Product Init step 0)

- [ ] Slug is kebab-case and unique in `portfolio-manifest.yaml > products[]`.
- [ ] All paths in `repos[]` exist in the workspace.
- [ ] `business_line` is one of `theory | commercial | infra`.
- [ ] Entry appended to `portfolio-manifest.yaml > products[].
