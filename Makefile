PYTHON ?= python

.PHONY: venv install install-dev clean-venv clean \
	test-core test-full test-one \
	pylint audit safety security secrets sbom sbom-if-needed \
	ci-guard ci-record ci-fast ci-full requirements-lock setup-env \
	wsl-check wsl-security wsl-ci docker-check docker-security docker-ci \
	wsl-docker-install wsl-compose-ci wsl-compose-security

venv:
	$(PYTHON) tools/run_task.py venv

clean-venv:
	$(PYTHON) -c "import os, shutil, pathlib; shutil.rmtree(pathlib.Path(os.environ.get('LYCO_VENV', '.venv')), ignore_errors=True)"

clean:
	$(PYTHON) tools/clean_artifacts.py

install:
	$(PYTHON) tools/run_task.py install

install-dev:
	$(PYTHON) tools/run_task.py install-dev

requirements-lock:
	$(PYTHON) tools/run_task.py requirements-lock

test-core:
	$(PYTHON) tools/run_task.py test-core

test-full:
	$(PYTHON) tools/run_task.py test-full

test-one:
	$(PYTHON) tools/run_task.py test-one $(TEST)

pylint:
	$(PYTHON) tools/run_task.py pylint

audit:
	$(PYTHON) tools/run_task.py audit

safety:
	$(PYTHON) tools/run_task.py safety

security:
	$(PYTHON) tools/run_task.py security

secrets:
	$(PYTHON) tools/run_task.py secrets

sbom:
	$(PYTHON) tools/run_task.py sbom

sbom-if-needed:
	$(PYTHON) tools/run_task.py sbom-if-needed

ci-guard:
	$(PYTHON) tools/run_task.py ci-guard

ci-record:
	$(PYTHON) tools/run_task.py ci-record

ci-fast: ci-guard pylint audit test-core

ci-full: ci-guard pylint audit safety security sbom-if-needed test-full secrets ci-record

setup-env:
	$(PYTHON) tools/run_task.py setup-env

wsl-check:
	$(PYTHON) tools/wsl_probe.py

wsl-security:
	$(PYTHON) tools/run_security_wsl.py

wsl-ci:
	$(PYTHON) tools/run_ci_wsl.py

docker-check:
	$(PYTHON) tools/docker_probe.py

docker-security:
	$(PYTHON) tools/run_security_docker.py

docker-ci:
	$(PYTHON) tools/run_ci_docker.py

wsl-docker-install:
	$(PYTHON) tools/run_task.py wsl-docker-install

wsl-compose-ci:
	$(PYTHON) tools/run_task.py wsl-compose-ci

wsl-compose-security:
	$(PYTHON) tools/run_task.py wsl-compose-security
