# Step 13: Integration And Configuration Audit (Whole Repo)

Perform a holistic audit of the repository to ensure every integration and configuration path is correct, consistent, and transplant-ready. Use `CONTEXT.md` and `STATE.json` as the canonical map.

## 1. Repository Integrity
- Check for committed build artifacts or cache files (`build/`, `dist/`, `*.egg-info`, `sbom/`).
- Verify `.gitignore` covers editor noise, venvs, caches, secrets, and SBOM outputs.
- Confirm no accidental binaries or credentials are tracked.

## 2. Packaging + Entry Points
- `pyproject.toml`: name, version, description, dependencies, scripts, package-data.
- `src/lyco_image_mosaic/launcher.py`: compiled-first logic and fallback behavior.
- `src/lyco_image_mosaic/app_config.json`: module/callable swap for framework forks.
- Ensure `README.md`/`DOCS.md` align with package metadata and install commands.

## 3. Tooling + Environment
- `tools/run_task.py`: matches Makefile targets and respects `.env`.
- `tools/setup_env.py` + `.env.example`: flags and defaults are consistent.
- `.python-version`, `requirements.txt`, `requirements-dev.txt`, `requirements.lock`: pinned and consistent.
- `TOOLING.md`: documents cache behavior, guard, and flags.

## 4. CI/CD Integrations
- `.github/workflows/ci.yml`: uses Python 3.12 and correct commands.
- `.gitlab-ci.yml`: uses same checks, env flags, and artifacts.
- Verify SBOM artifact paths and secret scanning behavior.

## 5. VS Code + Workspace Integrations
- `.vscode/tasks.json`: run/build/test/CI tasks align with scripts.
- `.vscode/launch.json`: debug configs map to current entry points.
- `.vscode/settings.json`: interpreter/env config is correct for target OS.

## 6. Tests + Docs
- `tests/` covers CLI, launcher, docs, E2E, local CI.
- `tests/README.md` aligns with current targets and task runner.
- `README.md`, `DOCS.md`, `CONTEXT.md`, `AGENT.md`, `TASKS.md`, `TODO.md` all match current structure and commands.

## 7. Report Findings
- If mismatches are found, note exactly which file/line and propose a fix.
- Update `STATE.json` and docs when changes are applied.
