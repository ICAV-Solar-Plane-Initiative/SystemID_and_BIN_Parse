# Create the project virtual environment (.venv) and install dependencies.
#
# Usage, from the repo root in PowerShell:
#     .\setup_env.ps1
#     .\setup_env.ps1 -Python "C:\path\to\python.exe"   # use a specific Python
#
# If PowerShell blocks the script, run it once with:
#     powershell -ExecutionPolicy Bypass -File .\setup_env.ps1

param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$VenvPython = ".venv\Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Host "Creating virtual environment in .venv ..."
    & $Python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw "Could not create .venv with '$Python'." }
}

Write-Host "Installing dependencies from requirements.txt ..."
& $VenvPython -m pip install --upgrade pip
& $VenvPython -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Dependency install failed." }

Write-Host ""
Write-Host "Done. Activate the environment with:  .venv\Scripts\Activate.ps1"
