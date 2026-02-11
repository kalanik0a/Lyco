from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "build" / "ci" / "last_run.json"


def _hash_requirements() -> str:
    h = hashlib.sha256()
    for name in ("requirements.txt", "requirements-dev.txt"):
        path = ROOT / name
        if path.exists():
            h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    """Return 1 when SBOM should be regenerated, 0 when it can be skipped."""
    if os.environ.get("RUN_SBOM") == "1":
        return 1
    current = _hash_requirements()
    if not ARTIFACT.exists():
        return 1
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    sbom = ROOT / "sbom" / "sbom.json"
    if not sbom.exists():
        return 1
    if data.get("requirements_hash") != current:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
