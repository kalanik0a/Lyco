"""Utilities for detecting and invoking WSL."""
from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass


@dataclass
class WslStatus:
    installed: bool
    distros: list[str]
    default_distro: str | None
    error: str | None = None


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def wsl_installed() -> bool:
    try:
        result = _run(["wsl.exe", "--status"])
        return result.returncode == 0
    except FileNotFoundError:
        return False


def list_distros() -> tuple[list[str], str | None]:
    result = _run(["wsl.exe", "-l", "-v"])
    if result.returncode != 0:
        return [], None
    distros: list[str] = []
    default: str | None = None
    for line in result.stdout.splitlines():
        if not line.strip() or line.lower().startswith("name"):
            continue
        is_default = line.lstrip().startswith("*")
        cleaned = line.replace("*", "").strip()
        parts = cleaned.split()
        if not parts:
            continue
        name = parts[0]
        distros.append(name)
        if is_default:
            default = name
    return distros, default


def get_status() -> WslStatus:
    if not wsl_installed():
        return WslStatus(installed=False, distros=[], default_distro=None)
    distros, default = list_distros()
    return WslStatus(installed=True, distros=distros, default_distro=default)


def resolve_distro() -> str | None:
    override = os.environ.get("WSL_DISTRO")
    status = get_status()
    if override and override in status.distros:
        return override
    if status.default_distro:
        return status.default_distro
    if status.distros:
        return status.distros[0]
    return None
