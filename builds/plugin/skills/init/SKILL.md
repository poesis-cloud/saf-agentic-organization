---
name: init
description: 'Initialise the current Git repository as a SAF workspace of the poesis-saf-agentic-organization framework: checks Git and the Git identity, writes the committed workspace marker .saf/workspace.yaml and the repository plugin settings .github/copilot/settings.json, then commits both. Use when an orchestrator reports that this folder is not a SAF workspace, or when the user asks to initialise, set up or bootstrap a SAF workspace.'
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

# Initialise a SAF workspace

A folder is a **SAF workspace** when its Git top-level holds `.saf/workspace.yaml`, committed
in `HEAD`. The SAF harness governs only such a folder. This skill makes the current repository
one, for the framework `{{PLUGIN_NAME}}`. Run the steps in order and stop at the first refusal,
telling the user exactly what to do. Never write anything outside the Git top-level.

## 1. Check Git

1. Run `git --version`. Git 2.38 or later is required; if it is missing or older, stop and
   say so.
2. Run `git rev-parse --show-toplevel` in the current folder. If it fails, this folder is not
   a Git repository: ask the user whether to run `git init` here. Run it only on a yes;
   otherwise stop. Every later path is relative to the top-level this command prints.
3. Run `git config user.name` and `git config user.email`. If either is empty, stop and tell
   the user to set them (`git config --global user.name "<name>"` and
   `git config --global user.email "<email>"`). Never set the identity yourself.

## 2. Check the marker

Run `git show HEAD:.saf/workspace.yaml` (it fails in a repository with no commit yet, which is
fine).

- It names `framework: {{PLUGIN_NAME}}`: the workspace is already initialised. Say so and
  stop.
- It names another framework: stop. A workspace belongs to one framework; do not overwrite it.

## 3. Write the marker

**Steps 3 to 5 run in ONE shell command.** The harness denies every tool call, shell commands included, while `.saf/workspace.yaml` exists but is not committed in `HEAD`, so writing the marker with a file tool and committing it in a later call is denied. Prepare the contents, then write both files and commit them inside a single shell invocation (e.g. a single PowerShell or `sh` script), with the marker written last before `git add`. If that command fails after writing the marker, remove the marker (`.saf/workspace.yaml`) in the same command so the folder is not left half-initialised.

Write `.saf/workspace.yaml` at the top-level, exactly (the harness marker schema allows these
two properties and no other):

```yaml
framework: {{PLUGIN_NAME}}
root: {{WORKSPACE_ROOT}}
```

## 4. Write the repository plugin settings

Choose the channel: run `copilot plugin list --json` and find the `{{PLUGIN_NAME}}` row. If
its `marketplace` is `poesis-saf-preview`, use the **preview** channel; otherwise (or if the
command is unavailable) use the **stable** channel.

| Channel | Marketplace name | `source` |
| --- | --- | --- |
| stable | `poesis-saf` | `{"source": "github", "repo": "poesis-cloud/saf-marketplace"}` |
| preview | `poesis-saf-preview` | `{"source": "github", "repo": "poesis-cloud/saf-marketplace", "ref": "preview"}` |

Write `.github/copilot/settings.json` at the top-level so that it recommends the marketplace
and enables both SAF plugins from it. For the stable channel:

```json
{
    "extraKnownMarketplaces": {
        "poesis-saf": {
            "source": { "source": "github", "repo": "poesis-cloud/saf-marketplace" }
        }
    },
    "enabledPlugins": {
        "poesis-saf-agentic-harness@poesis-saf": true,
        "{{PLUGIN_NAME}}@poesis-saf": true
    }
}
```

If the file already exists, keep every other key and entry it holds: add or replace only the
marketplace entry under `extraKnownMarketplaces` and the two entries under `enabledPlugins`.

## 5. Commit

Commit the two files, and only them, in the same shell command as steps 3 and 4:

```sh
git add .saf/workspace.yaml .github/copilot/settings.json
git commit -m "Initialise the SAF workspace ({{PLUGIN_NAME}})" -- .saf/workspace.yaml .github/copilot/settings.json
```

If the commit fails (a pre-commit hook, for example), report its output and stop.

## 6. Hand over

Tell the user the workspace is initialised and that the harness reads the marker when a
session opens: they must **start a new session** in this folder and select an orchestrator
again (`{{ORCHESTRATORS}}`).
