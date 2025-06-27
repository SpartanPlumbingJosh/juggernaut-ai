@echo off
REM Juggernaut AI - Taskbar Launcher (FIXED VERSION)
REM Pin this file to your taskbar for one-click startup

title Juggernaut AI - Starting...

echo.
echo ========================================
echo    JUGGERNAUT AI - STARTING SYSTEM
echo ========================================
echo.
echo RTX 4070 SUPER AI System
echo Real Gemma 2-9B-IT Integration
echo Professional Monster UI
echo.

REM Change to the Juggernaut AI directory
cd /d "D:\JuggernautAI"

REM Check if we're in the right directory
if not exist "juggernaut_real_fixed.py" (
    echo ERROR: Juggernaut AI files not found!
    echo Please ensure this file is in D:\JuggernautAI
    echo.
    pause
    exit /b 1
)

echo Starting Juggernaut AI System...
echo.
echo Web interface will be available at:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the system
echo ========================================
echo.

REM Start the FIXED Juggernaut AI system with correct model path
python juggernaut_real_fixed.py

REM If the system stops, show a message
echo.
echo ========================================
echo Juggernaut AI system has stopped.
echo ========================================
pause

