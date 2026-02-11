from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    sbom = ROOT / "sbom" / "sbom.json"
    if not sbom.exists():
        print("SBOM not found. Run: python tools/generate_sbom.py")
        return 1

    data = json.loads(sbom.read_text(encoding="utf-8"))
    components = data.get("components", [])
    print(f"Components: {len(components)}")
    for comp in components:
        name = comp.get("name", "unknown")
        version = comp.get("version", "unknown")
        purl = comp.get("purl", "")
        print(f"- {name}=={version} {purl}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
