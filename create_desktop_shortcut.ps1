# Create Desktop Shortcut for Juggernaut AI
# Creates a one-click desktop shortcut for easy access
# Author: Manus AI
# Date: June 27, 2025

Write-Host "========================================" -ForegroundColor Green
Write-Host "   CREATING DESKTOP SHORTCUT" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Define paths
$juggernautPath = "D:\JuggernautAI"
$batchFile = "$juggernautPath\Start_Juggernaut_AI.bat"
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = "$desktopPath\Juggernaut AI.lnk"

# Check if batch file exists
if (-not (Test-Path $batchFile)) {
    Write-Host "ERROR: Batch file not found at: $batchFile" -ForegroundColor Red
    Write-Host "Please ensure Juggernaut AI is properly installed." -ForegroundColor Yellow
    exit 1
}

Write-Host "Creating desktop shortcut..." -ForegroundColor Cyan

try {
    # Create WScript Shell object
    $WshShell = New-Object -comObject WScript.Shell
    
    # Create shortcut
    $Shortcut = $WshShell.CreateShortcut($shortcutPath)
    $Shortcut.TargetPath = $batchFile
    $Shortcut.WorkingDirectory = $juggernautPath
    $Shortcut.Description = "Juggernaut AI - One-Click Launcher"
    $Shortcut.IconLocation = "$env:SystemRoot\System32\shell32.dll,25"  # Computer icon
    
    # Save shortcut
    $Shortcut.Save()
    
    Write-Host "SUCCESS: Desktop shortcut created!" -ForegroundColor Green
    Write-Host "Location: $shortcutPath" -ForegroundColor Gray
    Write-Host ""
    Write-Host "You can now double-click 'Juggernaut AI' on your desktop to start the system!" -ForegroundColor Yellow
    
} catch {
    Write-Host "ERROR: Failed to create desktop shortcut" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Desktop shortcut setup completed!" -ForegroundColor Green

