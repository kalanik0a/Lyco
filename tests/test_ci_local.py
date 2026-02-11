"""Local CI/CD checks executed via unittest."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _skip_unless_enabled(testcase: unittest.TestCase) -> None:
    """Skip unless RUN_LOCAL_CI=1 is set."""
    if os.environ.get("RUN_LOCAL_CI") != "1":
        testcase.skipTest("Set RUN_LOCAL_CI=1 to run local CI checks")


class TestLocalCI(unittest.TestCase):
    """Run local CI scripts and assert success."""

    def test_pylint(self):
        """Run pylint wrapper."""
        _skip_unless_enabled(self)
        result = subprocess.run([sys.executable, "tools/check_pylint.py"], cwd=ROOT)
        self.assertEqual(result.returncode, 0)

    def test_vulnerabilities(self):
        """Run Safety scan wrapper."""
        _skip_unless_enabled(self)
        result = subprocess.run([sys.executable, "tools/check_vulnerabilities.py"], cwd=ROOT)
        self.assertEqual(result.returncode, 0)

    def test_audit(self):
        """Run pip-audit wrapper."""
        _skip_unless_enabled(self)
        result = subprocess.run([sys.executable, "tools/check_audit.py"], cwd=ROOT)
        self.assertEqual(result.returncode, 0)

    def test_security(self):
        """Run combined security checks."""
        _skip_unless_enabled(self)
        result = subprocess.run([sys.executable, "tools/security_checks.py"], cwd=ROOT)
        self.assertEqual(result.returncode, 0)

    def test_sbom(self):
        """Run SBOM generation."""
        _skip_unless_enabled(self)
        result = subprocess.run([sys.executable, "tools/generate_sbom.py"], cwd=ROOT)
        self.assertEqual(result.returncode, 0)

    def test_ci_record(self):
        """Write CI artifact."""
        _skip_unless_enabled(self)
        result = subprocess.run([sys.executable, "tools/ci_record.py"], cwd=ROOT)
        self.assertEqual(result.returncode, 0)


class TestSuiteCategories(unittest.TestCase):
    """Meta tests for suite grouping."""

    def test_core_suite_exists(self):
        """Core suite module should be importable."""
        __import__("tests.test_suite_core")

    def test_full_suite_exists(self):
        """Full suite module should be importable."""
        __import__("tests.test_suite_full")


class TestToolingEdgeCases(unittest.TestCase):
    """Validate expected behavior when tools are missing."""

    def test_semgrep_missing_on_windows(self):
        """Semgrep should be optional on Windows."""
        _skip_unless_enabled(self)
        if not sys.platform.startswith("win"):
            self.skipTest("Windows-only expectation")
        if shutil.which("semgrep") is None:
            # Ensure the helper script exists (no execution here).
            self.assertTrue((ROOT / "tools" / "run_semgrep_wsl.ps1").exists())


if __name__ == "__main__":
    unittest.main()
