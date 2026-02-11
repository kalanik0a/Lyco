from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    if shutil.which("pip-audit") is None:
        print("Missing tool: pip-audit. Install with: python -m pip install pip-audit")
        return 2

    cmd = ["pip-audit", "-r", "requirements.txt", "-r", "requirements-dev.txt"]
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
