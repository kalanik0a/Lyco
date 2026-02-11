# Lyco Python Framework

Lyco Python Framework is a starter framework for building Python desktop tools. The image mosaic app in this repo is the **Hello-world** example: it composes a transparent wallpaper from a YAML layout file and includes a PyQt GUI editor.

## Clone, Fork, Extend

This repo is designed to be cloned or forked as a base for your own projects:

1. Clone the repo.
2. Run `python tools/setup_env.py` to generate a `.env` tuned for your OS/CI.
3. Replace the example app (`src/lyco_image_mosaic/cli.py`) with your own logic.
4. Update `pyproject.toml` (name, description, entry points) for your new project.
5. Keep the tooling, CI/CD, and security workflow as your project foundation.

![Hello-world image mosaic screenshot](img/screenshot.png)


## Install

Target Python version: 3.12 (see `.python-version`).

PyPI (after publishing):

```powershell
python -m pip install lyco-python-framework
```

This installs the `lyco` command in your environment. If a platform wheel with the
bundled binary is available, `lyco` runs the compiled binary; otherwise it falls back
to the pure-Python entry point.

Cross-platform notes:
- Windows: The `lyco` command is installed into the Python Scripts directory. If `lyco`
  is not found, ensure your Python Scripts path is on `PATH`.
- Windows: `semgrep` is not supported on native Windows; use WSL or run semgrep in CI.
Optional helpers: `powershell tools/run_semgrep_wsl.ps1`, `powershell tools/run_semgrep_docker.ps1`.
- macOS: First run of downloaded binaries may be blocked by Gatekeeper. If prompted,
  allow the app in System Settings > Privacy & Security.
- Linux: The GUI needs an active display server (X11/Wayland). On headless systems,
  use `lyco compose` without `gui`.
- Wheels with the compiled binary are OS- and Python-version-specific. If a wheel for
  your platform is not available, installation falls back to pure Python.
- For portable Python installs, set `LYCO_PYTHON` and `LYCO_VENV` in `.env`.
- WSL/Docker security checks are available (see `TOOLING.md`).

Local development:

```powershell
python -m pip install -r requirements.txt
```

Dependencies are pinned in `requirements.txt` for reproducibility.

Developer tools:

```powershell
python -m pip install -r requirements-dev.txt
```

Optional semgrep tools (separate to avoid dependency conflicts with pip-audit):

```powershell
python -m pip install -r requirements-semgrep.txt
```

Security tooling uses `safety scan` with `.safety-policy.yml`.
Set `SAFETY_API_KEY` to enable the scan in non-interactive environments; otherwise the check is skipped.
Set `RUN_SAFETY=1` to enable safety scans, `RUN_SBOM=1` to force SBOM regeneration, and `RUN_SEMGREP=1` on supported platforms.

Editable install (recommended for development):

```powershell
python -m pip install -e .
```

Environment setup (auto-detects OS/CI and writes `.env`):

```powershell
python tools/setup_env.py
```

Key `.env` fields:
- `LYCO_OS` (`windows`, `macos`, `linux`) and `LYCO_CI_PROVIDER` (`github`, `gitlab`, `none`).
- `LYCO_PYTHON` and `LYCO_VENV` to point at a portable Python + venv path.

Task runner (cross-platform):

```powershell
python tools/run_task.py ci-fast
python tools/run_task.py ci-full
```

The task runner respects `LYCO_PYTHON` for portable Python installs and reports
when the `venv` module is unavailable (common in minimal containers).

Framework swapping:
- Update `src/lyco_image_mosaic/app_config.json` (or set `LYCO_APP_CONFIG`) to point
  at your app module and callable when you fork the framework.

## YAML Layout Format

```yaml
output: wallpaper.png
canvas_width: 7680
canvas_height: 2160
items:
  - file: "img1.png"
    x: 0
    y: 0
    resolution: "1920x1080"
  - file: "img2.jpg"
    x: 1920
    y: 0
    resolution: "2560x1440"
```

Notes:
- `canvas_width` and `canvas_height` are optional. If omitted, Lyco uses the bounding box of items.
- Coordinates are normalized so `0,0` is the top-left of the entire layout when saving from the GUI.

## CLI Usage

Compose a wallpaper from YAML:

```powershell
lyco compose -c layout.yml -o wallpaper.png
```

## GUI Usage

Open the editor:

```powershell
lyco gui -c layout.yml
```

Run directly from the repo without installing:

```powershell
python Lyco.py compose -c layout.yml -o wallpaper.png
python Lyco.py gui -c layout.yml
```

GUI controls:
- Drag rectangles to move items.
- Ctrl + Mouse Wheel to zoom.
- Ctrl + Click + Drag to pan.
- Export PNG to save a transparent wallpaper image.
- Save YAML to normalize coordinates and update canvas bounds.

## License

GNU General Public License v3.0. See `LICENSE`.

## Build Notes (Maintainers)

Build a compiled binary (Nuitka) and bundle it into wheels:

```powershell
python -m pip install .[build]
python tools/build_binary.py
python -m build
```

Note: Nuitka does not support the Windows Store Python distribution. Use Python from python.org for binary builds on Windows.

Multi-platform wheels with `cibuildwheel`:

```powershell
python -m pip install .[build]
cibuildwheel --output-dir dist
```

Upload to PyPI:

```powershell
python -m pip install .[build]
twine upload dist/*
```

For a full rundown of usage, installation modes, and testing, see `DOCS.md`.

## Tests

Run the unit test suite:

```powershell
python -m unittest discover -s tests
```

CI is configured for GitHub Actions and GitLab CI (`.github/workflows/ci.yml`, `.gitlab-ci.yml`).
VS Code tasks are available in `.vscode/tasks.json` for run, build, test, and CI checks.

Post CI/CD remediation tools:
`python tools/post_ci_cd_report.py`, `python tools/sbom_inspect.py`.

Tooling flags and cache behavior are documented in `TOOLING.md`.

Test suites:
`python -m unittest tests.test_suite_core`, `python -m unittest tests.test_suite_full`.

Python environment:
`.python-version`, `.env.example`, `requirements.lock`.
VS Code environment: `.vscode/settings.json`.
UI testing guidance: `tools/ui_testing.md`.

Makefile targets:
`make setup-env`, `make venv`, `make ci-fast`, `make ci-full`, `make test-core`, `make test-full`.
Lockfile: `make requirements-lock`.
WSL/Docker checks: `make wsl-check`, `make wsl-security`, `make docker-check`, `make docker-security`.
WSL/Docker CI: `make wsl-ci`, `make docker-ci`.
WSL Docker Compose: `scripts/wsl_install_docker.sh`, then `scripts/wsl_run_compose.sh ci`.
WSL Make targets: `make wsl-docker-install`, `make wsl-compose-ci`, `make wsl-compose-security`.

Windows note: `make` may not be installed by default; use VS Code tasks or run
the Python tooling scripts directly.
