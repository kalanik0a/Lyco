"""Bridge to run Docker install/compose inside WSL."""
from __future__ import annotations

import subprocess
import sys
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
        print("WSL is not installed. Cannot run WSL docker actions.")
        return 2
    distro = wsl_utils.resolve_distro()
    if not distro:
        print("No WSL distro configured. Set WSL_DISTRO or install Ubuntu.")
        return 2

    if len(sys.argv) < 2:
        print("Usage: python tools/run_wsl_docker.py <install|compose> [ci|security]")
        return 2

    action = sys.argv[1]
    root_path = _wsl_path(ROOT)
    scripts_path = f"{root_path}/scripts"

    if action == "install":
        cmd = ["wsl.exe", "-d", distro, "--", "bash", "-lc", f"{scripts_path}/wsl_install_docker.sh"]
    elif action == "compose":
        if len(sys.argv) < 3:
            print("Usage: python tools/run_wsl_docker.py compose <ci|security>")
            return 2
        mode = sys.argv[2]
        cmd = [
            "wsl.exe",
            "-d",
            distro,
            "--",
            "bash",
            "-lc",
            f"{scripts_path}/wsl_run_compose.sh {mode}",
        ]
    else:
        print("Unknown action. Use install or compose.")
        return 2

    print(f"Running WSL docker action '{action}' in {distro}...")
    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
