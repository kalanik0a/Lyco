from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    if shutil.which("pylint") is None:
        print("Missing tool: pylint. Install with: python -m pip install pylint")
        return 2

    src_path = str(ROOT / "src")
    cmd = [
        "pylint",
        f"--init-hook=import sys; sys.path.insert(0, r'{src_path}')",
        "Lyco.py",
        "src",
    ]
    print("Running:", " ".join(cmd))
    env = dict(**os.environ)
    env["PYTHONPATH"] = src_path + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.call(cmd, cwd=ROOT, env=env)


if __name__ == "__main__":
    raise SystemExit(main())
