# Lyco Python Framework - Docs

This document lists all supported ways to use, invoke, install, and test the Lyco Python Framework and its Hello-world example app.

## Ways To Use

- Use the Hello-world example to compose a transparent wallpaper from a YAML layout file.
- Edit layouts with a PyQt GUI and export a PNG.
- Run via the installed `lyco` command.
- Run directly from the repository without installing.
- Clone/fork the framework as a starting point for your own desktop tools.

## Forking Workflow (Template Use)

1. Run `python tools/setup_env.py` to create a `.env` for your OS/CI.
2. Rename the package in `pyproject.toml` and update entry points.
3. Replace `src/lyco_image_mosaic` with your app module.
4. Keep `tools/`, `.github/`, `.gitlab-ci.yml`, and `Makefile` as your baseline workflow.

## Invocation

CLI (installed):

```powershell
lyco compose -c layout.yml -o wallpaper.png
lyco gui -c layout.yml
```

CLI (repo, no install):

```powershell
python Lyco.py compose -c layout.yml -o wallpaper.png
python Lyco.py gui -c layout.yml
```

Module (if installed):

```powershell
python -m lyco_image_mosaic compose -c layout.yml -o wallpaper.png
python -m lyco_image_mosaic gui -c layout.yml
```

If running from the repo without installation, set `PYTHONPATH=src`:

```powershell
$env:PYTHONPATH="src"
python -m lyco_image_mosaic --help
```

## Installation

Target Python version: 3.12 (see `.python-version`).

PyPI (after publishing):

```powershell
python -m pip install lyco-python-framework
```

Editable (development):

```powershell
python -m pip install -e .
```

Requirements only (manual run):

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

### Environment Setup (After Clone)

Run the environment configuration script to generate `.env` with OS/CI defaults:

```powershell
python tools/setup_env.py
```

You can override detection:

```powershell
python tools/setup_env.py --os windows --ci gitlab --venv .venv
```

Key `.env` fields:
- `LYCO_OS` (`windows`, `macos`, `linux`) and `LYCO_CI_PROVIDER` (`github`, `gitlab`, `none`).
- `LYCO_PYTHON` and `LYCO_VENV` to point at a portable Python + venv path.

The task runner (`tools/run_task.py`) respects `LYCO_PYTHON` for portable Python installs
and logs when the `venv` module is unavailable (common in minimal containers).

### Framework Swapping

The framework exposes a small app config file for swapping the example module:

- `src/lyco_image_mosaic/app_config.json` defines the module and callable to invoke.
- Override with `LYCO_APP_CONFIG=/path/to/your/app_config.json`.

This allows a forked project to change one file to point at the new module
while keeping the rest of the framework intact.

### Cross-Platform Notes And OS-Specific Caveats

- Wheels with the compiled binary are OS- and Python-version-specific. If a wheel for
  your platform is not available, installation falls back to pure Python.
- The GUI requires a desktop display environment. On headless systems, use `lyco compose`.
- PyQt5 availability can vary by platform and Python version. If `pip` cannot find
  a compatible wheel, install a supported Python version for your OS.
- For portable Python installs, set `LYCO_PYTHON` and `LYCO_VENV` in `.env`.
- WSL/Docker security checks are available (see `TOOLING.md`).

Windows:
- `lyco` is installed into the Python Scripts directory. If it is not found, add
  your Python Scripts folder (for example, `%USERPROFILE%\\AppData\\Local\\Programs\\Python\\Python3x\\Scripts`)
  to `PATH`.
- Anti-virus or SmartScreen may prompt on first run of a newly built binary.
- `semgrep` is not supported on native Windows; use WSL or run semgrep in CI.
Optional helpers: `powershell tools/run_semgrep_wsl.ps1`, `powershell tools/run_semgrep_docker.ps1`.

macOS:
- Gatekeeper may block first run of a downloaded binary. If prompted, allow it in
  System Settings > Privacy & Security.
- If you use Homebrew Python, ensure the `pip` you call matches that Python.

Linux:
- PyQt5 requires system GUI libraries. On minimal distros you may need to install
  Qt and X11/Wayland packages before running `lyco gui`.
- Use `lyco compose` for headless servers or containers.

## Packaging And Distribution

Build a compiled binary (Nuitka) and bundle it into wheels:

```powershell
python -m pip install .[build]
python tools/build_binary.py
python -m build
```

Note: Nuitka does not support the Windows Store Python distribution. Use Python from python.org for binary builds on Windows.

Build multi-platform wheels with `cibuildwheel`:

```powershell
python -m pip install .[build]
cibuildwheel --output-dir dist
```

Upload to PyPI:

```powershell
python -m pip install .[build]
twine upload dist/*
```

## Testing

Suggested manual smoke tests:

```powershell
lyco --help
lyco compose -c layout.yml -o wallpaper.png
lyco gui -c layout.yml
```

### Unit Tests

Run the unit test suite:

```powershell
python -m unittest discover -s tests
```

CI is configured for GitHub Actions and GitLab CI (`.github/workflows/ci.yml`, `.gitlab-ci.yml`).
VS Code tasks are available in `.vscode/tasks.json` for run, build, test, and CI checks.

Test documentation lives in `tests/README.md`.

Local CI/CD test run:

```powershell
$env:RUN_LOCAL_CI="1"
python -m unittest tests.test_ci_local
```

Core suite:

```powershell
python -m unittest tests.test_suite_core
```

Full suite:

```powershell
python -m unittest tests.test_suite_full
```

Post CI/CD remediation report:

```powershell
python tools/post_ci_cd_report.py
python tools/sbom_inspect.py
```

Tooling flags and cache behavior are documented in `TOOLING.md`.

### Task Runner (Cross-Platform)

The repo includes a cross-platform task runner used by the Makefile:

```powershell
python tools/run_task.py ci-fast
python tools/run_task.py ci-full
python tools/run_task.py test-core
python tools/run_task.py test-full
```

Python environment:
- `.python-version` for Python 3.12
- `.env.example` for tooling flags
- `requirements.lock` for full pinned dependency snapshot
- `.vscode/settings.json` for interpreter and env file

UI testing guidance: `tools/ui_testing.md`.

Makefile targets:
- `make setup-env`, `make venv`
- `make ci-fast`, `make ci-full`
- `make test-core`, `make test-full`
- `make sbom-if-needed`, `make ci-guard`, `make ci-record`
- `make requirements-lock`
- `make wsl-check`, `make wsl-security`
- `make docker-check`, `make docker-security`
- `make wsl-ci`, `make docker-ci`
- WSL Docker Compose: `scripts/wsl_install_docker.sh`, then `scripts/wsl_run_compose.sh ci` or `scripts/wsl_run_compose.sh security`
- WSL Make targets: `make wsl-docker-install`, `make wsl-compose-ci`, `make wsl-compose-security`

Windows note: `make` may not be installed by default; use VS Code tasks or direct
Python commands if needed.
