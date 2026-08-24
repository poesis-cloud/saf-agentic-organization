# Organization verification gate.
#
# ONE entry point, reused everywhere:
#   - the agent's fast inner loop runs a single slice (`unit`, `functional`);
#   - CI runs the SAME `make verify` target over the whole tree.
#
# PYTHONPATH points at the sibling harness src (do not vendor it) plus the
# host renderer so tests can import ConfigLoader / Application / render_bundle.

PYTEST := PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -p no:cacheprovider
SAF_HARNESS_SRC ?= ../saf-agentic-harness/src
export SAF_HARNESS_SRC
PYTHONPATH := $(SAF_HARNESS_SRC):$(CURDIR)/builds/github-copilot
COVERAGE := --cov=tests.loaders --cov=render_bundle --cov-fail-under=95

.PHONY: verify test unit functional

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
