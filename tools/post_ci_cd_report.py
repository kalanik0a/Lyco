from __future__ import annotations

import json
import subprocess
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "build" / "vulns"


def _run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return result.stdout + ("\n" + result.stderr if result.stderr else "")


def _read_sbom() -> str:
    sbom = ROOT / "sbom" / "sbom.json"
    if not sbom.exists():
        return "SBOM not found. Run: python tools/generate_sbom.py"
    try:
        data = json.loads(sbom.read_text(encoding="utf-8"))
        components = data.get("components", [])
        lines = [f"- Components: {len(components)}"]
        for comp in components[:20]:
            name = comp.get("name", "unknown")
            version = comp.get("version", "unknown")
            lines.append(f"  - {name}=={version}")
        if len(components) > 20:
            lines.append("  - ...")
        return "\n".join(lines)
    except Exception as exc:
        return f"Failed to parse SBOM: {exc}"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = OUT_DIR / f"report-{date.today().isoformat()}.md"

    sections = [
        "# Post CI/CD Security Report",
        "",
        f"Date: {date.today().isoformat()}",
        "",
        "## Findings Summary",
        "- TODO: Summarize CVE/CWE/CPE or secret findings.",
        "",
        "## Tool Outputs (Raw)",
        "### pip-audit",
        "```",
        _run(["python", "tools/check_audit.py"]),
        "```",
        "",
        "### safety scan (optional)",
        "```",
        _run(["python", "tools/check_vulnerabilities.py"]),
        "```",
        "",
        "### bandit/semgrep",
        "```",
        _run(["python", "tools/security_checks.py"]),
        "```",
        "",
        "### secrets scan",
        "```",
        _run(["python", "tools/check_secrets.py"]),
        "```",
        "",
        "## SBOM Summary",
        _read_sbom(),
        "",
        "## Threat Modeling Notes",
        "- Dev (interpreted): TODO",
        "- Dev (compiled): TODO",
        "- Prod (interpreted): TODO",
        "- Prod (compiled): TODO",
        "",
        "## Remediation Plan",
        "- TODO: Describe fixes and where they land.",
        "",
        "## CI/CD Resolution",
        "- TODO: Re-run failing checks and record outcomes.",
    ]

    report.write_text("\n".join(sections) + "\n", encoding="utf-8")
    print(f"Wrote {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
