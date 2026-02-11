"""Core unit test suite (fast)."""

from __future__ import annotations

import unittest


def load_tests(loader, tests, pattern):
    """Load core unit tests."""
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromName("tests.test_cli"))
    suite.addTests(loader.loadTestsFromName("tests.test_launcher"))
    suite.addTests(loader.loadTestsFromName("tests.test_docs"))
    return suite


if __name__ == "__main__":
    unittest.main()
