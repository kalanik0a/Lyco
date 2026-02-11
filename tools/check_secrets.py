from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PATTERNS = [
    # Private keys
    r"-----BEGIN (RSA|EC|DSA|OPENSSH|PGP) PRIVATE KEY-----",
    # AWS
    r"AKIA[0-9A-Z]{16}",
    r"ASIA[0-9A-Z]{16}",
    # GitHub token
    r"ghp_[A-Za-z0-9]{36,}",
    r"gho_[A-Za-z0-9]{36,}",
    r"ghu_[A-Za-z0-9]{36,}",
    r"ghs_[A-Za-z0-9]{36,}",
    r"ghr_[A-Za-z0-9]{36,}",
    # Slack tokens
    r"xox[baprs]-[A-Za-z0-9-]{10,48}",
    # Google API key
    r"AIza[0-9A-Za-z\-_]{35}",
    # Generic JWT
    r"eyJ[a-zA-Z0-9_\-]+=*\.[a-zA-Z0-9_\-]+=*\.[a-zA-Z0-9_\-+=/]*",
    # Common secret env var names
    r"(AWS|GCP|GOOGLE|AZURE|OPENAI|SLACK|DISCORD|TOKEN|SECRET|PASSWORD|API_KEY)[A-Z0-9_]*\s*=\s*['\"][^'\"]{8,}['\"]",
]

EXCLUDES = {
    ".git",
    ".venv",
    "venv",
    "build",
    "dist",
    "sbom",
    "__pycache__",
}


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def _iter_files() -> list[Path]:
    files = []
    for path in ROOT.rglob("*"):
        if path.is_dir():
            if path.name in EXCLUDES:
                continue
            continue
        if any(part in EXCLUDES for part in path.parts):
            continue
        files.append(path)
    return files


def _scan_text(text: str) -> list[str]:
    hits = []
    for pattern in PATTERNS:
        if re.search(pattern, text):
            hits.append(pattern)
    return hits


def _read_text_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def scan_worktree() -> int:
    issues = []
    for path in _iter_files():
        content = _read_text_safe(path)
        if not content:
            continue
        hits = _scan_text(content)
        if hits:
            issues.append((path, hits))
    if issues:
        print("Potential secrets found in worktree:")
        for path, hits in issues:
            print(f"- {path}: {', '.join(hits)}")
        return 1
    return 0


def scan_git_changes() -> int:
    result = _run(["git", "diff", "--cached"])
    if result.returncode != 0:
        print("git diff --cached failed; falling back to working tree scan only.")
        return 0
    hits = _scan_text(result.stdout)
    if hits:
        print("Potential secrets found in staged changes:")
        for pattern in hits:
            print(f"- {pattern}")
        return 1
    return 0


def scan_with_rg() -> int:
    rg = shutil.which("rg")
    if rg is None:
        return 0
    args = [
        "rg",
        "--hidden",
        "--no-ignore",
        "--pcre2",
        "--glob",
        "!.git/**",
        "--glob",
        "!.venv/**",
        "--glob",
        "!venv/**",
        "--glob",
        "!build/**",
        "--glob",
        "!dist/**",
        "--glob",
        "!sbom/**",
        "--glob",
        "!__pycache__/**",
    ]
    for pattern in PATTERNS:
        proc = _run(args + [pattern, str(ROOT)])
        if proc.stdout.strip():
            print(proc.stdout)
            return 1
    return 0


def main() -> int:
    code = 0
    if os.environ.get("RUN_SECRET_SCAN") in ("0", "false", "False"):
        print("Secrets scan skipped (set RUN_SECRET_SCAN=1 to enable).")
        return 0
    code |= scan_worktree()
    code |= scan_git_changes()
    code |= scan_with_rg()
    if code == 0:
        print("No obvious secrets found.")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
