# Juggernaut AI - Simple Installer
# This script installs the Juggernaut AI Desktop Launcher

Write-Host "🤖 Installing Juggernaut AI Desktop Launcher..." -ForegroundColor Red

# Create desktop shortcut
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Juggernaut AI.lnk"

# Get current directory
$CurrentDir = Get-Location

# Create shortcut
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "python"
$Shortcut.Arguments = "`"$CurrentDir\juggernaut_launcher.py`""
$Shortcut.WorkingDirectory = $CurrentDir
$Shortcut.IconLocation = "python.exe,0"
$Shortcut.Description = "Juggernaut AI - One-Click Launcher"
$Shortcut.Save()

Write-Host "✅ Desktop shortcut created: $ShortcutPath" -ForegroundColor Green

# Create start menu shortcut
$StartMenuPath = [Environment]::GetFolderPath("StartMenu")
$ProgramsPath = Join-Path $StartMenuPath "Programs"
$JuggernautFolder = Join-Path $ProgramsPath "Juggernaut AI"

if (!(Test-Path $JuggernautFolder)) {
    New-Item -ItemType Directory -Path $JuggernautFolder -Force
}

$StartMenuShortcut = Join-Path $JuggernautFolder "Juggernaut AI Launcher.lnk"
$StartShortcut = $WshShell.CreateShortcut($StartMenuShortcut)
$StartShortcut.TargetPath = "python"
$StartShortcut.Arguments = "`"$CurrentDir\juggernaut_launcher.py`""
$StartShortcut.WorkingDirectory = $CurrentDir
$StartShortcut.IconLocation = "python.exe,0"
$StartShortcut.Description = "Juggernaut AI - One-Click Launcher"
$StartShortcut.Save()

Write-Host "✅ Start menu shortcut created: $StartMenuShortcut" -ForegroundColor Green

# Create batch file for easy launching
$BatchFile = Join-Path $CurrentDir "Launch Juggernaut AI.bat"
$BatchContent = @"
@echo off
cd /d "$CurrentDir"
python juggernaut_launcher.py
pause
"@

Set-Content -Path $BatchFile -Value $BatchContent
Write-Host "✅ Batch launcher created: $BatchFile" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Installation Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "You can now start Juggernaut AI by:" -ForegroundColor Yellow
Write-Host "  • Double-clicking the desktop shortcut" -ForegroundColor White
Write-Host "  • Using the Start menu shortcut" -ForegroundColor White
Write-Host "  • Running 'Launch Juggernaut AI.bat'" -ForegroundColor White
Write-Host "  • Running 'python juggernaut_launcher.py'" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Ready to launch your AI assistant!" -ForegroundColor Red

