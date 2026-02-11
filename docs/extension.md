# Extension Guide

This guide explains how to extend or repurpose the framework beyond the example app.

## Replace The App Module
1. Create a new package under `src/`.
2. Provide a callable entry point (for example, `main`).
3. Update `src/lyco/app_config.json`:
   - `module`: your module path
   - `callable`: your entry function name

The launcher (`src/lyco/launcher.py`) will import and invoke that callable at runtime.

## Add New Commands
If you keep the CLI structure:
- Add new subcommands in your CLI module.
- Update tests in `tests/` to cover new behavior.
- Update `README.md` and `DOCS.md` with new usage.

## Add New Tools
- Add scripts under `tools/` for new workflows.
- Register them in `tools/run_task.py` and `Makefile` if they should be part of CI.
- Document them in `docs/tools-and-scripts.md`.

## Add New CI Checks
- Update `.github/workflows/ci.yml` and `.gitlab-ci.yml` to include the checks.
- If the check is optional, gate it with an env flag and document the flag in `TOOLING.md`.

## Add New Tests
- Use `unittest` under `tests/`.
- Include new modules in `tests/test_suite_core.py` or `tests/test_suite_full.py`.
- If a test is optional or environment-dependent, gate it with an env flag.

## Build And Packaging Extensions
- Update `pyproject.toml` for new dependencies or scripts.
- Keep compiled artifacts under `src/<package>/bin/` if you bundle binaries.

