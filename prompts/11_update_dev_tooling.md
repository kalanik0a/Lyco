# Step 11: Update Dev Tooling And Workspace Configs

Update developer workflow files to reflect current project structure and commands:

- `.vscode/tasks.json`: ensure run, build, test, and CI tasks are accurate.
- `.vscode/launch.json`: ensure debug configs reflect current entry points and args.
- `.vscode/*.code-workspace` (if present): update folders/settings to match repo.
- `.gitlab-ci.yml`: keep CI steps aligned with tooling scripts and requirements files.
- `.github/workflows/ci.yml`: keep GitHub Actions aligned with the same checks.
- `TOOLING.md`, `.env.example`, `.python-version`, `requirements.lock`: keep tooling and caches aligned.
- `Makefile`: ensure targets match tooling scripts and cache guard steps.
- `TOOLING.md`: keep flags and cache logic accurate.
- `tools/run_task.py` and `tools/setup_env.py`: ensure task runner and env setup stay aligned with CI/Makefile.
- `src/lyco/app_config.json`: ensure framework swap configuration stays in sync with docs.
- Docs and state: update `README.md`, `DOCS.md`, `CONTEXT.md`, and `STATE.json` if any paths or commands change.

Confirm tasks still match actual scripts:
- `tools/check_pylint.py`
- `tools/check_vulnerabilities.py`
- `tools/check_audit.py`
- `tools/security_checks.py`
- `tools/generate_sbom.py`
- `python -m unittest discover -s tests`

