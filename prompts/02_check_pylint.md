# Step 2: Check For Pylint Problems

Use `STATE.json` to locate the lint config and entry points. Run `python tools/check_pylint.py` and review output for actionable issues, especially in `src/lyco_image_mosaic/cli.py`. Fix only meaningful problems (bugs, correctness, maintainability). Avoid cosmetic-only refactors unless they reduce risk or clarify intent.
