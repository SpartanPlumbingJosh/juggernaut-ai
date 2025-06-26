# Juggernaut AI - Complete Setup Script
# RTX 4070 SUPER Optimized AI System
# PowerShell Setup and Deployment Script

param(
    [switch]$SkipPython,
    [switch]$SkipModels,
    [switch]$Production,
    [string]$DataPath = "D:\JUGGERNAUT_DATA",
    [string]$GitRepo = "",
    [switch]$Help
)

# Display help information
if ($Help) {
    Write-Host @"
🤖 JUGGERNAUT AI SETUP SCRIPT
RTX 4070 SUPER Optimized AI System

USAGE:
    .\setup_juggernaut.ps1 [OPTIONS]

OPTIONS:
    -SkipPython     Skip Python installation check
    -SkipModels     Skip AI model download
    -Production     Setup for production deployment
    -DataPath       Custom data directory (default: D:\JUGGERNAUT_DATA)
    -GitRepo        Git repository URL for updates
    -Help           Show this help message

EXAMPLES:
    .\setup_juggernaut.ps1                    # Full setup
    .\setup_juggernaut.ps1 -SkipModels       # Setup without models
    .\setup_juggernaut.ps1 -Production       # Production setup
    .\setup_juggernaut.ps1 -DataPath C:\AI   # Custom data path

"@
    exit 0
}

# Color functions for output
function Write-Success { param($Message) Write-Host "✅ $Message" -ForegroundColor Green }
function Write-Info { param($Message) Write-Host "ℹ️  $Message" -ForegroundColor Cyan }
function Write-Warning { param($Message) Write-Host "⚠️  $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "❌ $Message" -ForegroundColor Red }
function Write-Header { param($Message) Write-Host "`n🚀 $Message" -ForegroundColor Magenta }

# Main setup function
function Start-JuggernautSetup {
    Write-Host @"
🤖 JUGGERNAUT AI SYSTEM SETUP
RTX 4070 SUPER Optimized Monster UI
=====================================
"@ -ForegroundColor Magenta

    try {
        # Step 1: System Requirements Check
        Write-Header "CHECKING SYSTEM REQUIREMENTS"
        Test-SystemRequirements

        # Step 2: Python Environment Setup
        if (-not $SkipPython) {
            Write-Header "SETTING UP PYTHON ENVIRONMENT"
            Install-PythonDependencies
        }

        # Step 3: Directory Structure Creation
        Write-Header "CREATING PROJECT STRUCTURE"
        New-ProjectStructure

        # Step 4: Configuration Setup
        Write-Header "CONFIGURING SYSTEM"
        Set-SystemConfiguration

        # Step 5: GPU Optimization
        Write-Header "OPTIMIZING FOR RTX 4070 SUPER"
        Optimize-GPUSettings

        # Step 6: AI Models (Optional)
        if (-not $SkipModels) {
            Write-Header "SETTING UP AI MODELS"
            Install-AIModels
        }

        # Step 7: Service Setup (Production)
        if ($Production) {
            Write-Header "CONFIGURING PRODUCTION ENVIRONMENT"
            Set-ProductionEnvironment
        }

        # Step 8: Final Verification
        Write-Header "VERIFYING INSTALLATION"
        Test-Installation

        # Step 9: Startup Instructions
        Write-Header "SETUP COMPLETE"
        Show-StartupInstructions

    } catch {
        Write-Error "Setup failed: $($_.Exception.Message)"
        Write-Host "Check logs for details: logs\setup.log" -ForegroundColor Yellow
        exit 1
    }
}

# Test system requirements
function Test-SystemRequirements {
    Write-Info "Checking system requirements..."
    
    # Check Windows version
    $osVersion = [System.Environment]::OSVersion.Version
    if ($osVersion.Major -lt 10) {
        throw "Windows 10 or higher required"
    }
    Write-Success "Windows version: $($osVersion.Major).$($osVersion.Minor)"

    # Check PowerShell version
    if ($PSVersionTable.PSVersion.Major -lt 5) {
        throw "PowerShell 5.0 or higher required"
    }
    Write-Success "PowerShell version: $($PSVersionTable.PSVersion)"

    # Check available disk space
    $drive = Split-Path $DataPath -Qualifier
    $disk = Get-WmiObject -Class Win32_LogicalDisk | Where-Object { $_.DeviceID -eq $drive }
    $freeSpaceGB = [math]::Round($disk.FreeSpace / 1GB, 2)
    
    if ($freeSpaceGB -lt 20) {
        Write-Warning "Low disk space: ${freeSpaceGB}GB available. Recommend 20GB+ for models."
    } else {
        Write-Success "Disk space: ${freeSpaceGB}GB available"
    }

    # Check for NVIDIA GPU
    try {
        $gpu = Get-WmiObject -Class Win32_VideoController | Where-Object { $_.Name -like "*NVIDIA*" }
        if ($gpu) {
            Write-Success "NVIDIA GPU detected: $($gpu.Name)"
            
            # Check for RTX 4070 SUPER specifically
            if ($gpu.Name -like "*RTX 4070 SUPER*") {
                Write-Success "RTX 4070 SUPER detected - GPU acceleration enabled!"
            } else {
                Write-Warning "RTX 4070 SUPER not detected. System optimized for RTX 4070 SUPER."
            }
        } else {
            Write-Warning "No NVIDIA GPU detected. CPU mode will be used."
        }
    } catch {
        Write-Warning "Could not detect GPU information."
    }

    # Check for CUDA (optional)
    try {
        $cudaVersion = & nvcc --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "CUDA toolkit detected"
        } else {
            Write-Warning "CUDA toolkit not found. Install for GPU acceleration."
        }
    } catch {
        Write-Warning "CUDA toolkit not found. Install for GPU acceleration."
    }
}

