# Tooling Context

This document defines optional runtime flags, caching behavior, and local tooling conventions.

## Environment Flags

- `LYCO_OS=auto`: set explicit OS mode (`windows`, `macos`, `linux`) or auto-detect.
- `LYCO_CI_PROVIDER=auto`: set CI provider (`github`, `gitlab`, `none`) or auto-detect.
- `LYCO_PYTHON=`: optional path to a portable Python executable.
- `LYCO_VENV=.venv`: path to the virtual environment directory.
- `RUN_SAFETY=1`: enable `safety scan` in non-interactive environments.
- `RUN_SBOM=1`: force SBOM regeneration even if cached.
- `RUN_BANDIT=1`: force Bandit run (normally enabled).
- `RUN_SEMGREP=1`: force Semgrep run on supported platforms.
- `RUN_SECRET_SCAN=1`: force secrets scan (normally enabled).
- `RUN_LOCAL_CI=1`: enable local CI tests (`tests/test_ci_local.py`).
- `CI_GUARD_DAYS=1`: minimum days between full CI runs.
- `CI_GUARD_ALLOW=1`: bypass CI guard prompt.
- `SAFETY_API_KEY=...`: required for `safety scan` in CI.
- `WSL_DISTRO=Ubuntu`: preferred WSL distro for security checks.
- `DOCKER_IMAGE=python:3.12`: Docker image used for containerized security checks.

## Semgrep Install Note

`semgrep` is pinned in `requirements-semgrep.txt` to avoid dependency conflicts with `pip-audit`.
Install it separately when you need semgrep scans.

## Cache-Heavy Steps

SBOM generation is skipped if the requirements hash has not changed since the last full run.
Use `RUN_SBOM=1` to force regeneration.

## CI Guard

`tools/ci_guard.py` checks the last full run time in `build/ci/last_run.json`.  
Set `CI_GUARD_ALLOW=1` to bypass the guard for a full run.

## Test Suites

- **Core suite**: fast unit tests, excludes E2E and local CI checks.
- **Full suite**: all tests, including E2E/local CI (when enabled).

## Artifacts

Local CI artifact: `build/ci/last_run.json`  
Includes last run time, SBOM hash, and high-level results for guard prompts.

## Environment Setup

Use `python tools/setup_env.py` to generate or update `.env` after cloning.
The script auto-detects OS/CI and sets defaults for semgrep and venv paths.
The task runner (`python tools/run_task.py`) loads `.env` automatically.

## WSL And Docker Security Checks

- `make wsl-check` / `python tools/wsl_probe.py`: validate WSL + distro availability.
- `make wsl-security` / `python tools/run_security_wsl.py`: run security checks inside WSL.
- `make wsl-ci` / `python tools/run_ci_wsl.py`: run the full CI suite inside WSL.
- `make docker-check` / `python tools/docker_probe.py`: validate Docker availability.
- `make docker-security` / `python tools/run_security_docker.py`: run security checks inside Docker.
- `make docker-ci` / `python tools/run_ci_docker.py`: run the full CI suite inside Docker.

## WSL Docker Compose

From inside a WSL distro:
- Install Docker: `scripts/wsl_install_docker.sh`
- Run CI service: `scripts/wsl_run_compose.sh ci`
- Run security service: `scripts/wsl_run_compose.sh security`

From Windows (WSL bridge):
- `make wsl-docker-install`
- `make wsl-compose-ci`
- `make wsl-compose-security`

## Makefile Notes (Windows)

`make` may not be installed by default on Windows. Use the VS Code tasks or run
the Python tooling scripts directly if `make` is unavailable.
