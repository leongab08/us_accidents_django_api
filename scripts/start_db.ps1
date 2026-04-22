$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Host "Starting PostgreSQL container..."
docker compose up -d postgres

Write-Host "Waiting for PostgreSQL to become ready..."
$maxAttempts = 60
for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
    try {
        docker compose exec -T postgres pg_isready -U accidents_user -d accidents_db | Out-Null
        Write-Host "PostgreSQL is ready."
        break
    }
    catch {
        if ($attempt -eq $maxAttempts) {
            throw "PostgreSQL did not become ready in time."
        }
        Start-Sleep -Seconds 2
    }
}

Write-Host "Current row count in us_accidents:"
docker compose exec -T postgres psql -U accidents_user -d accidents_db -c "SELECT COUNT(*) AS total_rows FROM us_accidents;"
