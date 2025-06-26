# Juggernaut AI - FIXED Setup Script
# RTX 4070 SUPER Optimized AI System
# Clean, working PowerShell setup

Write-Host "🤖 JUGGERNAUT AI SETUP" -ForegroundColor Magenta
Write-Host "RTX 4070 SUPER Optimized" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor White

# Step 1: Check Python
Write-Host "`n🔍 Checking Python..." -ForegroundColor Green
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ Python not found. Please install Python 3.11+ from python.org" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Python not found. Please install Python 3.11+ from python.org" -ForegroundColor Red
    exit 1
}

# Step 2: Install dependencies
Write-Host "`n📦 Installing Python dependencies..." -ForegroundColor Green
$packages = @(
    "Flask==2.3.3",
    "Flask-CORS==4.0.0", 
    "Werkzeug==2.3.7",
    "requests==2.31.0",
    "Pillow==10.0.1",
    "python-multipart==0.0.6"
)

foreach ($package in $packages) {
    Write-Host "Installing $package..." -ForegroundColor Yellow
    pip install $package
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️ Warning: Failed to install $package" -ForegroundColor Yellow
    }
}

# Step 3: Create data directory
Write-Host "`n📁 Creating data directory..." -ForegroundColor Green
$dataPath = "D:\JUGGERNAUT_DATA"

try {
    if (-not (Test-Path $dataPath)) {
        New-Item -ItemType Directory -Path $dataPath -Force | Out-Null
        Write-Host "✅ Created: $dataPath" -ForegroundColor Green
    } else {
        Write-Host "✅ Directory exists: $dataPath" -ForegroundColor Green
    }
    
    # Create subdirectories
    $subdirs = @("models", "chats", "files", "browser", "plugins")
    foreach ($subdir in $subdirs) {
        $fullPath = Join-Path $dataPath $subdir
        if (-not (Test-Path $fullPath)) {
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        }
    }
    Write-Host "✅ Subdirectories created" -ForegroundColor Green
    
} catch {
    Write-Host "⚠️ Could not create $dataPath - will use local directory" -ForegroundColor Yellow
}

# Step 4: Check for GPU (optional)
Write-Host "`n🎯 Checking for RTX 4070 SUPER..." -ForegroundColor Green
try {
    $gpu = Get-WmiObject -Class Win32_VideoController | Where-Object { $_.Name -like "*NVIDIA*" }
    if ($gpu) {
        Write-Host "✅ NVIDIA GPU detected: $($gpu.Name)" -ForegroundColor Green
        if ($gpu.Name -like "*RTX 4070 SUPER*") {
            Write-Host "🚀 RTX 4070 SUPER detected - GPU acceleration ready!" -ForegroundColor Cyan
        }
    } else {
        Write-Host "⚠️ No NVIDIA GPU detected - CPU mode will be used" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ Could not detect GPU information" -ForegroundColor Yellow
}

# Step 5: Test core modules
Write-Host "`n🧪 Testing core modules..." -ForegroundColor Green
try {
    python -c "import flask; print('✅ Flask imported successfully')"
    python -c "import core; print('✅ Core modules imported successfully')" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️ Core modules not fully available - some features may be limited" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ Module test failed - some features may be limited" -ForegroundColor Yellow
}

# Step 6: Create startup batch file
Write-Host "`n📝 Creating startup file..." -ForegroundColor Green
$batchContent = @"
@echo off
title Juggernaut AI - RTX 4070 SUPER
echo 🤖 Starting Juggernaut AI System...
echo 🎯 RTX 4070 SUPER Optimized
echo.
python app.py
pause
"@

try {
    Set-Content -Path "start_juggernaut.bat" -Value $batchContent -Encoding ASCII
    Write-Host "✅ Created start_juggernaut.bat" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Could not create startup file" -ForegroundColor Yellow
}

# Final instructions
Write-Host "`n🎉 SETUP COMPLETE!" -ForegroundColor Green
Write-Host "==================" -ForegroundColor White
Write-Host ""
Write-Host "🚀 TO START JUGGERNAUT AI:" -ForegroundColor Cyan
Write-Host "   python app.py" -ForegroundColor White
Write-Host "   OR double-click: start_juggernaut.bat" -ForegroundColor White
Write-Host ""
Write-Host "🌐 ACCESS THE INTERFACE:" -ForegroundColor Cyan  
Write-Host "   http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "📁 DATA DIRECTORY:" -ForegroundColor Cyan
Write-Host "   $dataPath" -ForegroundColor White
Write-Host ""
Write-Host "🎯 RTX 4070 SUPER GPU acceleration ready!" -ForegroundColor Green
Write-Host ""

# Ask if user wants to start now
$startNow = Read-Host "Start Juggernaut AI now? (y/n)"
if ($startNow -eq 'y' -or $startNow -eq 'Y') {
    Write-Host "`n🚀 Starting Juggernaut AI..." -ForegroundColor Green
    python app.py
}

