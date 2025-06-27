# Juggernaut AI - Taskbar Integration Setup
# Creates desktop shortcuts, taskbar integration, and Start Menu entries

param(
    [switch]$Silent = $false
)

# Function to write colored output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

if (-not $Silent) {
    Clear-Host
    Write-ColorOutput Red @"
========================================
   JUGGERNAUT AI TASKBAR INTEGRATION
========================================
"@
    Write-ColorOutput Yellow "Setting up taskbar and desktop shortcuts..."
    Write-Output ""
}

# Get current directory (should be D:\JuggernautAI)
$JuggernautDir = Get-Location
$BatchFile = Join-Path $JuggernautDir "Start_Juggernaut_AI.bat"
$IconFile = Join-Path $JuggernautDir "juggernaut_icon.ico"

# Check if batch file exists
if (-not (Test-Path $BatchFile)) {
    Write-ColorOutput Red "ERROR: Start_Juggernaut_AI.bat not found!"
    Write-Output "Please ensure you're running this from the JuggernautAI directory."
    if (-not $Silent) { pause }
    exit 1
}

# Create desktop shortcut
try {
    $WshShell = New-Object -comObject WScript.Shell
    $DesktopPath = [System.Environment]::GetFolderPath('Desktop')
    $ShortcutPath = Join-Path $DesktopPath "Juggernaut AI.lnk"
    
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $BatchFile
    $Shortcut.WorkingDirectory = $JuggernautDir
    $Shortcut.Description = "Juggernaut AI - RTX 4070 SUPER Powered AI System"
    $Shortcut.WindowStyle = 1  # Normal window
    
    # Set icon if it exists
    if (Test-Path $IconFile) {
        $Shortcut.IconLocation = $IconFile
    }
    
    $Shortcut.Save()
    
    if (-not $Silent) {
        Write-ColorOutput Green "✓ Desktop shortcut created: $ShortcutPath"
    }
} catch {
    Write-ColorOutput Red "✗ Failed to create desktop shortcut: $($_.Exception.Message)"
}

# Create Start Menu shortcut
try {
    $StartMenuPath = [System.Environment]::GetFolderPath('StartMenu')
    $ProgramsPath = Join-Path $StartMenuPath "Programs"
    $JuggernautStartPath = Join-Path $ProgramsPath "Juggernaut AI.lnk"
    
    $StartShortcut = $WshShell.CreateShortcut($JuggernautStartPath)
    $StartShortcut.TargetPath = $BatchFile
    $StartShortcut.WorkingDirectory = $JuggernautDir
    $StartShortcut.Description = "Juggernaut AI - RTX 4070 SUPER Powered AI System"
    $StartShortcut.WindowStyle = 1
    
    if (Test-Path $IconFile) {
        $StartShortcut.IconLocation = $IconFile
    }
    
    $StartShortcut.Save()
    
    if (-not $Silent) {
        Write-ColorOutput Green "✓ Start Menu shortcut created"
    }
} catch {
    Write-ColorOutput Red "✗ Failed to create Start Menu shortcut: $($_.Exception.Message)"
}

# Instructions for taskbar pinning
if (-not $Silent) {
    Write-Output ""
    Write-ColorOutput Cyan @"
========================================
   TASKBAR PINNING INSTRUCTIONS
========================================
"@
    Write-Output ""
    Write-ColorOutput Yellow "OPTION 1: Pin Batch File to Taskbar"
    Write-Output "1. Right-click on 'Start_Juggernaut_AI.bat'"
    Write-Output "2. Select 'Pin to taskbar'"
    Write-Output ""
    
    Write-ColorOutput Yellow "OPTION 2: Pin Desktop Shortcut to Taskbar"
    Write-Output "1. Find 'Juggernaut AI' shortcut on your desktop"
    Write-Output "2. Drag it to your taskbar"
    Write-Output ""
    
    Write-ColorOutput Yellow "OPTION 3: Pin from Start Menu"
    Write-Output "1. Click Start Menu"
    Write-Output "2. Find 'Juggernaut AI' in the programs list"
    Write-Output "3. Right-click and select 'Pin to taskbar'"
    Write-Output ""
    
    Write-ColorOutput Green @"
========================================
   SETUP COMPLETE!
========================================
"@
    Write-Output ""
    Write-ColorOutput Cyan "Your Juggernaut AI system is now ready for taskbar access!"
    Write-Output ""
    Write-ColorOutput Yellow "To start Juggernaut AI:"
    Write-Output "• Double-click the desktop shortcut"
    Write-Output "• Click the taskbar icon (after pinning)"
    Write-Output "• Run Start_Juggernaut_AI.bat directly"
    Write-Output ""
    Write-ColorOutput Cyan "The system will start and be available at: http://localhost:5000"
    Write-Output ""
    
    pause
}

Write-ColorOutput Green "Taskbar integration setup completed successfully!"

