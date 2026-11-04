"""Pain points are written only by the role the access-control list authorizes.

The harness denies a `pain-point` write by any other actor, so an orchestrator that does not
hold the privilege must route the pain point to the owner instead of writing it.
"""

from __future__ import annotations

import pytest
import yaml

from tests.conftest import ORG_ROOT

ORCHESTRATORS = ("value-management-officer", "release-train-engineer", "scrum-master")
OWNER_RULE = "**Only `@release-train-engineer` writes pain points**"


def _pain_point_writers() -> set[str]:
    acl = yaml.safe_load((ORG_ROOT / "conf" / "access-control-list.conf.yaml").read_text(encoding="utf-8"))
    roles = {
        role["slug"]
        for role in acl["roles"]
        if any(p["artifact"] == "pain-point" and p["action"] == "create" for p in role["privileges"])
    }
    return {actor["slug"] for actor in acl["actors"] if roles & set(actor["roles"])}


def test_only_the_release_train_engineer_may_create_pain_points() -> None:
    assert _pain_point_writers() == {"release-train-engineer"}


@pytest.mark.parametrize("slug", [slug for slug in ORCHESTRATORS if slug != "release-train-engineer"])
def test_other_orchestrators_route_pain_points_to_the_owner(slug: str) -> None:
    text = (ORG_ROOT / "skills" / f"{slug}.skill.md").read_text(encoding="utf-8")
    assert OWNER_RULE in text
