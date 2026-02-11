#!/usr/bin/env bash
set -euo pipefail

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is not installed. Run scripts/wsl_install_docker.sh first."
  exit 2
fi

if ! command -v docker compose >/dev/null 2>&1; then
  echo "docker compose plugin not found. Install docker-compose-plugin."
  exit 2
fi

MODE="${1:-ci}"

case "$MODE" in
  ci)
    docker compose run --rm ci
    ;;
  security)
    docker compose run --rm security
    ;;
  *)
    echo "Usage: scripts/wsl_run_compose.sh [ci|security]"
    exit 2
    ;;
esac