# Install Python dependencies
function Install-PythonDependencies {
    Write-Info "Checking Python installation..."
    
    # Check Python version
    try {
        $pythonVersion = & python --version 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "Python not found"
        }
        Write-Success "Python detected: $pythonVersion"
    } catch {
        Write-Error "Python 3.11+ required. Download from: https://python.org"
        throw "Python not installed"
    }

    # Check pip
    try {
        & pip --version 2>$null | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "pip not found"
        }
        Write-Success "pip is available"
    } catch {
        Write-Error "pip not found. Reinstall Python with pip."
        throw "pip not available"
    }

    # Upgrade pip
    Write-Info "Upgrading pip..."
    & pip install --upgrade pip

    # Install basic requirements
    Write-Info "Installing Python dependencies..."
    if (Test-Path "requirements.txt") {
        & pip install -r requirements.txt
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Python dependencies installed"
        } else {
            throw "Failed to install Python dependencies"
        }
    } else {
        Write-Warning "requirements.txt not found. Installing minimal dependencies..."
        & pip install Flask Flask-CORS Werkzeug requests Pillow python-multipart
    }

    # Install GPU support (optional)
    Write-Info "Installing GPU support (optional)..."
    try {
        & pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
        Write-Success "GPU support installed (CUDA 12.1)"
    } catch {
        Write-Warning "GPU support installation failed. CPU mode will be used."
    }
}

# Create project directory structure
function New-ProjectStructure {
    Write-Info "Creating directory structure..."
    
    # Main data directory
    if (-not (Test-Path $DataPath)) {
        New-Item -ItemType Directory -Path $DataPath -Force | Out-Null
        Write-Success "Created data directory: $DataPath"
    } else {
        Write-Info "Data directory exists: $DataPath"
    }

    # Subdirectories
    $directories = @(
        "$DataPath\models",
        "$DataPath\chats", 
        "$DataPath\files",
        "$DataPath\files\uploads",
        "$DataPath\files\processed",
        "$DataPath\images",
        "$DataPath\images\thumbnails",
        "$DataPath\browser",
        "$DataPath\browser\sessions",
        "$DataPath\browser\screenshots",
        "$DataPath\browser\downloads",
        "$DataPath\plugins",
        "$DataPath\plugins\core",
        "$DataPath\plugins\community",
        "$DataPath\plugins\custom",
        "$DataPath\plugins\config",
        "$DataPath\cache",
        "$DataPath\exports",
        "$DataPath\backups",
        "logs",
        "temp"
    )

    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }
    }
    Write-Success "Directory structure created"

    # Create .gitignore
    $gitignoreContent = @"
