#!/usr/bin/env bash
set -euo pipefail

if command -v docker >/dev/null 2>&1; then
  echo "Docker is already installed."
  exit 0
fi

if ! command -v sudo >/dev/null 2>&1; then
  echo "sudo is required to install Docker."
  exit 2
fi

echo "Installing Docker engine and compose plugin..."
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-plugin

echo "Enabling Docker service..."
sudo service docker start || true

echo "Adding current user to docker group..."
sudo usermod -aG docker "$USER"

echo "Docker installation complete. You may need to restart the WSL session."
