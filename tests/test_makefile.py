"""Makefile target validation tests."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAKEFILE = ROOT / "Makefile"


def _parse_phony_targets(text: str) -> list[str]:
    """Parse .PHONY targets from the Makefile.

    Parameters
    ----------
    text : str
        Full Makefile contents.

    Returns
    -------
    list[str]
        Parsed phony targets.
    """
    targets: list[str] = []
    lines = text.splitlines()
    collecting = False
    buffer = ""
    for line in lines:
        if line.startswith(".PHONY:"):
            collecting = True
            buffer = line[len(".PHONY:"):].strip()
            if not line.rstrip().endswith("\\"):
                collecting = False
                targets.extend(buffer.split())
                buffer = ""
            continue
        if collecting:
            cleaned = line.strip()
            if cleaned.endswith("\\"):
                cleaned = cleaned[:-1].strip()
            buffer += " " + cleaned
            if not line.rstrip().endswith("\\"):
                collecting = False
                targets.extend(buffer.split())
                buffer = ""
    cleaned = [t for t in targets if t and t != "\\"]
    return sorted(set(cleaned))


def _make_available() -> bool:
    return shutil.which("make") is not None


class TestMakefileTargets(unittest.TestCase):
    """Validate Makefile targets are present and invokable."""

    def setUp(self) -> None:
        """Skip tests if make is unavailable."""
        if not _make_available():
            self.skipTest("make is not available on PATH")

    def test_phony_targets_defined(self):
        """Ensure each .PHONY target has a rule or dependency entry."""
        text = MAKEFILE.read_text(encoding="utf-8")
        targets = _parse_phony_targets(text)
        self.assertTrue(targets, "No .PHONY targets found")
        for target in targets:
            if re.search(rf"^{re.escape(target)}\s*:", text, re.MULTILINE) is None:
                self.fail(f"Target '{target}' has no rule definition")

    def test_make_dry_run(self):
        """Ensure all .PHONY targets are dry-run invokable."""
        text = MAKEFILE.read_text(encoding="utf-8")
        targets = _parse_phony_targets(text)
        for target in targets:
            result = subprocess.run(
                ["make", "-n", target],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                result.returncode,
                0,
                msg=f"Dry-run failed for target '{target}': {result.stderr}",
            )

    def test_make_real_run_optional(self):
        """Optionally run targets if RUN_MAKE_TARGETS=1 is set."""
        if os.environ.get("RUN_MAKE_TARGETS") != "1":
            self.skipTest("Set RUN_MAKE_TARGETS=1 to run targets")
        text = MAKEFILE.read_text(encoding="utf-8")
        targets = _parse_phony_targets(text)
        for target in targets:
            if target in {"docker-ci", "docker-check", "docker-security", "wsl-check",
                          "wsl-security", "wsl-ci", "wsl-docker-install",
                          "wsl-compose-ci", "wsl-compose-security", "test-one"}:
                continue
            env = os.environ.copy()
            env.setdefault("CI_GUARD_ALLOW", "1")
            env.setdefault("RUN_SAFETY", "0")
            result = subprocess.run(["make", target], cwd=ROOT, env=env)
            self.assertEqual(result.returncode, 0, msg=f"Target failed: {target}")


if __name__ == "__main__":
    unittest.main()