# Juggernaut AI - Git Ignore File
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Data directories
data/
logs/
temp/
*.log

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
desktop.ini

# Models (large files)
*.gguf
*.bin
*.safetensors

# User data
D:/JUGGERNAUT_DATA/
C:/JUGGERNAUT_DATA/
"@

    Set-Content -Path ".gitignore" -Value $gitignoreContent -Encoding UTF8
    Write-Success "Created .gitignore file"
}

# Configure system settings
function Set-SystemConfiguration {
    Write-Info "Creating system configuration..."
    
    # Create .env file
    $envContent = @"
# Juggernaut AI Configuration
JUGGERNAUT_DATA_PATH=$DataPath

# GPU Configuration
GPU_ENABLED=true
GPU_LAYERS=35
BATCH_SIZE=512
MAX_TOKENS=4096

# Server Configuration
HOST=0.0.0.0
PORT=5000
DEBUG=false

# Security
SECRET_KEY=$(New-Guid)
MAX_FILE_SIZE=100MB
ALLOWED_ORIGINS=*

# Performance
WORKER_PROCESSES=1
WORKER_THREADS=4
CACHE_SIZE=1GB

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/juggernaut.log
"@

    Set-Content -Path ".env" -Value $envContent -Encoding UTF8
    Write-Success "Created .env configuration"

    # Create config.json
    $configContent = @{
        "system" = @{
            "name" = "Juggernaut AI"
            "version" = "1.0.0"
            "data_path" = $DataPath
        }
        "ai_engine" = @{
            "gpu_enabled" = $true
            "gpu_layers" = 35
            "batch_size" = 512
            "context_length" = 4096
            "temperature" = 0.7
        }
        "server" = @{
            "host" = "0.0.0.0"
            "port" = 5000
            "debug" = $false
        }
        "security" = @{
            "max_file_size" = "100MB"
            "allowed_extensions" = @(".txt", ".pdf", ".jpg", ".png", ".mp3", ".mp4")
            "blocked_domains" = @("malware.com", "phishing.com")
        }
        "performance" = @{
            "cache_size" = "1GB"
            "worker_processes" = 1
            "request_timeout" = 30
        }
    } | ConvertTo-Json -Depth 4

    Set-Content -Path "config.json" -Value $configContent -Encoding UTF8
    Write-Success "Created config.json"
}

# Optimize GPU settings for RTX 4070 SUPER
function Optimize-GPUSettings {
    Write-Info "Optimizing for RTX 4070 SUPER..."
    
    # GPU optimization settings
    $gpuConfig = @"
# RTX 4070 SUPER Optimization Settings
# 12GB VRAM, 7168 CUDA Cores, 504 GB/s Memory Bandwidth

GPU_LAYERS=35          # Optimal for 12GB VRAM
BATCH_SIZE=512         # High throughput setting  
CONTEXT_LENGTH=4096    # Balanced context window
ROPE_FREQ_BASE=10000   # Standard RoPE frequency
ROPE_FREQ_SCALE=1.0    # No frequency scaling
N_THREADS=8            # CPU threads for preprocessing
N_GPU_LAYERS=35        # All layers on GPU
USE_MMAP=true          # Memory mapping for efficiency
USE_MLOCK=false        # Don't lock memory
NUMA=false             # Single GPU setup
"@

    Set-Content -Path "gpu_config.txt" -Value $gpuConfig -Encoding UTF8
    Write-Success "RTX 4070 SUPER optimization configured"

    # Create GPU test script
    $gpuTestScript = @"
# GPU Test Script for RTX 4070 SUPER
import subprocess
import sys

def test_gpu():
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"✅ GPU Detected: {gpu_name}")
            print(f"✅ VRAM Available: {gpu_memory:.1f}GB")
            
            if "RTX 4070 SUPER" in gpu_name:
                print("🚀 RTX 4070 SUPER detected - Optimal configuration loaded!")
            else:
                print("⚠️  Different GPU detected - Configuration may need adjustment")
        else:
            print("❌ No CUDA GPU detected")
    except ImportError:
        print("⚠️  PyTorch not installed - GPU test skipped")

