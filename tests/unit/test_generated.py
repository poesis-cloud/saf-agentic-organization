"""The structured files of the organization are exactly what `builds/model` generates.

The model in `builds/model/` is the source of the artifact schemas, templates, workflows, briefs,
catalogs, access control list, workspace layout, tools map and `docs/catalog.md`. Change the
model and run `make generate`; a hand edit of a generated file, or a model change that was not
regenerated, fails here.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from tests.loaders import LAYERS, organization_root

ORG = organization_root()
GENERATED_FOLDERS = ("artifacts", "templates", "workflows", *(f"instructions/{layer}" for layer in LAYERS))
GENERATED_FILES = ("conf/workspace.conf.yaml", "conf/access-control-list.conf.yaml", "builds/plugin/tools.yaml", "docs/catalog.md")


@pytest.fixture(scope="module")
def generated(tmp_path_factory: pytest.TempPathFactory) -> Path:
    root = tmp_path_factory.mktemp("generated")
    subprocess.run([sys.executable, str(ORG / "builds" / "model" / "generate.py"), str(root)], check=True, capture_output=True)
    return root


def _files(root: Path) -> dict[str, str]:
    found = {name: (root / name).read_text(encoding="utf-8") for name in GENERATED_FILES}
    for folder in GENERATED_FOLDERS:
        for path in sorted((root / folder).rglob("*")):
            if path.is_file():
                found[path.relative_to(root).as_posix()] = path.read_text(encoding="utf-8")
    return found


def test_committed_files_are_what_the_model_generates(generated: Path) -> None:
    expected, committed = _files(generated), _files(ORG)
    assert sorted(committed) == sorted(expected), "a generated folder holds a file the model does not produce, or misses one"
    stale = [name for name in expected if committed[name] != expected[name]]
    assert stale == [], f"run `make generate`: {stale[:5]}"


def test_the_generator_touches_nothing_hand_written(generated: Path) -> None:
    for folder in ("agents", "skills", "instructions/shared"):
        assert not (generated / folder).exists(), folder


def test_the_generator_states_its_usage_without_a_target() -> None:
    result = subprocess.run([sys.executable, str(ORG / "builds" / "model" / "generate.py")], capture_output=True, text=True)
    assert result.returncode != 0 and "generate.py <organization-root>" in result.stderr
