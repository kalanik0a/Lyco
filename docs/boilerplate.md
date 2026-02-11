# Using This Repo As Boilerplate

This repository is designed to be a reusable starter for Python desktop tools. The current app (image mosaic) is a Hello-world example that you can replace with your own implementation while keeping the tooling, CI, and security scaffolding.

## Minimal Fork Steps
1. Run `python tools/setup_env.py` to generate `.env` for your OS/CI.
2. Update `pyproject.toml`:
   - `project.name`, `project.description`, `project.scripts`.
   - Optional: add authors, classifiers, URLs.
3. Replace the example app:
   - Create your package under `src/`.
   - Update `src/lyco/app_config.json` to point at your module.
   - Update `src/lyco/launcher.py` if you rename the package.
4. Update docs:
   - `README.md` and `DOCS.md` for your new app.
   - `CONTEXT.md` and `AGENT.md` for project-specific context.
5. Run the tests and CI checks before publishing.

## What To Keep
- `tools/`: task runner, security checks, SBOM generation, CI guard.
- `.github/` and `.gitlab-ci.yml`: CI workflows.
- `Makefile`: consistent local targets.
- `prompts/`: CI/CD checklist and prompts for maintenance.
- `tests/`: core test suite patterns (replace or extend as needed).

## What To Customize
- `src/lyco/cli.py`: replace with your CLI/GUI implementation.
- `src/lyco/app_config.json`: point to your module/callable.
- `requirements.txt`: runtime dependencies for your app.
- `requirements-dev.txt`: dev/security tools for your team.
- `LICENSE`: confirm licensing for your distribution.

## App Config Swap
The launcher checks `src/lyco/app_config.json` and an optional env var:
- `LYCO_APP_CONFIG=/path/to/app_config.json`

This allows a fork to update one JSON file to swap the app module without reworking the launcher.

## Packaging Notes
- The `lyco` script is defined in `pyproject.toml`.
- The compiled binary (if built) is bundled under `src/lyco/bin/`.
- Wheels can be built via `cibuildwheel` and `tools/build_binary.py`.