if __name__ == "__main__":
    test_gpu()
"@

    Set-Content -Path "test_gpu.py" -Value $gpuTestScript -Encoding UTF8
    Write-Success "GPU test script created"
}

# Install AI models (optional)
function Install-AIModels {
    Write-Info "Setting up AI models..."
    
    $modelsPath = "$DataPath\models"
    
    # Check if models already exist
    $existingModels = Get-ChildItem -Path $modelsPath -Filter "*.gguf" -ErrorAction SilentlyContinue
    if ($existingModels.Count -gt 0) {
        Write-Success "$($existingModels.Count) GGUF models found"
        return
    }

    Write-Info "No models found. The system will run in demo mode."
    Write-Info "To add AI models:"
    Write-Host "  1. Download GGUF models (Llama, Mistral, etc.)" -ForegroundColor Yellow
    Write-Host "  2. Place them in: $modelsPath" -ForegroundColor Yellow
    Write-Host "  3. Restart the system" -ForegroundColor Yellow
    
    # Create model info file
    $modelInfo = @"
# AI Models for Juggernaut AI
# Place GGUF format models in this directory

RECOMMENDED MODELS:
==================

1. Llama-2-7B-Chat-GGUF (Recommended)
   - Size: ~4GB
   - Good balance of performance and quality
   - Download: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF

2. Mistral-7B-Instruct-GGUF (Alternative)
   - Size: ~4GB  
   - Fast inference, good for coding
   - Download: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF

3. CodeLlama-7B-Instruct-GGUF (Coding)
   - Size: ~4GB
   - Specialized for code generation
   - Download: https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF

INSTALLATION:
=============
1. Download .gguf files from HuggingFace
2. Place in this directory
3. Restart Juggernaut AI
4. Models will be auto-detected

PERFORMANCE NOTES:
==================
- RTX 4070 SUPER can handle 7B models efficiently
- 13B models possible with reduced GPU layers
- Monitor VRAM usage in system settings
"@

    Set-Content -Path "$modelsPath\README.txt" -Value $modelInfo -Encoding UTF8
    Write-Success "Model information created"
}

# Configure production environment
function Set-ProductionEnvironment {
    Write-Info "Configuring production environment..."
    
    # Update .env for production
    $prodEnv = Get-Content ".env" -Raw
    $prodEnv = $prodEnv -replace "DEBUG=false", "DEBUG=false"
    $prodEnv = $prodEnv -replace "LOG_LEVEL=INFO", "LOG_LEVEL=WARNING"
    Set-Content -Path ".env" -Value $prodEnv -Encoding UTF8

    # Create Windows service script
    $serviceScript = @"
# Juggernaut AI Windows Service
# Run as Windows Service for production

# Install NSSM (Non-Sucking Service Manager)
# Download from: https://nssm.cc/download

# Install service:
# nssm install JuggernautAI "$(Get-Location)\python.exe" "$(Get-Location)\app.py"
# nssm set JuggernautAI AppDirectory "$(Get-Location)"
# nssm set JuggernautAI DisplayName "Juggernaut AI System"
# nssm set JuggernautAI Description "RTX 4070 SUPER Optimized AI System"
# nssm start JuggernautAI

Write-Host "Production service configuration created"
Write-Host "Install NSSM and run the commands above to create Windows service"
"@

    Set-Content -Path "install_service.ps1" -Value $serviceScript -Encoding UTF8
    Write-Success "Production service script created"

    # Create startup batch file
    $startupBatch = @"
@echo off
title Juggernaut AI System
echo Starting Juggernaut AI System...
echo RTX 4070 SUPER Optimized Monster UI
echo.

cd /d "%~dp0"
python app.py

pause
"@

    Set-Content -Path "start_juggernaut.bat" -Value $startupBatch -Encoding ASCII
    Write-Success "Startup batch file created"
}

