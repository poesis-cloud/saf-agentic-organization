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

# Portfolio manifest template — `portfolio/portfolio-manifest.yaml`

The portfolio is the **meta-governance** tier above the ARTs (one ART per product). It is a
singleton, created once. The **Business Owner** and **Enterprise Architect** hats own its content;
`@value-management-officer` is the only writer of the manifest, in `portfolio-sync`.

## Portfolio tree (singleton)

The paths are bound by `conf/workspace.conf.yaml`; the workspace root is
`FRAMEWORK_WORKSPACE_DIR`.

```text
portfolio/
  portfolio-manifest.yaml                      # this manifest
  strategic-themes.md
  portfolio-vision.md
  portfolio-roadmap.md
  budget-allocation.md
  portfolio-kanban.md
  portfolio/portfolio-backlog/<epic-slug>/<epic-slug>.epic.md
  portfolio/products/<product-slug>/product-manifest.yaml
  portfolio/art/<art-slug>/art-manifest.yaml
```

## Manifest — `portfolio/portfolio-manifest.yaml`

The harness validates this manifest by parsing the whole file as JSON (function 9 parses every
non-Markdown artifact as JSON), so write it as JSON — JSON is also valid YAML — with quoted
`"YYYY-MM-DD"` dates and no comments.

```json
{
  "slug": "portfolio-manifest",
  "title": "<Portfolio title>",
  "scope": "portfolio",
  "businessOwner": "central-supervisor",
  "enterpriseArchitect": "central-supervisor",
  "created": "YYYY-MM-DD",
  "products": [
    {
      "slug": "<product-slug>",
      "path": "portfolio/products/<product-slug>"
    }
  ],
  "arts": [
    "<art-slug>"
  ],
  "github_project": null,
  "stepOutcomes": []
}
```

- `products` is the authoritative product registry. Each entry's `path` is the product folder
  `portfolio/products/<product-slug>` of the workspace layout.
- `arts` may be kept as a derived compatibility list. Epics may span any subset of the products via
  their `products` list.
- `github_project` is the Portfolio Project URL, or `null`.
- `stepOutcomes`: every step that commits this file appends one entry
  `{ "step": "<workflow-slug>/<step-slug>", "outcome": "written | revised | confirmed | no-change | none", "date": "YYYY-MM-DD", "note": "<what was decided and why>", "friction": "<optional workflow friction observed>" }`.

## Relationship to products

- The portfolio does **not** own product code or product Features — it owns **Epics**.
- An Epic's child Features stay product-scoped (`parentEpic: E-N` in the Feature frontmatter).
- Cross-product coordination is expressed at the Epic level only; the "no cross-product Feature"
  rule is unchanged (one Feature per product, each linked to the shared Epic).
