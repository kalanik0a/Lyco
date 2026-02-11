# Product Tasks (CTO/CISO/CSO/CFO + PM)

This list captures what executive stakeholders typically need to see to advance this project from a repo to a product. It is ordered by a practical implementation sequence, and each phase intermixes CTO/CISO/CSO/CFO priorities with PM execution tasks.

## Phase 0: Product Definition

- Define target users and primary use cases (desktop creator vs. automation-first CLI).
- Decide product scope and platform support matrix (Windows/macOS/Linux, Python versions).
- Clarify licensing implications (GPL v3) and commercial viability.
- Establish success metrics and adoption goals (activation, task completion, retention).
- Define pricing model and distribution strategy (free, paid tiers, enterprise).
- Define a clone/fork onboarding flow for teams starting new apps from the framework.

## Phase 1: Packaging, Metadata, And Release Readiness

- Add full package metadata (authors, maintainers, keywords, classifiers, URLs).
- Ensure license metadata uses `license = {file = "LICENSE"}` and include in sdists.
- Add `MANIFEST.in` for any non-code files needed in source distributions.
- Standardize versioning policy and add `CHANGELOG.md`.
- Establish release checklist and version/tag strategy for PyPI publishing.

## Phase 2: Quality Gates And Local Dev Experience

- Add formatter and linter (e.g., `ruff` + `ruff format` or `black` + `ruff`).
- Add type checking (e.g., `mypy` or `pyright`) with baseline config.
- Add `pre-commit` hooks to enforce lint/format/type on commit.
- Define quality gates for PRs (lint, type, tests, docs).
- Define tooling flags, cache behavior, and local CI guard (see `TOOLING.md`).
- Keep VS Code and Makefile tooling in sync (`.vscode/`, `Makefile`).
- Provide an OS-aware environment bootstrap script for new clones (writes `.env`).

## Phase 3: Testing And Validation

- Expand unit test coverage (core logic, YAML parsing, compose output).
- Add tests for GUI/editor behaviors (snap, save normalization), launcher app config loading, and YAML edge cases.
- Separate GUI smoke tests from core tests and document headless strategy.
- Add `coverage.py` and set a minimum coverage threshold.
- Add `tox` or `nox` to standardize test runs across Python versions.

## Phase 4: CI/CD And Distribution

- Add CI to run tests on Windows/macOS/Linux. (Started: GitHub Actions + GitLab CI)
- Add automated builds for wheels and sdists, including compiled binaries.
- Add artifact signing and verification policy for published releases.
- Automate PyPI publishing on tags or approved releases.

## Phase 5: Security And Supply Chain

- Run dependency risk review (PyQt5, Pillow, PyYAML, build tooling).
- Add SBOM generation for releases.
- Add vulnerability scanning (`pip-audit` or equivalent).
- Define a security policy (`SECURITY.md`) and disclosure process.

## Phase 6: Documentation And Support

- Create onboarding flow and quick-start docs.
- Add `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`.
- Add troubleshooting guides by OS and common errors.
- Establish support channels, SLAs, and feedback loop.
- Create example layouts and sample assets for fast adoption.

## Phase 7: Productization And GTM

- Create product page and demo video.
- Define support and maintenance plan for paid tiers.
- Set up post-release monitoring (support tickets, crash reports).

## Ongoing Executive Review Checklist

- CTO: architecture roadmap, build/release readiness, quality gates.
- CISO: security posture, SBOM, dependency risk, disclosure policy.
- CSO: onboarding, support readiness, customer feedback loops.
- CFO: cost model, revenue strategy, licensing impact.
