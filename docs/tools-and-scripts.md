# Tools And Scripts Guide

This guide summarizes the scripts under `tools/` and related automation files.

## Core Tooling
- `tools/run_task.py`: cross-platform task runner for CI/Makefile tasks.
- `tools/setup_env.py`: generate/update `.env` with OS/CI defaults.
- `tools/clean_artifacts.py`: remove build/test artifacts.
- `tools/ci_guard.py`: prevent too-frequent full CI runs unless overridden.
- `tools/ci_record.py`: write CI run artifact metadata to `build/ci/last_run.json`.

## Security And SBOM
- `tools/check_vulnerabilities.py`: Safety scan wrapper (gated by `RUN_SAFETY` and `SAFETY_API_KEY`).
- `tools/check_audit.py`: pip-audit wrapper.
- `tools/security_checks.py`: combined bandit/pip-audit/safety/semgrep.
- `tools/generate_sbom.py`: generate CycloneDX SBOM from requirements.
- `tools/should_run_sbom.py`: skip SBOM regeneration if requirements unchanged.
- `tools/sbom_inspect.py`: dump SBOM components for inspection.
- `tools/check_secrets.py`: local secrets scan across worktree and staged diffs.

## CI Helpers
- `tools/run_ci_wsl.py`: run CI inside WSL.
- `tools/run_security_wsl.py`: run security checks inside WSL.
- `tools/run_ci_docker.py`: run CI inside Docker.
- `tools/run_security_docker.py`: run security checks inside Docker.
- `tools/docker_probe.py`: check Docker availability.
- `tools/wsl_probe.py`: check WSL availability.
- `tools/wsl_utils.py`: WSL detection utilities.
- `tools/run_wsl_docker.py`: Windows bridge to WSL docker install/compose scripts.

## Build
- `tools/build_binary.py`: build a compiled binary with Nuitka and bundle it into the package.

## Reports
- `tools/post_ci_cd_report.py`: generate a remediation report after CI/CD findings.
- `tools/ui_testing.md`: notes on GUI testing approaches.

## Supporting Files
- `Makefile`: common targets for CI and dev workflows.
- `.github/workflows/ci.yml`: GitHub Actions CI pipeline.
- `.gitlab-ci.yml`: GitLab CI pipeline.
- `docker-compose.yml`: Docker compose services for CI/security.
- `scripts/wsl_install_docker.sh`: install Docker inside WSL.
- `scripts/wsl_run_compose.sh`: run docker-compose tasks inside WSL.

## Environment Flags
See `TOOLING.md` for all flags, defaults, and cache behavior.
