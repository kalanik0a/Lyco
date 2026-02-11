"""Build a compiled Lyco binary with Nuitka and bundle it into the package."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    """Build the compiled binary and copy it into the package.

    Returns
    -------
        Process exit code. Zero indicates success.
    """
    root = Path(__file__).resolve().parents[1]
    src = root / "src" / "lyco_image_mosaic" / "cli.py"
    if not src.exists():
        print(f"Missing source: {src}")
        return 1

    out_dir = root / "build" / "nuitka"
    out_dir.mkdir(parents=True, exist_ok=True)

    exe_name = "lyco.exe" if os.name == "nt" else "lyco"
    cmd = [
        sys.executable,
        "-m",
        "nuitka",
        "--onefile",
        "--enable-plugin=pyqt5",
        f"--output-dir={out_dir}",
        "--output-filename=lyco",
        str(src),
    ]
    print("Running:", " ".join(cmd))
    result = subprocess.call(cmd)
    if result != 0:
        return result

    built = out_dir / exe_name
    if not built.exists():
        # Nuitka may append a .bin on some platforms; try to locate it.
        candidates = list(out_dir.glob("lyco*"))
        if candidates:
            built = candidates[0]
        else:
            print(f"Built binary not found in {out_dir}")
            return 1

    bin_dir = root / "src" / "lyco_image_mosaic" / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    target = bin_dir / exe_name
    shutil.copy2(built, target)
    print(f"Copied binary to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