# Test installation
function Test-Installation {
    Write-Info "Testing installation..."
    
    # Test Python imports
    try {
        & python -c "import flask, core; print('✅ Core modules imported successfully')"
        Write-Success "Python modules test passed"
    } catch {
        Write-Warning "Python modules test failed - some features may not work"
    }

    # Test GPU
    if (Test-Path "test_gpu.py") {
        & python test_gpu.py
    }

    # Test directory structure
    $requiredDirs = @("$DataPath", "$DataPath\models", "$DataPath\chats", "logs")
    foreach ($dir in $requiredDirs) {
        if (Test-Path $dir) {
            Write-Success "Directory exists: $dir"
        } else {
            Write-Error "Missing directory: $dir"
        }
    }

    # Test configuration files
    $configFiles = @(".env", "config.json")
    foreach ($file in $configFiles) {
        if (Test-Path $file) {
            Write-Success "Configuration file: $file"
        } else {
            Write-Warning "Missing configuration: $file"
        }
    }
}

# Show startup instructions
function Show-StartupInstructions {
    Write-Host @"

🎉 JUGGERNAUT AI SETUP COMPLETE!
================================

🚀 TO START THE SYSTEM:
   python app.py

🌐 ACCESS THE INTERFACE:
   http://localhost:5000

📁 DATA DIRECTORY:
   $DataPath

⚙️  CONFIGURATION:
   Edit .env or config.json for custom settings

🤖 AI MODELS:
   Place GGUF models in: $DataPath\models\
   System runs in demo mode without models

🔧 GPU ACCELERATION:
   RTX 4070 SUPER optimization enabled
   35 GPU layers configured for 12GB VRAM

📖 DOCUMENTATION:
   See README.md for detailed usage instructions

🆘 SUPPORT:
   Check logs\ directory for troubleshooting
   Visit GitHub repository for updates

"@ -ForegroundColor Green

    # Create desktop shortcut (optional)
    $createShortcut = Read-Host "Create desktop shortcut? (y/n)"
    if ($createShortcut -eq 'y' -or $createShortcut -eq 'Y') {
        try {
            $WshShell = New-Object -comObject WScript.Shell
            $Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Juggernaut AI.lnk")
            $Shortcut.TargetPath = "$PWD\start_juggernaut.bat"
            $Shortcut.WorkingDirectory = $PWD
            $Shortcut.Description = "Juggernaut AI - RTX 4070 SUPER Optimized"
            $Shortcut.Save()
            Write-Success "Desktop shortcut created"
        } catch {
            Write-Warning "Could not create desktop shortcut"
        }
    }

    Write-Host "`n🚀 Ready to unleash RTX 4070 SUPER AI power!" -ForegroundColor Magenta
}

# Error handling
trap {
    Write-Error "Setup failed: $($_.Exception.Message)"
    Write-Host "Check setup.log for details" -ForegroundColor Yellow
    exit 1
}

# Start logging
Start-Transcript -Path "logs\setup.log" -Append -ErrorAction SilentlyContinue

# Run main setup
Start-JuggernautSetup

# Stop logging
Stop-Transcript -ErrorAction SilentlyContinue

Write-Host "`n✅ Setup completed successfully!" -ForegroundColor Green

