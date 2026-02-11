# TODO

## Security Tooling
- Revisit Bandit suppression (`B404`, `B603`) and narrow scope if feasible.
  - Caveat: Most subprocess usage is in tooling wrappers; consider `# nosec` on specific lines instead of global skips.
- Evaluate `safety scan` non-interactive configuration if authentication becomes required.
  - Caveat: Requires a Safety account; policy file in `.safety-policy.yml` is prepared.

## CI/CD Hygiene
- Add `sbom/` handling to CI artifacts to avoid accidental commits.
- Decide whether SBOM should include dev dependencies or remain runtime-only.
 - Validate `tools/setup_env.py` defaults for each OS and CI provider.

## Build Caveats
- Nuitka is not supported with Windows Store Python; use python.org distribution for binary builds.
- Module invocation from the repo requires install or `PYTHONPATH=src`.

## Tooling
- Consider adding `pytest-qt` if GUI automation is required (see `tools/ui_testing.md`).
- Review whether Makefile targets should be mirrored in VS Code tasks.
 - Decide whether `tools/run_task.py` should fully replace direct VS Code task calls.
