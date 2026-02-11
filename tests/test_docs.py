"""Documentation smoke tests for README and DOCS."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
DOCS = ROOT / "DOCS.md"


class TestDocs(unittest.TestCase):
    """Tests that core documentation sections exist."""

    def test_readme_has_core_sections(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("## Install", text)
        self.assertIn("## CLI Usage", text)
        self.assertIn("lyco compose", text)
        self.assertIn("lyco gui", text)
        self.assertIn("DOCS.md", text)

    def test_docs_has_usage_and_installation(self):
        text = DOCS.read_text(encoding="utf-8")
        self.assertIn("## Ways To Use", text)
        self.assertIn("## Invocation", text)
        self.assertIn("## Installation", text)
        self.assertIn("## Testing", text)
        self.assertIn("lyco compose", text)
        self.assertIn("python -m lyco", text)


if __name__ == "__main__":
    unittest.main()

