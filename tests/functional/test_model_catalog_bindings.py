"""Every catalog model is one each harness host adapter can dispatch.

`resolve-step-model` ranks every profile in `conf/model-profiles.conf.yaml` and returns the
winner. A host that does not offer the winner does not refuse it: the GitHub Copilot app /
Copilot CLI silently runs another model with the named model's tool set. So the catalog may
only hold slugs that every adapter in the harness checkout binds in its `models.yaml`.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from tests.conftest import HARNESS_SRC, ORG_ROOT

ADAPTER_MODELS = sorted((HARNESS_SRC.parent / "adapters").glob("*/models.yaml"))


def _catalog() -> set[str]:
    data = yaml.safe_load((ORG_ROOT / "conf" / "model-profiles.conf.yaml").read_text(encoding="utf-8"))
    return {profile["slug"] for profile in data["modelProfiles"]}


def test_the_harness_checkout_ships_host_model_bindings() -> None:
    assert ADAPTER_MODELS, f"no adapters/*/models.yaml under {HARNESS_SRC.parent}"


@pytest.mark.parametrize("models", ADAPTER_MODELS, ids=lambda path: path.parent.name)
def test_every_catalog_model_is_bound_by_the_host_adapter(models: Path) -> None:
    bindings = yaml.safe_load(models.read_text(encoding="utf-8"))["modelBindings"]
    assert sorted(_catalog() - set(bindings)) == []
