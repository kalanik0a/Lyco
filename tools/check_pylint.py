from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    if shutil.which("pylint") is None:
        print("Missing tool: pylint. Install with: python -m pip install pylint")
        return 2

    cmd = ["pylint", "Lyco.py", "src"]
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
