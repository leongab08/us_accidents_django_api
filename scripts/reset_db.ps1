$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Host "Removing containers and volume..."
docker compose down -v

Write-Host "Recreating database and loading CSV from scratch..."
docker compose up -d postgres

Write-Host "Use scripts/start_db.ps1 in a few moments to verify the row count."
