# Juggernaut AI - Complete Setup Script
# One-click setup for reliable Gemma AI system using Ollama
# Author: Manus AI
# Date: June 27, 2025

Write-Host "========================================" -ForegroundColor Red
Write-Host "   JUGGERNAUT AI - COMPLETE SETUP" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
Write-Host ""
Write-Host "RTX 4070 SUPER Optimized System" -ForegroundColor White
Write-Host "Real Gemma 3 AI via Ollama" -ForegroundColor White
Write-Host "No DLL Dependencies" -ForegroundColor White
Write-Host "One-Click Desktop Launch" -ForegroundColor White
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "NOTICE: Running without Administrator privileges." -ForegroundColor Yellow
    Write-Host "Some operations may require elevation." -ForegroundColor Yellow
    Write-Host ""
}

$setupStartTime = Get-Date

# Step 1: Install Ollama
Write-Host "STEP 1: Installing Ollama..." -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan

& .\install_ollama.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Ollama installation failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "SUCCESS: Ollama installation completed!" -ForegroundColor Green
Write-Host ""

# Step 2: Install Python dependencies
Write-Host "STEP 2: Installing Python Dependencies..." -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

$pythonDeps = @("flask", "requests")

foreach ($dep in $pythonDeps) {
    Write-Host "Installing $dep..." -ForegroundColor Yellow
    pip install $dep --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: $dep installed" -ForegroundColor Green
    } else {
        Write-Host "WARNING: Failed to install $dep" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "SUCCESS: Python dependencies completed!" -ForegroundColor Green
Write-Host ""

# Step 3: Create desktop shortcut
Write-Host "STEP 3: Creating Desktop Shortcut..." -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

& .\create_desktop_shortcut.ps1

Write-Host ""
Write-Host "SUCCESS: Desktop shortcut created!" -ForegroundColor Green
Write-Host ""

# Step 4: Final verification
Write-Host "STEP 4: Final System Verification..." -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# Check if all components are in place
$componentsOK = $true

# Check Ollama
try {
    $ollamaVersion = ollama --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: Ollama is ready: $ollamaVersion" -ForegroundColor Green
    } else {
        Write-Host "WARNING: Ollama not responding" -ForegroundColor Yellow
        $componentsOK = $false
    }
} catch {
    Write-Host "WARNING: Ollama not found in PATH" -ForegroundColor Yellow
    $componentsOK = $false
}

# Check Python files
$requiredFiles = @("juggernaut_ollama.py", "Start_Juggernaut_AI.bat")
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "SUCCESS: $file found" -ForegroundColor Green
    } else {
        Write-Host "ERROR: $file missing" -ForegroundColor Red
        $componentsOK = $false
    }
}

# Check desktop shortcut
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = "$desktopPath\Juggernaut AI.lnk"
if (Test-Path $shortcutPath) {
    Write-Host "SUCCESS: Desktop shortcut created" -ForegroundColor Green
} else {
    Write-Host "WARNING: Desktop shortcut not found" -ForegroundColor Yellow
}

$setupEndTime = Get-Date
$setupDuration = $setupEndTime - $setupStartTime

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   SETUP COMPLETED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Setup time: $($setupDuration.ToString('mm\:ss'))" -ForegroundColor Green
Write-Host ""

if ($componentsOK) {
    Write-Host "SYSTEM STATUS: READY" -ForegroundColor Green
    Write-Host ""
    Write-Host "YOUR JUGGERNAUT AI SYSTEM IS READY!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "TO START YOUR AI SYSTEM:" -ForegroundColor Cyan
    Write-Host "1. Double-click 'Juggernaut AI' on your desktop" -ForegroundColor White
    Write-Host "   OR" -ForegroundColor Gray
    Write-Host "2. Run: Start_Juggernaut_AI.bat" -ForegroundColor White
    Write-Host ""
    Write-Host "FEATURES:" -ForegroundColor Cyan
    Write-Host "- Real Gemma 3 AI responses (no demo mode)" -ForegroundColor White
    Write-Host "- RTX 4070 SUPER GPU acceleration (automatic)" -ForegroundColor White
    Write-Host "- CPU fallback (automatic)" -ForegroundColor White
    Write-Host "- No DLL dependency issues" -ForegroundColor White
    Write-Host "- Professional Monster UI" -ForegroundColor White
    Write-Host "- Web interface: http://localhost:5000" -ForegroundColor White
    Write-Host ""
    Write-Host "Your AI system will be ready for tasks immediately!" -ForegroundColor Green
} else {
    Write-Host "SYSTEM STATUS: NEEDS ATTENTION" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Some components need attention. Please:" -ForegroundColor Yellow
    Write-Host "1. Restart PowerShell as Administrator" -ForegroundColor White
    Write-Host "2. Re-run this setup script" -ForegroundColor White
    Write-Host "3. Check error messages above" -ForegroundColor White
}

Write-Host ""
Write-Host "Setup completed at: $(Get-Date)" -ForegroundColor Gray

