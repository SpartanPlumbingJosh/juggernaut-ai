# Create Desktop Shortcut for Juggernaut AI
# Run this script to create a desktop icon

param(
    [string]$InstallPath = (Get-Location).Path
)

Write-Host "Creating Juggernaut AI Desktop Shortcut..." -ForegroundColor Green

# Get desktop path
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Juggernaut AI.lnk"

# Create shortcut
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "python"
$Shortcut.Arguments = "`"$InstallPath\desktop_launcher.py`""
$Shortcut.WorkingDirectory = $InstallPath
$Shortcut.Description = "Juggernaut AI - RTX 4070 SUPER Powered AI Assistant"
$Shortcut.WindowStyle = 1

# Try to set icon if available
$IconPath = Join-Path $InstallPath "static\juggernaut_icon.ico"
if (Test-Path $IconPath) {
    $Shortcut.IconLocation = $IconPath
}

$Shortcut.Save()

Write-Host "SUCCESS: Desktop shortcut created at: $ShortcutPath" -ForegroundColor Green
Write-Host "You can now double-click the desktop icon to start Juggernaut AI!" -ForegroundColor Cyan

# Also create Start Menu shortcut
$StartMenuPath = [Environment]::GetFolderPath("StartMenu")
$ProgramsPath = Join-Path $StartMenuPath "Programs"
$StartShortcutPath = Join-Path $ProgramsPath "Juggernaut AI.lnk"

$StartShortcut = $WshShell.CreateShortcut($StartShortcutPath)
$StartShortcut.TargetPath = "python"
$StartShortcut.Arguments = "`"$InstallPath\desktop_launcher.py`""
$StartShortcut.WorkingDirectory = $InstallPath
$StartShortcut.Description = "Juggernaut AI - RTX 4070 SUPER Powered AI Assistant"
$StartShortcut.WindowStyle = 1

if (Test-Path $IconPath) {
    $StartShortcut.IconLocation = $IconPath
}

$StartShortcut.Save()

Write-Host "SUCCESS: Start Menu shortcut created" -ForegroundColor Green
Write-Host ""
Write-Host "INSTALLATION COMPLETE!" -ForegroundColor Yellow
Write-Host "- Desktop shortcut: Double-click to start" -ForegroundColor White
Write-Host "- Start Menu: Search for 'Juggernaut AI'" -ForegroundColor White
Write-Host "- Manual start: python desktop_launcher.py" -ForegroundColor White

