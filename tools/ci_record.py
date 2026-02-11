from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
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
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    sbom_path = ROOT / "sbom" / "sbom.json"
    sbom_hash = ""
    if sbom_path.exists():
        sbom_hash = hashlib.sha256(sbom_path.read_bytes()).hexdigest()
    data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "requirements_hash": _hash_requirements(),
        "sbom_path": str(sbom_path),
        "sbom_hash": sbom_hash,
    }
    ARTIFACT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {ARTIFACT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
