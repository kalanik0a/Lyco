# AI-Assistance Customization Guide

This guide walks you through tailoring the AI-assistance files to your own project after you fork this repo.

## Goal
Align the AI-assisted workflows with your project name, entry points, tooling, and CI/CD pipeline so automated guidance stays accurate.

## Step 0: Identify Your New App
Decide the new package name, entry points, and scripts:
- Package path under `src/`
- CLI entry point callable
- Primary commands users should run

Write those down first. You will reference them in multiple files.

## Step 1: Update `CONTEXT.md`
Edit:
- Purpose section: describe the new product/app.
- How To Run: list the new command and module paths.
- Primary Files: point to your new package and key tools.
- Packaging And Release: update dependencies, scripts, and packaging notes.
- Docs Map: include any new docs.

Keep `CONTEXT.md` short and current. It is the project map for humans and tools.

## Step 2: Update `STATE.json`
Edit the machine-readable map:
- Paths to entry points and tools.
- Canonical commands for lint, tests, security, and SBOM.
- Any decisions or constraints that affect automation.

Keep `STATE.json` valid JSON. Avoid comments or trailing commas.

## Step 3: Update `AGENT.md`
Condense the changes into a runnable guide:
- Update core commands and key files.
- Remove references to the old example app.
- Add new caveats or platform constraints.

## Step 4: Update `prompts/`
The prompts are CI/CD steps for maintenance. Update them when workflows change:
- If you add new checks, add a prompt and include it in `prompts/CI_CD_TASKS.md`.
- If you remove a check, remove or update the prompt.

## Step 5: Update `TASKS.md` And `TODO.md`
- Replace roadmap tasks with your project goals.
- Add risks, open questions, or technical debt in `TODO.md`.

## Step 6: Update Tooling Docs
If you changed tooling, update:
- `TOOLING.md`: flags, cache behavior, guard logic.
- `docs/tools-and-scripts.md`: script descriptions.
- `docs/usage.md`: updated commands.

## Step 7: Validate
Run the normal checks to ensure the guidance matches reality:
- `python tools/check_pylint.py`
- `python tools/check_audit.py`
- `python tools/security_checks.py`
- `python tools/generate_sbom.py`
- `python -m unittest discover -s tests`

## Common Pitfalls
- Updating `README.md` but forgetting `CONTEXT.md`.
- Renaming packages without updating `app_config.json` or `pyproject.toml`.
- Adding new tools without wiring them into `tools/run_task.py` and `Makefile`.
- Leaving old example app references in prompts and docs.

## Minimal Change Checklist
- `pyproject.toml` updated for name, scripts, and dependencies.
- `src/<your_package>/` created and referenced in `app_config.json`.
- `CONTEXT.md`, `STATE.json`, `AGENT.md` updated.
- `prompts/CI_CD_TASKS.md` updated if CI/CD steps changed.
- `TOOLING.md` and `docs/tools-and-scripts.md` updated if tooling changed.
