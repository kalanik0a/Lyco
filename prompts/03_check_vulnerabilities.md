# Step 3: Check For Code Vulnerabilities

Use `CONTEXT.md` and `STATE.json` to understand dependencies and tooling. Run security checks:
- `python tools/check_vulnerabilities.py`
- `python tools/check_audit.py`
- `python tools/security_checks.py` (if needed for combined results)

Investigate high-severity findings first. If a fix requires a dependency update, confirm the target version and note any compatibility risks (especially for PyQt5, Pillow, PyYAML).
