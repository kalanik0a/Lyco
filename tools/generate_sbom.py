from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    if os.environ.get("RUN_SBOM") in ("0", "false", "False"):
        print("SBOM generation skipped (set RUN_SBOM=1 to enable).")
        return 0
    if shutil.which("cyclonedx-py") is None:
        print(
            "Missing tool: cyclonedx-bom. Install with: python -m pip install cyclonedx-bom"
        )
        return 2

    out_dir = ROOT / "sbom"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "sbom.json"

    cmd = [
        "cyclonedx-py",
        "requirements",
        "-i",
        "requirements.txt",
        "-o",
        str(out_file),
    ]
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
