# Interservim AI Sales Agent - Setup Script
# Run this script as Administrator to install all dependencies

Write-Host "========================================"
Write-Host "INTERSERVIM AI SALES AGENT - Setup"
Write-Host "========================================"

# 1. Check if running as admin
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "WARNING: Not running as Administrator. Some installations may fail." -ForegroundColor Yellow
}

# 2. Check Python
try {
    $pyVersion = python --version 2>&1
    Write-Host "[OK] Python: $pyVersion" -ForegroundColor Green
} catch {
    Write-Host "[FAIL] Python not found. Download from https://python.org" -ForegroundColor Red
}

# 3. Install Flutter
$flutterPath = "C:\flutter"
if (-not (Test-Path "$flutterPath\bin\flutter.bat")) {
    Write-Host "Installing Flutter SDK..." -ForegroundColor Yellow
    
    # Try to detect latest version
    $manifestUrl = "https://storage.googleapis.com/flutter_infra_release/releases/releases_windows.json"
    try {
        $manifest = Invoke-RestMethod -Uri $manifestUrl -Headers @{"User-Agent"="Mozilla/5.0"}
        $latestStable = $manifest.releases | Where-Object { $_.channel -eq "stable" } | Select-Object -Last 1
        $version = $latestStable.version
        $archive = $latestStable.archive
        $downloadUrl = "https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/$archive"
        Write-Host "Downloading Flutter $version..."
        Invoke-WebRequest -Uri $downloadUrl -OutFile "$env:TEMP\flutter.zip" -UseBasicParsing
        Expand-Archive -Path "$env:TEMP\flutter.zip" -DestinationPath "C:\"
        [Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";C:\flutter\bin", "User")
        Write-Host "[OK] Flutter $version installed" -ForegroundColor Green
    } catch {
        Write-Host "[FAIL] Could not download Flutter. Download manually from https://flutter.dev" -ForegroundColor Red
        Write-Host "Extract to C:\flutter and add C:\flutter\bin to PATH" -ForegroundColor Yellow
    }
} else {
    Write-Host "[OK] Flutter already installed" -ForegroundColor Green
}

# 4. Install Python dependencies
if (Test-Path "apps\backend\api\requirements.txt") {
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    pip install -r apps\backend\api\requirements.txt
    Write-Host "[OK] Python dependencies installed" -ForegroundColor Green
}

# 5. Android Studio check
$androidStudio = Get-ItemProperty "HKLM:\SOFTWARE\Android Studio" -ErrorAction SilentlyContinue
if (-not $androidStudio) {
    Write-Host "[WARN] Android Studio not detected. Download from https://developer.android.com/studio" -ForegroundColor Yellow
} else {
    Write-Host "[OK] Android Studio detected" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================"
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Open a NEW terminal"
Write-Host "2. Run: flutter doctor"
Write-Host "3. Run: cd apps\mobile\flutter_app && flutter pub get"
Write-Host "4. Run: cd apps\backend\api && uvicorn app.main:app --reload"
Write-Host "========================================"
