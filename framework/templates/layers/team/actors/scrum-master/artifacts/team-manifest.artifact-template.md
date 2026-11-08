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

# Team manifest template — `portfolio/art/<art-slug>/teams/<team-slug>/team-manifest.yaml`

The harness validates this manifest by parsing the whole file as JSON (function 9 parses every
non-Markdown artifact as JSON), so write it as JSON — JSON is also valid YAML — with quoted
`"YYYY-MM-DD"` dates and no comments.

```json
{
  "slug": "<team-slug>",
  "title": "<Team title>",
  "description": "<Short description of the team>",
  "stepOutcomes": []
}
```

`stepOutcomes`: every step that commits this file appends one entry
`{ "step": "<workflow-slug>/<step-slug>", "outcome": "written | revised | confirmed | no-change | none", "date": "YYYY-MM-DD", "note": "<what was decided and why>", "friction": "<optional workflow friction observed>" }`.
