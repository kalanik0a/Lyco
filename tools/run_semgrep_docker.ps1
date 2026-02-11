$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

Write-Host "Running semgrep in Docker..."
docker run --rm -v "${root}:/src" semgrep/semgrep semgrep --config /src/.semgrep.yml /src/src /src/Lyco.py /src/tools
