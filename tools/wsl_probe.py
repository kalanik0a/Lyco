"""Detect WSL availability and advise on distro setup."""
from __future__ import annotations

import os
from tools import wsl_utils


def main() -> int:
    status = wsl_utils.get_status()
    if not status.installed:
        print("WSL is not installed. WSL mode cannot run.")
        print("Install WSL 2 and a Linux distro (Ubuntu recommended).")
        print("Suggested: wsl --install -d Ubuntu")
        return 2

    if not status.distros:
        print("WSL is installed but no distros are registered.")
        print("Install a distro (Ubuntu recommended).")
        print("Suggested: wsl --install -d Ubuntu")
        return 2

    selected = wsl_utils.resolve_distro()
    if not selected:
        print("WSL is installed, but no usable distro found.")
        return 2

    if os.environ.get("WSL_DISTRO") and os.environ.get("WSL_DISTRO") != selected:
        print(f"Requested WSL_DISTRO not found. Using {selected}.")
    print(f"WSL ready. Using distro: {selected}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
