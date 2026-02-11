$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$wslRoot = & wsl.exe wslpath -a "$root"

if (-not $wslRoot) {
    throw "Failed to resolve WSL path. Is WSL installed?"
}

Write-Host "Running semgrep in WSL..."
& wsl.exe semgrep --config "$wslRoot/.semgrep.yml" "$wslRoot/src" "$wslRoot/Lyco.py" "$wslRoot/tools"
