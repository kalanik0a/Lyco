"""Cross-platform task runner for Makefile and CI workflows."""
from __future__ import annotations

import os
import platform
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env"


def load_env() -> None:
    """Load simple KEY=VALUE pairs from .env without overriding existing vars."""
    if not ENV_FILE.exists():
        return
    for raw in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key not in os.environ:
            os.environ[key] = value


def is_docker() -> bool:
    """Best-effort check for containerized execution."""
    if os.environ.get("RUNNING_IN_DOCKER") == "1":
        return True
    if Path("/.dockerenv").exists():
        return True
    cgroup = Path("/proc/1/cgroup")
    if cgroup.exists():
        content = cgroup.read_text(encoding="utf-8", errors="ignore")
        if "docker" in content or "containerd" in content:
            return True
    return False


def venv_path() -> Path:
    """Return the configured venv path."""
    return Path(os.environ.get("LYCO_VENV", ".venv"))


def venv_python() -> Path:
    """Return the venv Python path for the active platform."""
    if platform.system().lower().startswith("win"):
        return venv_path() / "Scripts" / "python.exe"
    return venv_path() / "bin" / "python"


def base_python() -> str:
    """Return the Python executable to use for bootstrapping."""
    override = os.environ.get("LYCO_PYTHON")
    if override:
        return override
    return sys.executable


def run(cmd: list[str]) -> int:
    """Run a subprocess and return the exit code."""
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd, cwd=ROOT)


def ensure_venv() -> int:
    """Ensure the venv exists, creating it if needed."""
    venv_py = venv_python()
    if venv_py.exists():
        return 0
    base = base_python()
    if os.environ.get("LYCO_PYTHON") and not Path(base).exists():
        print(f"Configured LYCO_PYTHON does not exist: {base}")
        return 2
    if is_docker():
        print("Detected container runtime. Creating a venv may not be available.")
    if run([base, "-c", "import venv"]) != 0:
        print("Python venv module not available. Install python3-venv or use a full Python build.")
        return 2
    return run([base, "-m", "venv", str(venv_path())])


def task_venv() -> int:
    """Create the virtual environment."""
    return ensure_venv()


def task_install(dev: bool = False) -> int:
    """Install requirements into the venv."""
    if ensure_venv() != 0:
        return 2
    venv_py = venv_python()
    req = "requirements-dev.txt" if dev else "requirements.txt"
    return run([str(venv_py), "-m", "pip", "install", "-r", req])


def task_requirements_lock() -> int:
    """Freeze the venv to requirements.lock."""
    if ensure_venv() != 0:
        return 2
    venv_py = venv_python()
    lock_path = ROOT / "requirements.lock"
    print(f"Writing lockfile to {lock_path}")
    with lock_path.open("w", encoding="utf-8") as handle:
        result = subprocess.run([str(venv_py), "-m", "pip", "freeze"], cwd=ROOT, stdout=handle)
    return result.returncode


def task_test(module: str) -> int:
    """Run a unittest module."""
    return run([base_python(), "-m", "unittest", module])


def task_ci_guard() -> int:
    return run([base_python(), "tools/ci_guard.py"])


def task_ci_record() -> int:
    return run([base_python(), "tools/ci_record.py"])


def main() -> int:
    load_env()
    if len(sys.argv) < 2:
        print("Usage: python tools/run_task.py <task> [args...]")
        return 2

    task = sys.argv[1]
    extra = sys.argv[2:]

    if task == "venv":
        return task_venv()
    if task == "install":
        return task_install(False)
    if task == "install-dev":
        return task_install(True)
    if task == "requirements-lock":
        return task_requirements_lock()
    if task == "test-core":
        return task_test("tests.test_suite_core")
    if task == "test-full":
        return task_test("tests.test_suite_full")
    if task == "test-one":
        if not extra:
            print("Usage: python tools/run_task.py test-one <module>")
            return 2
        return task_test(extra[0])
    if task == "pylint":
        return run([base_python(), "tools/check_pylint.py"])
    if task == "audit":
        return run([base_python(), "tools/check_audit.py"])
    if task == "safety":
        return run([base_python(), "tools/check_vulnerabilities.py"])
    if task == "security":
        return run([base_python(), "tools/security_checks.py"])
    if task == "secrets":
        return run([base_python(), "tools/check_secrets.py"])
    if task == "sbom":
        return run([base_python(), "tools/generate_sbom.py"])
    if task == "sbom-if-needed":
        code = run([base_python(), "tools/should_run_sbom.py"])
        if code != 0:
            return run([base_python(), "tools/generate_sbom.py"])
        return 0
    if task == "ci-guard":
        return task_ci_guard()
    if task == "ci-record":
        return task_ci_record()
    if task == "ci-fast":
        guard = task_ci_guard()
        if guard != 0:
            return guard
        code = 0
        code |= run([base_python(), "tools/check_pylint.py"])
        code |= run([base_python(), "tools/check_audit.py"])
        code |= task_test("tests.test_suite_core")
        return code
    if task == "ci-full":
        guard = task_ci_guard()
        if guard != 0:
            return guard
        code = 0
        code |= run([base_python(), "tools/check_pylint.py"])
        code |= run([base_python(), "tools/check_audit.py"])
        code |= run([base_python(), "tools/check_vulnerabilities.py"])
        code |= run([base_python(), "tools/security_checks.py"])
        sbom_needed = run([base_python(), "tools/should_run_sbom.py"])
        if sbom_needed != 0:
            code |= run([base_python(), "tools/generate_sbom.py"])
        code |= task_test("tests.test_suite_full")
        code |= run([base_python(), "tools/check_secrets.py"])
        code |= task_ci_record()
        return code
    if task == "setup-env":
        return run([base_python(), "tools/setup_env.py", *extra])
    if task == "wsl-check":
        return run([base_python(), "tools/wsl_probe.py"])
    if task == "wsl-security":
        return run([base_python(), "tools/run_security_wsl.py"])
    if task == "wsl-ci":
        return run([base_python(), "tools/run_ci_wsl.py"])
    if task == "docker-check":
        return run([base_python(), "tools/docker_probe.py"])
    if task == "docker-security":
        return run([base_python(), "tools/run_security_docker.py"])
    if task == "docker-ci":
        return run([base_python(), "tools/run_ci_docker.py"])
    if task == "wsl-docker-install":
        return run([base_python(), "tools/run_wsl_docker.py", "install"])
    if task == "wsl-compose-ci":
        return run([base_python(), "tools/run_wsl_docker.py", "compose", "ci"])
    if task == "wsl-compose-security":
        return run([base_python(), "tools/run_wsl_docker.py", "compose", "security"])

    print(f"Unknown task: {task}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
