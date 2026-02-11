"""Remove build/test artifacts for a clean working tree."""
from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


DIRS = [
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".nox",
    "build",
    "dist",
    "htmlcov",
    "sbom",
]

FILES = [
    ".coverage",
    "coverage.xml",
]


def main() -> int:
    for name in DIRS:
        path = ROOT / name
        shutil.rmtree(path, ignore_errors=True)
    for name in FILES:
        path = ROOT / name
        if path.exists():
            path.unlink()
    for egg in ROOT.glob("*.egg-info"):
        shutil.rmtree(egg, ignore_errors=True)
    for egg in (ROOT / "src").glob("*.egg-info"):
        shutil.rmtree(egg, ignore_errors=True)
    print("Cleaned build/test artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
