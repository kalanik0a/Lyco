"""Tests for the binary-first launcher behavior."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if SRC.exists():
    sys.path.insert(0, str(SRC))

from lyco import launcher  # noqa: E402


class TestLauncher(unittest.TestCase):
    """Tests for launcher fallbacks."""

    def test_launcher_falls_back_to_python(self):
        with mock.patch.object(launcher, "_compiled_binary_path") as path_mock:
            path_mock.return_value = Path("nonexistent")
            with mock.patch.object(launcher.cli, "main") as cli_main:
                launcher.main()
                cli_main.assert_called_once()

    def test_launcher_runs_binary_if_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            binary = Path(tmp) / ("lyco.exe" if sys.platform.startswith("win") else "lyco")
            binary.write_text("stub", encoding="utf-8")
            with mock.patch.object(launcher, "_compiled_binary_path", return_value=binary):
                with mock.patch("subprocess.call", return_value=0) as call_mock:
                    with self.assertRaises(SystemExit) as ctx:
                        launcher.main()
                    self.assertEqual(ctx.exception.code, 0)
                    call_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()

