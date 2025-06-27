# JUGGERNAUT AI - Enhanced System Setup Script
# Installs dependencies and prepares the enhanced system

param(
    [switch]$SkipDependencies = $false
)

Write-Host "========================================" -ForegroundColor Red
Write-Host "   JUGGERNAUT AI - ENHANCED SETUP" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
Write-Host ""
Write-Host "Setting up Enhanced System with System Access" -ForegroundColor Yellow
Write-Host ""

# Check if Python is available
Write-Host "Step 1: Checking Python installation..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "SUCCESS: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check if Ollama is available
Write-Host "Step 2: Checking Ollama installation..." -ForegroundColor Cyan
try {
    $ollamaVersion = ollama --version 2>&1
    Write-Host "SUCCESS: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Ollama not found. Please install Ollama first." -ForegroundColor Red
    exit 1
}

# Check if Gemma 3 model is available
Write-Host "Step 3: Checking Gemma 3 model..." -ForegroundColor Cyan
try {
    $models = ollama list 2>&1
    if ($models -match "gemma3:12b") {
        Write-Host "SUCCESS: Gemma 3 12B model found" -ForegroundColor Green
    } else {
        Write-Host "WARNING: Gemma 3 12B model not found" -ForegroundColor Yellow
        Write-Host "Installing Gemma 3 12B model..." -ForegroundColor Cyan
        ollama pull gemma3:12b
        if ($LASTEXITCODE -eq 0) {
            Write-Host "SUCCESS: Gemma 3 12B model installed" -ForegroundColor Green
        } else {
            Write-Host "ERROR: Failed to install Gemma 3 model" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "ERROR: Failed to check Ollama models" -ForegroundColor Red
    exit 1
}

# Install Python dependencies
if (-not $SkipDependencies) {
    Write-Host "Step 4: Installing Python dependencies..." -ForegroundColor Cyan
    try {
        pip install -r requirements_enhanced.txt --upgrade
        if ($LASTEXITCODE -eq 0) {
            Write-Host "SUCCESS: Dependencies installed" -ForegroundColor Green
        } else {
            Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
            exit 1
        }
    } catch {
        Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Step 4: Skipping dependency installation (--SkipDependencies)" -ForegroundColor Yellow
}

# Test system access module
Write-Host "Step 5: Testing system access module..." -ForegroundColor Cyan
try {
    $testResult = python -c "from system_access_module import system_access; print('System access module loaded successfully')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: System access module working" -ForegroundColor Green
    } else {
        Write-Host "WARNING: System access module test failed: $testResult" -ForegroundColor Yellow
        Write-Host "The system will still work but some features may be limited" -ForegroundColor Yellow
    }
} catch {
    Write-Host "WARNING: Could not test system access module" -ForegroundColor Yellow
}

# Create desktop shortcut
Write-Host "Step 6: Creating desktop shortcut..." -ForegroundColor Cyan
try {
    $currentDir = Get-Location
    $shortcutPath = "$env:USERPROFILE\Desktop\Juggernaut AI Enhanced.lnk"
    $targetPath = "$currentDir\Start_Enhanced_Juggernaut.bat"
    
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($shortcutPath)
    $Shortcut.TargetPath = $targetPath
    $Shortcut.WorkingDirectory = $currentDir
    $Shortcut.Description = "Juggernaut AI Enhanced System with System Access"
    $Shortcut.Save()
    
    Write-Host "SUCCESS: Desktop shortcut created" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Could not create desktop shortcut: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Red
Write-Host "   ENHANCED SYSTEM SETUP COMPLETE!" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
Write-Host ""
Write-Host "SYSTEM CAPABILITIES:" -ForegroundColor Yellow
Write-Host "- File Operations and Analysis" -ForegroundColor White
Write-Host "- Directory Structure Analysis" -ForegroundColor White
Write-Host "- Command Execution" -ForegroundColor White
Write-Host "- System Performance Monitoring" -ForegroundColor White
Write-Host "- Installed Software Detection" -ForegroundColor White
Write-Host "- Comprehensive System Reports" -ForegroundColor White
Write-Host ""
Write-Host "TO START THE ENHANCED SYSTEM:" -ForegroundColor Yellow
Write-Host "1. Double-click 'Juggernaut AI Enhanced' on your desktop" -ForegroundColor White
Write-Host "2. Or run: Start_Enhanced_Juggernaut.bat" -ForegroundColor White
Write-Host "3. Access at: http://localhost:5001" -ForegroundColor White
Write-Host ""
Write-Host "EXAMPLE COMMANDS TO TRY:" -ForegroundColor Yellow
Write-Host "- 'Analyze my D: drive and show largest files'" -ForegroundColor White
Write-Host "- 'Show me my system overview'" -ForegroundColor White
Write-Host "- 'What software is installed on my computer?'" -ForegroundColor White
Write-Host "- 'Read the file D:/myfile.txt and explain it'" -ForegroundColor White
Write-Host ""
Write-Host "Your AI now has comprehensive system access!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Red

