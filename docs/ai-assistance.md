# AI-Assistance Files

This repo includes a set of AI-assistance files that describe how to maintain and operate the project. They are designed for human and AI tooling to follow the same playbooks.

## Files And Purpose
- `AGENT.md`: consolidated operational guide (key files, commands, caveats, roadmap).
- `CONTEXT.md`: product and repository summary (purpose, entry points, docs map).
- `STATE.json`: machine-readable state (paths, commands, decisions, roadmap alignment).
- `TASKS.md`: phased product/engineering roadmap.
- `TODO.md`: current follow-ups and caveats.
- `prompts/CI_CD_TASKS.md`: master checklist for CI/CD workflows.
- `prompts/01_check_comments.md`: review code comment clarity.
- `prompts/02_check_pylint.md`: run lint checks and address issues.
- `prompts/03_check_vulnerabilities.md`: run vulnerability scans.
- `prompts/04_check_sbom.md`: generate and review SBOM.
- `prompts/05_check_tests.md`: check test coverage and relevance.
- `prompts/06_run_tests.md`: execute tests.
- `prompts/07_validate_tests.md`: validate tests vs. docs/expected behavior.
- `prompts/08_update_versions.md`: confirm versioning changes.
- `prompts/09_update_package_info.md`: validate packaging metadata and docs.
- `prompts/10_update_project_state.md`: update context/state/task tracking.
- `prompts/11_update_dev_tooling.md`: verify tooling config and CI scripts.
- `prompts/12_check_secrets.md`: run secrets scan and spot-check diffs.
- `prompts/13_integration_audit.md`: full integration/config audit.
- `prompts/POST_CI_CD_TASKS.md`: remediation workflow after CI/CD findings.

## How They Work Together
1. `CONTEXT.md` and `STATE.json` define the project map.
2. `AGENT.md` condenses the map into a runnable guide.
3. `prompts/` provide a step-by-step CI/CD checklist.
4. `TASKS.md` and `TODO.md` capture long-term roadmap and short-term follow-ups.

## When To Update
- After adding new tools, scripts, or workflows, update `AGENT.md`, `CONTEXT.md`, and `STATE.json`.
- When new CI/CD checks are added, update the relevant prompts and `prompts/CI_CD_TASKS.md`.

## How To Modify AI-Assistance Data
These files are intentionally simple so they can be edited by hand and reviewed in diffs.

Guidelines:
- Keep entries concise and action-oriented.
- Prefer paths relative to repo root (for example, `tools/run_task.py`).
- Avoid duplicating long instructions across multiple files; link to the canonical doc.
- Update cross-references when paths or names change.

Recommended edit order when the project changes:
1. Update `CONTEXT.md` to reflect the new purpose, entry points, and docs map.
2. Update `STATE.json` with paths, commands, and decisions (keep it machine-readable).
3. Update `AGENT.md` with the condensed guide and key commands.
4. Update `prompts/` and `prompts/CI_CD_TASKS.md` for CI/CD changes.
5. Update `TASKS.md` and `TODO.md` for roadmap and follow-ups.

See `docs/ai-assistance-customization.md` for a step-by-step walkthrough.
