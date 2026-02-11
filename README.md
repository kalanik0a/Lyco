# Lyco Python Framework

Lyco Python Framework is a boilerplate for building Python desktop tools. It provides a runnable example app (image mosaic) plus a full stack of tooling: CI, security scans, task runner, docs, and AI-assisted maintenance prompts.

## Docs

Documentation lives in `docs/`. Start here:

Docs tree (links):
- `docs/` (folder)
- [docs/README.md](docs/README.md)
- [docs/boilerplate.md](docs/boilerplate.md)
- [docs/usage.md](docs/usage.md)
- [docs/extension.md](docs/extension.md)
- [docs/ai-assistance.md](docs/ai-assistance.md)
- [docs/ai-assistance-customization.md](docs/ai-assistance-customization.md)
- [docs/tools-and-scripts.md](docs/tools-and-scripts.md)

Docs for tooling and AI-assistance live under `docs/`:
- Tooling: `docs/tools-and-scripts.md`
- AI assistance: `docs/ai-assistance.md`, `docs/ai-assistance-customization.md`

## Use As Boilerplate
1. Update `pyproject.toml` (name, description, scripts, dependencies).
2. Replace the example app under `src/lyco/` with your own package.
3. Update `src/lyco/app_config.json` to point at your module/callable.
4. Update `README.md`, `DOCS.md`, `CONTEXT.md`, and `AGENT.md`.
5. Keep the tooling, CI, and security scaffolding as your foundation.

See `docs/boilerplate.md` and `docs/ai-assistance-customization.md` for the guided workflow.

## Quick Start
1. Generate `.env` defaults: `python tools/setup_env.py`.
2. Install runtime deps: `python -m pip install -r requirements.txt`.
3. Run the example app: `python Lyco.py --help`.
4. Run tests: `python -m unittest discover -s tests`.

## Example App (Image Mosaic)
The bundled Hello-world app composes a transparent wallpaper from a YAML layout file and includes a PyQt GUI editor.

Example YAML:

```yaml
output: wallpaper.png
canvas_width: 7680
canvas_height: 2160
items:
  - file: "img1.png"
    x: 0
    y: 0
    resolution: "1920x1080"
  - file: "img2.jpg"
    x: 1920
    y: 0
    resolution: "2560x1440"
```

## CLI Usage

```powershell
lyco compose -c layout.yml -o wallpaper.png
lyco gui -c layout.yml
```

Repo wrapper (no install):

```powershell
python Lyco.py compose -c layout.yml -o wallpaper.png
python Lyco.py gui -c layout.yml
```

Module invocation:

```powershell
python -m lyco --help
```

## Install
Target Python version: 3.12 (see `.python-version`).

```powershell
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

Editable install:

```powershell
python -m pip install -e .
```

Optional semgrep tools:

```powershell
python -m pip install -r requirements-semgrep.txt
```

## Tests

```powershell
python -m unittest discover -s tests
```

CI is configured for GitHub Actions and GitLab CI (`.github/workflows/ci.yml`, `.gitlab-ci.yml`).

## Build Notes

```powershell
python -m pip install .[build]
python tools/build_binary.py
python -m build
```

Nuitka does not support the Windows Store Python distribution. Use Python from python.org for binary builds on Windows.

## License
GNU General Public License v3.0. See `LICENSE`.
