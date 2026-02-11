from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    if shutil.which("safety") is None:
        print("Missing tool: safety. Install with: python -m pip install safety")
        return 2

    if os.environ.get("RUN_SAFETY") != "1" or "SAFETY_API_KEY" not in os.environ:
        print("Safety scan skipped (set RUN_SAFETY=1 and SAFETY_API_KEY).")
        return 0
    cmd = [
        "safety",
        "scan",
        "--policy",
        str(ROOT / ".safety-policy.yml"),
        "-r",
        "requirements.txt",
        "-r",
        "requirements-dev.txt",
    ]
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
