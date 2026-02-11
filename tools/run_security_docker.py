"""Run security checks inside Docker."""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    if shutil.which("docker") is None:
        print("Docker CLI not found.")
        return 2

    image = os.environ.get("DOCKER_IMAGE", "python:3.12")
    run_safety = os.environ.get("RUN_SAFETY")
    if run_safety is None:
        run_safety = "1" if os.environ.get("SAFETY_API_KEY") else "0"
    env = [
        f"RUN_SAFETY={run_safety}",
        f"RUN_SEMGREP={os.environ.get('RUN_SEMGREP', '0')}",
        f"RUN_SBOM={os.environ.get('RUN_SBOM', '0')}",
        f"RUN_SECRET_SCAN={os.environ.get('RUN_SECRET_SCAN', '1')}",
        f"SAFETY_API_KEY={os.environ.get('SAFETY_API_KEY', '')}",
    ]
    cmd = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{ROOT}:/workspace",
        "-w",
        "/workspace",
        *sum([["-e", item] for item in env], []),
        image,
        "bash",
        "-lc",
        "python3 -m pip install -r requirements.txt -r requirements-dev.txt "
        "&& python3 tools/security_checks.py "
        "&& python3 tools/check_vulnerabilities.py",
    ]
    print(f"Running Docker security checks in {image}...")
    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
