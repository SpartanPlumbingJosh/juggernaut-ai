@echo off
REM Juggernaut AI - Quick Start (Alternative launcher)
REM Minimal startup for taskbar pinning

title Juggernaut AI

REM Change to Juggernaut directory
cd /d "D:\JuggernautAI"

REM Quick check and start
if exist "juggernaut_real_fixed.py" (
    echo Starting Juggernaut AI...
    echo Web interface: http://localhost:5000
    python juggernaut_real_fixed.py
) else (
    echo ERROR: Juggernaut AI not found in D:\JuggernautAI
    pause
)

