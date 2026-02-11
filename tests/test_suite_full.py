"""Full unit test suite (includes E2E and local CI)."""

from __future__ import annotations

import unittest


def load_tests(loader, tests, pattern):
    """Load full test suite."""
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromName("tests.test_cli"))
    suite.addTests(loader.loadTestsFromName("tests.test_launcher"))
    suite.addTests(loader.loadTestsFromName("tests.test_docs"))
    suite.addTests(loader.loadTestsFromName("tests.test_e2e"))
    suite.addTests(loader.loadTestsFromName("tests.test_ci_local"))
    return suite


if __name__ == "__main__":
    unittest.main()
