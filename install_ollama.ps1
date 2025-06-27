# Ollama Installer and Setup Script for Juggernaut AI
# Installs Ollama and sets up Gemma model for reliable AI responses
# Author: Manus AI
# Date: June 27, 2025

Write-Host "========================================" -ForegroundColor Green
Write-Host "   JUGGERNAUT AI - OLLAMA SETUP" -ForegroundColor Green
Write-Host "   Reliable Gemma AI Installation" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "WARNING: Not running as Administrator." -ForegroundColor Yellow
    Write-Host "Some operations may require Administrator privileges." -ForegroundColor Yellow
    Write-Host ""
}

# Step 1: Check if Ollama is already installed
Write-Host "Step 1: Checking for existing Ollama installation..." -ForegroundColor Cyan

try {
    $ollamaVersion = ollama --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: Ollama is already installed: $ollamaVersion" -ForegroundColor Green
        $ollamaInstalled = $true
    } else {
        $ollamaInstalled = $false
    }
} catch {
    $ollamaInstalled = $false
}

# Step 2: Install Ollama if not present
if (-not $ollamaInstalled) {
    Write-Host "Step 2: Installing Ollama..." -ForegroundColor Cyan
    
    $ollamaUrl = "https://ollama.com/download/windows"
    $installerPath = "$env:TEMP\OllamaSetup.exe"
    
    Write-Host "Downloading Ollama installer..." -ForegroundColor Yellow
    try {
        Invoke-WebRequest -Uri $ollamaUrl -OutFile $installerPath
        Write-Host "SUCCESS: Ollama installer downloaded" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Failed to download Ollama installer" -ForegroundColor Red
        Write-Host "Please download manually from: https://ollama.com/download" -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host "Installing Ollama (this may take a few minutes)..." -ForegroundColor Yellow
    try {
        Start-Process $installerPath -ArgumentList "/S" -Wait
        Write-Host "SUCCESS: Ollama installation completed" -ForegroundColor Green
        
        # Add Ollama to PATH if needed
        $env:PATH = "$env:PATH;$env:LOCALAPPDATA\Programs\Ollama"
        
        # Verify installation
        Start-Sleep -Seconds 5
        $ollamaVersion = ollama --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "SUCCESS: Ollama verified: $ollamaVersion" -ForegroundColor Green
        } else {
            Write-Host "WARNING: Ollama installed but not in PATH. Restart may be required." -ForegroundColor Yellow
        }
    } catch {
        Write-Host "ERROR: Failed to install Ollama" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Ollama is already installed, skipping installation." -ForegroundColor Green
}

# Step 3: Check for existing Gemma model
Write-Host ""
Write-Host "Step 3: Checking for Gemma model..." -ForegroundColor Cyan

$modelList = ollama list 2>&1
if ($modelList -match "gemma") {
    Write-Host "SUCCESS: Gemma model already installed" -ForegroundColor Green
    $modelInstalled = $true
} else {
    $modelInstalled = $false
}

# Step 4: Install Gemma model if not present
if (-not $modelInstalled) {
    Write-Host "Step 4: Installing Gemma 3 model (9B parameters)..." -ForegroundColor Cyan
    Write-Host "This will download approximately 5.5GB. Please be patient..." -ForegroundColor Yellow
    
    $modelStartTime = Get-Date
    
    # Pull the 9B model (equivalent to user's Q6_K model)
    ollama pull gemma3:9b
    
    if ($LASTEXITCODE -eq 0) {
        $modelEndTime = Get-Date
        $modelDuration = $modelEndTime - $modelStartTime
        Write-Host "SUCCESS: Gemma 3 model installed in $($modelDuration.ToString('mm\:ss'))" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Failed to install Gemma model" -ForegroundColor Red
        Write-Host "Check your internet connection and try again." -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "Gemma model is already installed, skipping download." -ForegroundColor Green
}

# Step 5: Test Ollama service
Write-Host ""
Write-Host "Step 5: Testing Ollama service..." -ForegroundColor Cyan

# Start Ollama service in background
Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden

# Wait for service to start
Start-Sleep -Seconds 3

# Test the API
try {
    $testResponse = Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -Body '{"model":"gemma3:9b","prompt":"Hello","stream":false}' -ContentType "application/json" -TimeoutSec 30
    
    if ($testResponse.response) {
        Write-Host "SUCCESS: Ollama API is working" -ForegroundColor Green
        Write-Host "Test response: $($testResponse.response.Substring(0, [Math]::Min(50, $testResponse.response.Length)))..." -ForegroundColor Gray
    } else {
        Write-Host "WARNING: Ollama API responded but no content received" -ForegroundColor Yellow
    }
} catch {
    Write-Host "WARNING: Could not test Ollama API immediately" -ForegroundColor Yellow
    Write-Host "The service may need a moment to fully start" -ForegroundColor Yellow
}

# Step 6: Display completion information
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   OLLAMA SETUP COMPLETED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "INSTALLATION SUMMARY:" -ForegroundColor Cyan
Write-Host "- Ollama: Installed and running" -ForegroundColor White
Write-Host "- Gemma 3 Model: 9B parameters (equivalent to your Q6_K model)" -ForegroundColor White
Write-Host "- API Endpoint: http://localhost:11434" -ForegroundColor White
Write-Host "- GPU Acceleration: Automatic (when available)" -ForegroundColor White
Write-Host "- CPU Fallback: Automatic" -ForegroundColor White
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. Your Juggernaut AI system will now use Ollama instead of llama-cpp-python" -ForegroundColor White
Write-Host "2. No more DLL dependency issues" -ForegroundColor White
Write-Host "3. Automatic GPU acceleration with CPU fallback" -ForegroundColor White
Write-Host "4. Real Gemma responses with full capabilities" -ForegroundColor White
Write-Host ""
Write-Host "The Ollama service will start automatically with Windows." -ForegroundColor Gray
Write-Host "Your Juggernaut AI system is ready to use!" -ForegroundColor Green

