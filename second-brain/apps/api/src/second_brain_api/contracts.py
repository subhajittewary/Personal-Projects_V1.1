"""Cross-service contracts are canonicalized under /contracts/json-schema."""
from pathlib import Path

CONTRACTS_DIR = Path(__file__).resolve().parents[4] / "contracts" / "json-schema"
