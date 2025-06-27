# Deploy Juggernaut AI Solution to D Drive
# Pulls latest updates from GitHub and sets up the system
# Author: Manus AI
# Date: June 27, 2025

Write-Host "========================================" -ForegroundColor Green
Write-Host "   JUGGERNAUT AI - D DRIVE DEPLOYMENT" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "WARNING: Not running as Administrator." -ForegroundColor Yellow
    Write-Host "Some operations may require Administrator privileges." -ForegroundColor Yellow
    Write-Host ""
}

# Define paths
$targetDir = "D:\JuggernautAI"
$repoUrl = "https://github.com/SpartanPlumbingJosh/juggernaut-ai.git"

Write-Host "Target Directory: $targetDir" -ForegroundColor Cyan
Write-Host "Repository: $repoUrl" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if D drive exists
if (-not (Test-Path "D:\")) {
    Write-Host "ERROR: D drive not found!" -ForegroundColor Red
    Write-Host "Please ensure D drive is available." -ForegroundColor Red
    exit 1
}
Write-Host "✓ D drive found" -ForegroundColor Green

# Step 2: Handle existing directory
if (Test-Path $targetDir) {
    Write-Host "Existing Juggernaut directory found at: $targetDir" -ForegroundColor Yellow
    
    # Check if it's a git repository
    if (Test-Path "$targetDir\.git") {
        Write-Host "Git repository detected. Pulling latest updates..." -ForegroundColor Cyan
        
        # Navigate to directory and pull updates
        Set-Location $targetDir
        
        # Fetch latest changes
        Write-Host "Fetching latest changes from GitHub..." -ForegroundColor Yellow
        git fetch origin main
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Fetch successful" -ForegroundColor Green
            
            # Pull the changes
            Write-Host "Pulling updates..." -ForegroundColor Yellow
            git pull origin main
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ Successfully pulled latest updates!" -ForegroundColor Green
            } else {
                Write-Host "ERROR: Failed to pull updates" -ForegroundColor Red
                Write-Host "You may need to resolve conflicts manually." -ForegroundColor Yellow
                exit 1
            }
        } else {
            Write-Host "ERROR: Failed to fetch from GitHub" -ForegroundColor Red
            Write-Host "Check your internet connection and repository access." -ForegroundColor Yellow
            exit 1
        }
    } else {
        Write-Host "Directory exists but is not a git repository." -ForegroundColor Yellow
        Write-Host "Backing up existing directory..." -ForegroundColor Yellow
        
        $backupDir = "D:\JuggernautAI_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        Move-Item $targetDir $backupDir
        Write-Host "✓ Backed up to: $backupDir" -ForegroundColor Green
        
        # Clone fresh repository
        Write-Host "Cloning fresh repository..." -ForegroundColor Cyan
        git clone $repoUrl $targetDir
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Repository cloned successfully!" -ForegroundColor Green
            Set-Location $targetDir
        } else {
            Write-Host "ERROR: Failed to clone repository" -ForegroundColor Red
            exit 1
        }
    }
} else {
    # Create directory and clone repository
    Write-Host "Creating Juggernaut directory and cloning repository..." -ForegroundColor Cyan
    
    # Create parent directory if needed
    $parentDir = Split-Path $targetDir -Parent
    if (-not (Test-Path $parentDir)) {
        New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
    }
    
    # Clone repository
    git clone $repoUrl $targetDir
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Repository cloned successfully!" -ForegroundColor Green
        Set-Location $targetDir
    } else {
        Write-Host "ERROR: Failed to clone repository" -ForegroundColor Red
        Write-Host "Check your internet connection and repository access." -ForegroundColor Yellow
        exit 1
    }
}

# Step 3: Verify solution files are present
Write-Host ""
Write-Host "Verifying solution files..." -ForegroundColor Cyan

$requiredFiles = @(
    "build_llama_cpp_cuda.ps1",
    "juggernaut_final_working.py", 
    "Start_Juggernaut_Final.bat",
    "FINAL_SOLUTION_README.md"
)

$allFilesPresent = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✓ $file" -ForegroundColor Green
    } else {
        Write-Host "✗ $file (MISSING)" -ForegroundColor Red
        $allFilesPresent = $false
    }
}

if (-not $allFilesPresent) {
    Write-Host ""
    Write-Host "ERROR: Some solution files are missing!" -ForegroundColor Red
    Write-Host "The repository may not have been updated properly." -ForegroundColor Yellow
    exit 1
}

# Step 4: Check for model file
Write-Host ""
Write-Host "Checking for Gemma model..." -ForegroundColor Cyan

$modelPaths = @(
    "D:\models\gemma-2-9b-it-Q6_K.gguf",
    "D:\models\gemma-2-9b-it.gguf",
    "$targetDir\models\gemma-2-9b-it-Q6_K.gguf"
)

$modelFound = $false
foreach ($modelPath in $modelPaths) {
    if (Test-Path $modelPath) {
        Write-Host "✓ Model found at: $modelPath" -ForegroundColor Green
        $modelFound = $true
        break
    }
}

if (-not $modelFound) {
    Write-Host "⚠ Gemma model not found in expected locations:" -ForegroundColor Yellow
    foreach ($path in $modelPaths) {
        Write-Host "  - $path" -ForegroundColor Gray
    }
    Write-Host "Please ensure your Gemma model is downloaded to D:\models\" -ForegroundColor Yellow
}

# Step 5: Display next steps
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   DEPLOYMENT COMPLETED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Current directory: $targetDir" -ForegroundColor Cyan
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. BUILD LLAMA-CPP-PYTHON FROM SOURCE:" -ForegroundColor White
Write-Host "   .\build_llama_cpp_cuda.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. START YOUR AI SYSTEM:" -ForegroundColor White
Write-Host "   .\Start_Juggernaut_Final.bat" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. ACCESS WEB INTERFACE:" -ForegroundColor White
Write-Host "   http://localhost:5000" -ForegroundColor Cyan
Write-Host ""

if (-not $modelFound) {
    Write-Host "IMPORTANT: Download your Gemma model to D:\models\ before starting!" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "For detailed instructions, see: FINAL_SOLUTION_README.md" -ForegroundColor Gray
Write-Host ""
Write-Host "Ready to build and run your AI system!" -ForegroundColor Green

