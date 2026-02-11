"""Detect local Docker availability."""
from __future__ import annotations

import shutil
import subprocess


def main() -> int:
    if shutil.which("docker") is None:
        print("Docker CLI not found.")
        return 2
    result = subprocess.run(["docker", "info"], capture_output=True, text=True)  # nosec B607
    if result.returncode != 0:
        print("Docker is installed but not running or not accessible.")
        return 2
    print("Docker is available.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
