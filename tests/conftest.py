"""Shared pytest path setup for the organization suite."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ORG_ROOT = Path(__file__).resolve().parents[1]
HARNESS_CANDIDATES = (
    Path(os.environ["SAF_HARNESS_SRC"]) if os.environ.get("SAF_HARNESS_SRC") else None,
    Path(__file__).resolve().parents[2] / "saf-agentic-harness" / "src",
    Path(__file__).resolve().parents[3] / "saf" / "saf-agentic-harness" / "src",
    ORG_ROOT / ".harness" / "src",
)


def _harness_src() -> Path:
    for candidate in HARNESS_CANDIDATES:
        if candidate is None:
            continue
        if (candidate / "config" / "config_loader.py").is_file():
            return candidate
    raise RuntimeError(
        "saf-agentic-harness/src not found beside this checkout; "
        "set SAF_HARNESS_SRC to the harness src directory."
    )


HARNESS_SRC = _harness_src()
if str(HARNESS_SRC) not in sys.path:
    sys.path.insert(0, str(HARNESS_SRC))
if str(ORG_ROOT / "builds" / "github-copilot") not in sys.path:
    sys.path.insert(0, str(ORG_ROOT / "builds" / "github-copilot"))
