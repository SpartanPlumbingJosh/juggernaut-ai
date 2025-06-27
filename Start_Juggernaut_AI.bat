@echo off
title JUGGERNAUT AI - One-Click Launcher
color 0C

echo ========================================
echo    JUGGERNAUT AI - ONE-CLICK LAUNCHER
echo ========================================
echo.
echo RTX 4070 SUPER AI System
echo Real Gemma 3 via Ollama
echo Professional Monster UI
echo.

REM Change to Juggernaut directory
cd /d D:\JuggernautAI

REM Check if we're in the right directory
if not exist "juggernaut_ollama.py" (
    echo ERROR: Juggernaut AI files not found in D:\JuggernautAI
    echo Please ensure the system is properly installed.
    echo.
    pause
    exit /b 1
)

echo Starting Juggernaut AI System...
echo.
echo Web interface: http://localhost:5000
echo.
echo System will start in 3 seconds...
timeout /t 3 /nobreak >nul

REM Start the Ollama-based Juggernaut system
python juggernaut_ollama.py

echo.
echo System stopped. Press any key to exit...
pause >nul

