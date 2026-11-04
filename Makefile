# Organization verification gate.
#
# ONE entry point, reused everywhere:
#   - the agent's fast inner loop runs a single slice (`unit`, `functional`);
#   - CI runs the SAME `make verify` target over the whole tree.
#
# PYTHONPATH points at the sibling harness src (do not vendor it) plus the
# host renderer so tests can import ConfigLoader / Application / render_bundle.
#
# Host bundles (rendered outside the source; see README "Installing"):
#   make bundle      BUNDLE_DIR=...      VS Code Copilot Chat
#   make bundle-cli  CLI_BUNDLE_DIR=...  GitHub Copilot app / Copilot CLI

PYTEST := PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -p no:cacheprovider
SAF_HARNESS_SRC ?= ../saf-agentic-harness/src
export SAF_HARNESS_SRC
PYTHONPATH := $(SAF_HARNESS_SRC):$(CURDIR)/builds/github-copilot
COVERAGE := --cov=tests.loaders --cov=render_bundle --cov=builds/github-copilot-cli --cov-fail-under=95

BUNDLE_DIR ?= ../saf-agentic-organization-bundle/github-copilot
CLI_BUNDLE_DIR ?= ../saf-agentic-organization-bundle/github-copilot-cli

.PHONY: verify test unit functional bundle bundle-cli

## verify: unit + functional planes, coverage ≥95% on organization Python.
verify:
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) tests -q $(COVERAGE)

## unit: coherence + renderer only.
unit:
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) tests/unit -q $(COVERAGE)

## functional: live ConfigLoader + harness commands against this tree.
functional:
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) tests/functional -q

## test: alias for the gate.
test: verify

## bundle: render the VS Code Copilot Chat bundle into BUNDLE_DIR.
bundle:
	python3 builds/github-copilot/render_bundle.py . $(BUNDLE_DIR)

## bundle-cli: render the GitHub Copilot app / Copilot CLI plugin into CLI_BUNDLE_DIR.
bundle-cli:
	python3 builds/github-copilot-cli/render_bundle.py . $(CLI_BUNDLE_DIR)
