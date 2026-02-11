from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _run(cmd: list[str]) -> int:
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd)


def _require(tool: str) -> bool:
    if shutil.which(tool) is None:
        print(f"Missing tool: {tool}. Install the security extras to proceed.")
        return False
    return True


def main() -> int:
    exit_code = 0

    if not _require("bandit"):
        return 2
    if os.environ.get("RUN_BANDIT") in ("0", "false", "False"):
        print("Bandit skipped (set RUN_BANDIT=1 to enable).")
    else:
        exit_code |= _run(["bandit", "-c", str(ROOT / ".bandit"), "-r", "src", "Lyco.py", "tools"])

    if not _require("pip-audit"):
        return 2
    exit_code |= _run(["pip-audit", "-r", "requirements.txt", "-r", "requirements-dev.txt"])

    if not _require("safety"):
        return 2
    if os.environ.get("RUN_SAFETY") != "1" or "SAFETY_API_KEY" not in os.environ:
        print("Safety scan skipped (set RUN_SAFETY=1 and SAFETY_API_KEY).")
    else:
        exit_code |= _run(
            [
                "safety",
                "scan",
                "--policy",
                str(ROOT / ".safety-policy.yml"),
                "-r",
                "requirements.txt",
                "-r",
                "requirements-dev.txt",
            ]
        )

    if os.environ.get("RUN_SEMGREP") != "1":
        print("Semgrep skipped (set RUN_SEMGREP=1 to enable).")
    elif os.environ.get("LYCO_OS", platform.system().lower()).startswith("win"):
        print("Skipping semgrep: not supported on Windows without WSL.")
    else:
        if not _require("semgrep"):
            return 2
        exit_code |= _run(["semgrep", "--config", str(ROOT / ".semgrep.yml"), "src", "Lyco.py", "tools"])

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
