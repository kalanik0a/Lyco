# Usage Guide

This repo supports multiple ways to run the app. All entry points funnel to the same CLI logic.

## Entry Points
- Installed command: `lyco`
- Module: `python -m lyco`
- Repo wrapper: `python Lyco.py`

## Common Commands
- Show help: `lyco --help`
- Compose a mosaic: `lyco compose -c layout.yml -o wallpaper.png`
- Open GUI: `lyco gui -c layout.yml`

## Running From The Repo
Without installing, use the wrapper or module:
- `python Lyco.py --help`
- `python -m lyco --help` (set `PYTHONPATH=src`)

## Environment Setup
- Generate `.env`: `python tools/setup_env.py`
- Install deps: `python -m pip install -r requirements.txt`
- Install dev tools: `python -m pip install -r requirements-dev.txt`

## Testing
- Run all tests: `python -m unittest discover -s tests`
- Core suite: `python -m unittest tests.test_suite_core`
- Full suite: `python -m unittest tests.test_suite_full`

## CI Shortcuts
- `python tools/run_task.py ci-fast`
- `python tools/run_task.py ci-full`

## Known Caveats
- GUI requires a display server (X11/Wayland on Linux).
- `semgrep` is not supported on native Windows; use WSL or CI.

