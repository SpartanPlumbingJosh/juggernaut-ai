# Juggernaut AI - Setup Script
# PowerShell script for easy installation and setup

param(
    [string]$InstallPath = "C:\Projects\juggernaut_ai",
    [string]$GemmaModelPath = "",
    [switch]$SkipDependencies = $false
)

Write-Host "ðŸš€ Juggernaut AI Setup Script" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3\.([0-9]+)") {
        $minorVersion = [int]$matches[1]
        if ($minorVersion -ge 11) {
            Write-Host "âœ“ Python $pythonVersion found" -ForegroundColor Green
        } else {
            Write-Host "âŒ Python 3.11+ required. Found: $pythonVersion" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "âŒ Python not found. Please install Python 3.11+" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "âŒ Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Create installation directory
Write-Host "Creating installation directory..." -ForegroundColor Yellow
if (!(Test-Path $InstallPath)) {
    New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
    Write-Host "âœ“ Created directory: $InstallPath" -ForegroundColor Green
} else {
    Write-Host "âœ“ Directory exists: $InstallPath" -ForegroundColor Green
}

# Copy project files (assuming they're in the current directory)
Write-Host "Copying project files..." -ForegroundColor Yellow
$sourceFiles = @(
    "app.py",
    "ai_engine.py",
    "browser_controller.py", 
    "chat_manager.py",
    "file_manager.py",
    "plugin_manager.py",
    "requirements.txt"
)

foreach ($file in $sourceFiles) {
    if (Test-Path $file) {
        Copy-Item $file $InstallPath -Force
        Write-Host "âœ“ Copied $file" -ForegroundColor Green
    } else {
        Write-Host "âš  Warning: $file not found" -ForegroundColor Yellow
    }
}

# Create directory structure
Write-Host "Creating directory structure..." -ForegroundColor Yellow
$directories = @("templates", "static", "data", "data\chats", "data\files", "data\images", "data\plugins", "logs")
foreach ($dir in $directories) {
    $fullPath = Join-Path $InstallPath $dir
    if (!(Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Host "âœ“ Created directory: $dir" -ForegroundColor Green
    }
}

# Copy frontend files
Write-Host "Copying frontend files..." -ForegroundColor Yellow
if (Test-Path "templates\index.html") {
    Copy-Item "templates\index.html" "$InstallPath\templates\" -Force
    Write-Host "âœ“ Copied templates/index.html" -ForegroundColor Green
}
if (Test-Path "static\app.css") {
    Copy-Item "static\app.css" "$InstallPath\static\" -Force
    Write-Host "âœ“ Copied static/app.css" -ForegroundColor Green
}
if (Test-Path "static\app.js") {
    Copy-Item "static\app.js" "$InstallPath\static\" -Force
    Write-Host "âœ“ Copied static/app.js" -ForegroundColor Green
}

# Install Python dependencies
if (!$SkipDependencies) {
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    Set-Location $InstallPath
    
    try {
        pip install flask flask_cors requests pillow openpyxl python-docx pdfplumber watchdog tqdm selenium webdriver-manager psutil pydub pyttsx3 pandas
        Write-Host "âœ“ Dependencies installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "âŒ Failed to install dependencies. Please run manually:" -ForegroundColor Red
        Write-Host "pip install flask flask_cors requests pillow openpyxl python-docx pdfplumber watchdog tqdm selenium webdriver-manager psutil pydub pyttsx3 pandas" -ForegroundColor Yellow
    }
}

# Configure Gemma model path if provided
if ($GemmaModelPath -ne "") {
    Write-Host "Configuring Gemma model path..." -ForegroundColor Yellow
    $aiEngineFile = Join-Path $InstallPath "ai_engine.py"
    if (Test-Path $aiEngineFile) {
        $content = Get-Content $aiEngineFile -Raw
        $content = $content -replace 'model_path="[^"]*"', "model_path=`"$GemmaModelPath`""
        Set-Content $aiEngineFile $content
        Write-Host "âœ“ Updated Gemma model path to: $GemmaModelPath" -ForegroundColor Green
    }
}

# Create startup script
Write-Host "Creating startup script..." -ForegroundColor Yellow
$startupScript = @"
# Juggernaut AI Startup Script
Write-Host "ðŸš€ Starting Juggernaut AI..." -ForegroundColor Green
Set-Location "$InstallPath"
python app.py
"@

$startupScriptPath = Join-Path $InstallPath "start_juggernaut.ps1"
Set-Content $startupScriptPath $startupScript
Write-Host "âœ“ Created startup script: start_juggernaut.ps1" -ForegroundColor Green

# Create desktop shortcut (optional)
$createShortcut = Read-Host "Create desktop shortcut? (y/n)"
if ($createShortcut -eq "y" -or $createShortcut -eq "Y") {
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "Juggernaut AI.lnk"
    
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($shortcutPath)
    $Shortcut.TargetPath = "powershell.exe"
    $Shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$startupScriptPath`""
    $Shortcut.WorkingDirectory = $InstallPath
    $Shortcut.IconLocation = "powershell.exe,0"
    $Shortcut.Description = "Juggernaut AI - Monster UI"
    $Shortcut.Save()
    
    Write-Host "âœ“ Desktop shortcut created" -ForegroundColor Green
}

Write-Host ""
Write-Host "ðŸŽ‰ Setup Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host "Installation Path: $InstallPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start Juggernaut AI:" -ForegroundColor Yellow
Write-Host "1. Open PowerShell" -ForegroundColor White
Write-Host "2. Navigate to: $InstallPath" -ForegroundColor White
Write-Host "3. Run: .\start_juggernaut.ps1" -ForegroundColor White
Write-Host "4. Open browser to: http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "Or simply double-click the desktop shortcut if created." -ForegroundColor Yellow
Write-Host ""

# Offer to start immediately
$startNow = Read-Host "Start Juggernaut AI now? (y/n)"
if ($startNow -eq "y" -or $startNow -eq "Y") {
    Write-Host "Starting Juggernaut AI..." -ForegroundColor Green
    Set-Location $InstallPath
    python app.py
}


