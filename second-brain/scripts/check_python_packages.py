"""Minimal no-dependency import-boundary check for the initial monorepo."""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRS = [
    ROOT / "apps/api/src", ROOT / "apps/worker/src", ROOT / "packages/agent/src",
    ROOT / "packages/rag/src", ROOT /
    "packages/memory/src", ROOT / "packages/graph/src",
    ROOT / "packages/mcp/src",
]
for source_dir in SOURCE_DIRS:
    sys.path.insert(0, str(source_dir))

for package in ["second_brain_api", "second_brain_worker", "second_brain_agent", "second_brain_rag", "second_brain_memory", "second_brain_graph", "second_brain_mcp"]:
    importlib.import_module(package)
    print(f"imported {package}")
