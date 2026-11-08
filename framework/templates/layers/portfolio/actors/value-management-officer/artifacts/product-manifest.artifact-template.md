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

# Product manifest template — `portfolio/products/<product-slug>/product-manifest.yaml`

The harness validates this manifest by parsing the whole file as JSON (function 9 parses every
non-Markdown artifact as JSON), so write it as JSON — JSON is also valid YAML — with quoted
`"YYYY-MM-DD"` dates and no comments.

```json
{
  "slug": "<product-slug>",
  "title": "<Human readable name>",
  "description": "<one-line>",
  "business_line": "commercial",
  "status": "active",
  "owner": "central-supervisor",
  "created": "YYYY-MM-DD",
  "repos": [
    "<relative/path/to/repo>"
  ],
  "upstream": [],
  "downstream": [],
  "project_brief": null,
  "github_project": null,
  "stepOutcomes": []
}
```

- `slug` is kebab-case and equals the `<product-slug>` folder name.
- `business_line`: `theory | commercial | infra`. `status`: `active | paused | sunset | exploration`.
- `owner` is always `central-supervisor` in single-user mode.
- `repos` lists the repos attached to this product (workspace-relative paths). Only these repos may
  receive commits from Stories of this product.
- `upstream` / `downstream` list the products this one consumes / that consume this one (referenced
  by `dependsOn` in Feature/Story frontmatter).
- `project_brief` (path to `PROJECT_BRIEF.md`) and `github_project` (URL) are optional, or `null`.
- `stepOutcomes`: every step that commits this file appends one entry
  `{ "step": "<workflow-slug>/<step-slug>", "outcome": "written | revised | confirmed | no-change | none", "date": "YYYY-MM-DD", "note": "<what was decided and why>", "friction": "<optional workflow friction observed>" }`.

## Status lifecycle

`exploration → active → paused → sunset` (one-way after sunset).

## Checklist (`portfolio-sync` `update-product-manifest`)

- [ ] Slug is kebab-case and unique in `portfolio/portfolio-manifest.yaml` `products`.
- [ ] All paths in `repos` exist in the workspace.
- [ ] `business_line` is one of `theory | commercial | infra`.
- [ ] The product is listed in `portfolio/portfolio-manifest.yaml` `products`.
