# Test Suite Documentation

This directory contains native `unittest` tests for Lyco Python Framework.

## Test Modules

- `test_cli.py`: CLI helpers, YAML parsing, and compose workflow.
- `test_launcher.py`: Binary-first launcher fallback behavior.
- `test_docs.py`: Documentation smoke tests for README/DOCS.
- `test_e2e.py`: End-to-end invocation and compile checks (skips when unsupported).
- `test_ci_local.py`: Local CI/CD checks (set `RUN_LOCAL_CI=1` to enable).
- `test_suite_core.py`: Core suite runner (fast).
- `test_suite_full.py`: Full suite runner.

## Running Tests

```powershell
python -m unittest discover -s tests
```

Local CI/CD test run:

```powershell
$env:RUN_LOCAL_CI="1"
python -m unittest tests.test_ci_local
```

Core suite:

```powershell
python -m unittest tests.test_suite_core
```

Full suite:

```powershell
python -m unittest tests.test_suite_full
```

Make targets:

```powershell
make test-core
make test-full
```

Cross-platform task runner:

```powershell
python tools/run_task.py test-core
python tools/run_task.py test-full
```

## Test Data

Tests generate temporary YAML files and images at runtime using `tempfile` and `Pillow`.
