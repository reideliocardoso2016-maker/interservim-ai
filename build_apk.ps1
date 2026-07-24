<#
.SYNOPSIS
    Build script for INTERSERVIM AI SALES AGENT - APK Generation
.DESCRIPTION
    This script automates the build process for the Android APK.
    It installs any missing dependencies and builds the Flutter APK.
#>

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host " INTERSERVIM AI SALES AGENT - APK Builder" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$FlutterAppDir = Join-Path $ProjectRoot "apps\mobile\flutter_app"
$FlutterInstallDir = "C:\flutter"
$PythonApiDir = Join-Path $ProjectRoot "apps\backend\api"
$AndroidSdkDir = "$env:LOCALAPPDATA\Android\Sdk"

# Step 1: Check prerequisites
Write-Host "[1/7] Verificando requisitos..." -ForegroundColor Yellow

$hasGit = $false
try { git --version 2>$null; $hasGit = $true } catch {}

$hasFlutter = $false
try { flutter --version 2>$null; $hasFlutter = $true } catch {}

$hasPython = $false
try { python --version 2>$null; $hasPython = $true } catch {}

$hasJava = $false
try { java -version 2>$null; $hasJava = $true } catch {}

Write-Host "  Git: $(if($hasGit){'✅'}else{'❌'})"
Write-Host "  Flutter: $(if($hasFlutter){'✅'}else{'❌'})"
Write-Host "  Python: $(if($hasPython){'✅'}else{'❌'})"
Write-Host "  Java: $(if($hasJava){'✅'}else{'❌'})"

# Step 2: Install Git if needed
if (-not $hasGit) {
    Write-Host "[2/7] Instalando Git..." -ForegroundColor Yellow
    winget install Git.Git --accept-package-agreements --accept-source-agreements --silent
    $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
}

# Step 3: Install Flutter if needed
if (-not $hasFlutter) {
    Write-Host "[3/7] Instalando Flutter SDK..." -ForegroundColor Yellow
    if (-not (Test-Path $FlutterInstallDir)) {
        git clone -b stable --depth 1 https://github.com/flutter/flutter.git $FlutterInstallDir
        $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
        [Environment]::SetEnvironmentVariable("Path", "$userPath;C:\flutter\bin", "User")
        $env:Path = "$env:Path;C:\flutter\bin"
    }
    
    # Try multiple times to download Dart SDK (network may be intermittent)
    $maxRetries = 5
    $retryDelay = 10
    for ($i = 1; $i -le $maxRetries; $i++) {
        Write-Host "  Attempt $i/$maxRetries to initialize Flutter..."
        $result = & flutter --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $hasFlutter = $true
            break
        }
        Write-Host "  Retrying in ${retryDelay}s..."
        Start-Sleep $retryDelay
        $retryDelay = [Math]::Min($retryDelay * 2, 120)
    }
}

# Step 4: Install Java (JDK 17 for Android)
if (-not $hasJava) {
    Write-Host "[4/7] Instalando Java JDK 17..." -ForegroundColor Yellow
    $javaUrl = "https://aka.ms/download-jdk/microsoft-jdk-17.0.13-windows-x64.zip"
    $javaZip = "$env:TEMP\jdk.zip"
    try {
        Invoke-WebRequest -Uri $javaUrl -OutFile $javaZip -UseBasicParsing
        Expand-Archive -Path $javaZip -DestinationPath "C:\Program Files\Java" -Force
        $javaHome = Get-ChildItem "C:\Program Files\Java" -Directory | Select-Object -First 1
        if ($javaHome) {
            [Environment]::SetEnvironmentVariable("JAVA_HOME", $javaHome.FullName, "Machine")
            $env:JAVA_HOME = $javaHome.FullName
            $env:Path = "$($javaHome.FullName)\bin;$env:Path"
        }
    } catch {
        Write-Host "  Java download failed: $_" -ForegroundColor Red
    }
}

# Step 5: Accept Android licenses
if ($hasFlutter) {
    Write-Host "[5/7] Configurando Android SDK..." -ForegroundColor Yellow
    # Try to accept licenses
    & flutter doctor --android-licenses 2>&1 | Out-Null
    Write-Host "  Ejecutando flutter doctor..." -ForegroundColor Yellow
    & flutter doctor 2>&1
}

# Step 6: Install Python dependencies and seed DB
Write-Host "[6/7] Configurando Backend..." -ForegroundColor Yellow
if ($hasPython) {
    Push-Location $PythonApiDir
    pip install -r requirements.txt 2>&1 | Out-Null
    $env:DATABASE_URL = "sqlite:///./interservim_ai.db"
    python seed.py 2>&1
    Pop-Location
}

# Step 7: Build Flutter APK
Write-Host "[7/7] Generando APK..." -ForegroundColor Yellow
if ($hasFlutter) {
    Push-Location $FlutterAppDir
    & flutter pub get 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Construyendo APK (release)..." -ForegroundColor Yellow
        & flutter build apk --release 2>&1
        if ($LASTEXITCODE -eq 0) {
            $apkPath = "build\app\outputs\flutter-apk\app-release.apk"
            if (Test-Path $apkPath) {
                $size = (Get-Item $apkPath).Length / 1MB
                Write-Host ""
                Write-Host "================================================" -ForegroundColor Green
                Write-Host " APK GENERADO EXITOSAMENTE!" -ForegroundColor Green
                Write-Host " Ruta: $apkPath" -ForegroundColor Green
                Write-Host " Tamaño: $([math]::Round($size, 2)) MB" -ForegroundColor Green
                Write-Host "================================================" -ForegroundColor Green
            }
        } else {
            Write-Host "  ERROR: El build del APK falló" -ForegroundColor Red
        }
    }
    Pop-Location
} else {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Yellow
    Write-Host " FLUTTER NO DISPONIBLE" -ForegroundColor Yellow
    Write-Host "================================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Para generar el APK manualmente:" -ForegroundColor White
    Write-Host "1. Abra una terminal NUEVA (como Administrador)" -ForegroundColor White
    Write-Host "2. cd $FlutterAppDir" -ForegroundColor White
    Write-Host "3. flutter pub get" -ForegroundColor White
    Write-Host "4. flutter build apk --release" -ForegroundColor White
    Write-Host ""
    Write-Host "Alternativa - use Flutter en línea (codemagic.io, etc.):" -ForegroundColor White
    Write-Host "5. Suba el código a GitHub" -ForegroundColor White
    Write-Host "6. Conecte con Codemagic" -ForegroundColor White
    Write-Host "7. Build automático del APK" -ForegroundColor White
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host " PROCESO COMPLETADO" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
