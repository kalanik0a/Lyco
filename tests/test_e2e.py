"""End-to-end tests for installation, invocation, and compile flows."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestE2EInvocations(unittest.TestCase):
    """End-to-end tests for supported invocation paths."""

    def _run(
        self,
        args: list[str],
        env: dict[str, str] | None = None,
        cwd: Path | None = None,
    ) -> subprocess.CompletedProcess:
        """Run a subprocess and return the completed process."""
        return subprocess.run(
            args,
            cwd=cwd or ROOT,
            env=env,
            capture_output=True,
            text=True,
        )

    def test_repo_wrapper_help(self):
        """Lyco.py wrapper should print help."""
        result = self._run([sys.executable, "Lyco.py", "--help"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertTrue(
            "Lyco Python Framework" in result.stdout
            or "Lyco Image Mosaic" in result.stdout
        )

    def test_module_help_with_pythonpath(self):
        """Module invocation should work with PYTHONPATH=src."""
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT / "src")
        result = self._run([sys.executable, "-m", "lyco_image_mosaic", "--help"], env=env)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertTrue(
            "Lyco Python Framework" in result.stdout
            or "Lyco Image Mosaic" in result.stdout
        )

    def test_compose_via_module(self):
        """Compose should succeed via module invocation."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            img = tmp_path / "img.png"
            layout = tmp_path / "layout.yml"
            output = tmp_path / "out.png"

            from PIL import Image

            Image.new("RGBA", (16, 16), (255, 0, 0, 255)).save(img)
            layout.write_text(
                "\n".join(
                    [
                        "output: out.png",
                        "items:",
                        "  - file: \"img.png\"",
                        "    x: 0",
                        "    y: 0",
                        "    resolution: \"16x16\"",
                    ]
                ),
                encoding="utf-8",
            )

            env = os.environ.copy()
            env["PYTHONPATH"] = str(ROOT / "src")
            result = self._run(
                [sys.executable, "-m", "lyco_image_mosaic", "compose", "-c", str(layout), "-o", str(output)],
                env=env,
                cwd=tmp_path,
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertTrue(output.exists())

    def test_lyco_command_help_if_installed(self):
        """If lyco is installed, it should print help."""
        if shutil.which("lyco") is None:
            self.skipTest("lyco command not found in PATH")
        result = self._run(["lyco", "--help"])
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertTrue(
            "Lyco Python Framework" in result.stdout
            or "Lyco Image Mosaic" in result.stdout
        )


class TestE2ECompile(unittest.TestCase):
    """End-to-end compile checks using Nuitka when supported."""

    def test_nuitka_build_if_supported(self):
        """Attempt Nuitka build when supported; skip otherwise."""
        if "WindowsApps" in sys.executable:
            self.skipTest("Windows Store Python is not supported by Nuitka")
        if shutil.which("nuitka") is None:
            self.skipTest("Nuitka is not installed")

        result = subprocess.run(
            [sys.executable, "tools/build_binary.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)


if __name__ == "__main__":
    unittest.main()
