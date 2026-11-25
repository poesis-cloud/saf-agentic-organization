# Organization verification gate.
#
# ONE entry point, reused everywhere:
#   - the agent's fast inner loop runs a single slice (`unit`, `functional`);
#   - CI runs the SAME `make verify` target over the whole tree.
#
# PYTHONPATH points at the sibling harness src (do not vendor it) plus the
# plugin renderer so tests can import ConfigLoader / Application / render_plugin.
#
# The GitHub Copilot plugin (Agent Plugins 1.0) and the Claude Code plugin are rendered
# outside the source:
#   make plugin PLUGIN_DIR=...
#   make plugin-claude CLAUDE_PLUGIN_DIR=...

PYTEST := PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -p no:cacheprovider
SAF_HARNESS_SRC ?= ../saf-agentic-harness/src
export SAF_HARNESS_SRC
PYTHONPATH := $(SAF_HARNESS_SRC):$(CURDIR)/builds/plugin:$(CURDIR)/builds/claude-plugin
COVERAGE := --cov=tests.loaders --cov=builds/plugin --cov=builds/claude-plugin --cov-fail-under=95

PLUGIN_DIR ?= ../saf-agentic-organization-plugin
CLAUDE_PLUGIN_DIR ?= ../saf-agentic-organization-claude-plugin

.PHONY: verify test unit functional plugin plugin-claude generate

## verify: unit plane with coverage ≥95% on organization Python, then the functional plane
## (every workflow run through the harness; untraced, which halves its run time).
verify:
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) tests/unit -q $(COVERAGE)
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) tests/functional -q

## unit: coherence + renderer only.
unit:
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) tests/unit -q $(COVERAGE)

## functional: live ConfigLoader + harness commands against this tree.
functional:
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) tests/functional -q

## test: alias for the gate.
test: verify

## plugin: render the GitHub Copilot plugin into PLUGIN_DIR.
plugin:
	python3 builds/plugin/render_plugin.py . "$(PLUGIN_DIR)"

## plugin-claude: render the Claude Code plugin into CLAUDE_PLUGIN_DIR.
plugin-claude:
	python3 builds/claude-plugin/render_claude_plugin.py . "$(CLAUDE_PLUGIN_DIR)"

## generate: rewrite the structured files (schemas, templates, workflows, briefs, catalogs,
## access control list, workspace layout, tools map, docs/catalog.md) from builds/model.
generate:
	python3 builds/model/generate.py .
