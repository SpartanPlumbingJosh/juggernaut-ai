# Juggernaut AI - PowerShell Setup Commands

## Quick Start Commands

Here are the essential PowerShell commands to get your Juggernaut AI project running. Copy and paste these commands in order:

### 1. Set Execution Policy (Run as Administrator)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Navigate to Your Project Directory
```powershell
# Change this path to where you extracted your files
cd "C:\Path\To\Your\Extracted\Files"
```

### 3. Run the Setup Script
```powershell
.\setup_juggernaut.ps1
```

## Alternative Manual Setup Commands

If the automated script doesn't work, use these manual commands:

### Create Project Directory
```powershell
$InstallPath = "C:\Projects\juggernaut_ai"
New-Item -ItemType Directory -Path $InstallPath -Force
```

### Copy All Project Files
```powershell
# Copy main Python files
Copy-Item "app.py" $InstallPath -Force
Copy-Item "ai_engine.py" $InstallPath -Force
Copy-Item "browser_controller.py" $InstallPath -Force
Copy-Item "chat_manager.py" $InstallPath -Force
Copy-Item "file_manager.py" $InstallPath -Force
Copy-Item "plugin_manager.py" $InstallPath -Force
Copy-Item "requirements.txt" $InstallPath -Force

# Copy frontend files
Copy-Item "index.html" "$InstallPath\templates\" -Force
Copy-Item "app.css" "$InstallPath\static\" -Force
Copy-Item "app.js" "$InstallPath\static\" -Force
```

### Create Directory Structure
```powershell
$directories = @("templates", "static", "data", "data\chats", "data\files", "data\images", "data\plugins", "logs")
foreach ($dir in $directories) {
    $fullPath = Join-Path $InstallPath $dir
    New-Item -ItemType Directory -Path $fullPath -Force
}
```

### Install Python Dependencies
```powershell
cd $InstallPath
pip install flask flask_cors requests pillow openpyxl python-docx pdfplumber watchdog tqdm selenium webdriver-manager psutil pydub pyttsx3 pandas torch transformers sentencepiece protobuf accelerate opencv-python
```

### Start the Application
```powershell
cd $InstallPath
python app.py
```

## Troubleshooting Commands

### Check Python Version
```powershell
python --version
```

### Check if Flask is Installed
```powershell
pip show flask
```

### Install Missing Dependencies
```powershell
pip install -r requirements.txt
```

### Force Reinstall All Dependencies
```powershell
pip install --force-reinstall -r requirements.txt
```

## Creating a Startup Script

Create a file called `start_juggernaut.ps1` with this content:

```powershell
# Juggernaut AI Startup Script
Write-Host "🚀 Starting Juggernaut AI..." -ForegroundColor Green
Set-Location "C:\Projects\juggernaut_ai"
python app.py
```

Then run it with:
```powershell
.\start_juggernaut.ps1
```

## Access Your Application

Once running, open your browser to:
```
http://localhost:5000
```

