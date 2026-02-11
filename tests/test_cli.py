"""Tests for CLI helpers and compose workflow."""

import os
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if SRC.exists():
    sys.path.insert(0, str(SRC))

from lyco import cli  # noqa: E402


class TestParseResolution(unittest.TestCase):
    """Tests for parse_resolution."""

    def test_parse_resolution_valid(self):
        self.assertEqual(cli.parse_resolution("1920x1080"), (1920, 1080))
        self.assertEqual(cli.parse_resolution("2560X1440"), (2560, 1440))

    def test_parse_resolution_invalid(self):
        with self.assertRaises(SystemExit):
            cli.parse_resolution("bad")
        with self.assertRaises(SystemExit):
            cli.parse_resolution("0x100")


class TestYamlHelpers(unittest.TestCase):
    """Tests for YAML load/save helpers."""

    def test_load_save_yaml_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "layout.yml"
            data = {"output": "out.png", "items": []}
            cli.save_yaml(path, data)
            loaded = cli.load_yaml(path)
            self.assertEqual(loaded, data)


class TestCompose(unittest.TestCase):
    """Tests for composing a PNG from YAML."""

    def _write_test_image(self, path: Path, size: tuple[int, int], color=(255, 0, 0, 255)):
        from PIL import Image

        img = Image.new("RGBA", size, color)
        img.save(path)

    def test_compose_from_yaml(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            img1 = tmp_path / "img1.png"
            img2 = tmp_path / "img2.png"
            self._write_test_image(img1, (32, 32), (255, 0, 0, 255))
            self._write_test_image(img2, (64, 64), (0, 255, 0, 255))

            layout = tmp_path / "layout.yml"
            layout.write_text(
                "\n".join(
                    [
                        "output: out.png",
                        "items:",
                        "  - file: \"img1.png\"",
                        "    x: 0",
                        "    y: 0",
                        "    resolution: \"32x32\"",
                        "  - file: \"img2.png\"",
                        "    x: 32",
                        "    y: 0",
                        "    resolution: \"64x64\"",
                    ]
                ),
                encoding="utf-8",
            )

            output = tmp_path / "out.png"
            cwd = os.getcwd()
            try:
                # compose_from_yaml reads relative paths; run from layout dir.
                os.chdir(tmp_path)
                cli.compose_from_yaml(layout, str(output))
            finally:
                os.chdir(cwd)

            self.assertTrue(output.exists())

    def test_compose_invalid_yaml(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            layout = tmp_path / "layout.yml"
            layout.write_text("output: out.png", encoding="utf-8")
            with self.assertRaises(SystemExit):
                cli.compose_from_yaml(layout, None)


if __name__ == "__main__":
    unittest.main()

