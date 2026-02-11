"""Run security checks inside WSL."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

from tools import wsl_utils


ROOT = Path(__file__).resolve().parents[1]


def _wsl_path(path: Path) -> str:
    result = subprocess.run(["wsl.exe", "wslpath", "-a", str(path)], capture_output=True, text=True)  # nosec B607
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()


def main() -> int:
    status = wsl_utils.get_status()
    if not status.installed:
        print("WSL is not installed. Cannot run WSL security checks.")
        return 2
    distro = wsl_utils.resolve_distro()
    if not distro:
        print("No WSL distro configured. Set WSL_DISTRO or install Ubuntu.")
        return 2

    root_path = _wsl_path(ROOT)
    env = os.environ.copy()
    env.setdefault("RUN_SAFETY", "1" if env.get("SAFETY_API_KEY") else "0")
    env.setdefault("RUN_SEMGREP", "1")
    env.setdefault("RUN_SBOM", "0")
    env.setdefault("RUN_SECRET_SCAN", "1")

    env_prefix = (
        f"RUN_SAFETY={env['RUN_SAFETY']} "
        f"RUN_SEMGREP={env['RUN_SEMGREP']} "
        f"RUN_SBOM={env['RUN_SBOM']} "
        f"RUN_SECRET_SCAN={env['RUN_SECRET_SCAN']}"
    )
    cmd = [
        "wsl.exe",
        "-d",
        distro,
        "--",
        "bash",
        "-lc",
        f"cd {root_path} && {env_prefix} python3 tools/security_checks.py && python3 tools/check_vulnerabilities.py",
    ]
    print(f"Running WSL security checks in {distro}...")
    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
