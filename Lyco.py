"""Compatibility wrapper for running Lyco from the repo root."""

# pylint: disable=invalid-name,wrong-import-position,import-error,no-name-in-module

from pathlib import Path
import sys

root = Path(__file__).resolve().parent
src = root / "src"
if src.exists():
    sys.path.insert(0, str(src))

from lyco.cli import main  # noqa: E402


if __name__ == "__main__":
    main()
