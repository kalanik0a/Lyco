"""Launcher that prefers a bundled compiled binary if present."""

from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

from . import cli  # pylint: disable=import-error,no-name-in-module


def _compiled_binary_path() -> Path:
    """Return the expected path of the bundled compiled binary."""
    bin_dir = Path(__file__).resolve().parent / "bin"
    exe = "lyco.exe" if os.name == "nt" else "lyco"
    return bin_dir / exe


def main() -> None:
    """Run the compiled binary if available, otherwise run the Python CLI."""
    binary = _compiled_binary_path()
    if binary.exists():
        raise SystemExit(subprocess.call([str(binary), *sys.argv[1:]]))

    # Allow swapping the app module via config or env when used as a framework.
    config_path = os.environ.get("LYCO_APP_CONFIG")
    if config_path:
        config_file = Path(config_path)
    else:
        config_file = Path(__file__).resolve().parent / "app_config.json"

    if config_file.exists():
        try:
            data = json.loads(config_file.read_text(encoding="utf-8"))
            module_path = data.get("module", "lyco.cli")
            callable_name = data.get("callable", "main")
            module = importlib.import_module(module_path)
            entry = getattr(module, callable_name)
            entry()
            return
        except Exception as exc:
            print(f"Failed to load app config ({config_file}): {exc}")

    # Fallback to pure Python entry point when no compiled binary is bundled.
    cli.main()
