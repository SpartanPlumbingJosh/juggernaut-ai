# 🖥️ Juggernaut AI Desktop Launcher

**Super Simple One-Click Startup for Juggernaut AI!**

No more command line needed - just double-click and go!

## 🚀 Quick Setup (30 seconds)

### Option 1: Automatic Installation (Recommended)
```powershell
# 1. Clone the repository
git clone https://github.com/SpartanPlumbingJosh/juggernaut-ai.git
cd juggernaut-ai

# 2. Run the installer
.\simple_installer.ps1
```

### Option 2: Manual Setup
```powershell
# 1. Clone the repository
git clone https://github.com/SpartanPlumbingJosh/juggernaut-ai.git
cd juggernaut-ai

# 2. Install dependencies
pip install Flask Flask-CORS psutil Werkzeug requests Pillow python-multipart

# 3. Run the launcher
python juggernaut_launcher.py
```

## 🎯 What You Get

### Professional Desktop Launcher
- **🤖 Beautiful GUI** - Dark theme with red Juggernaut branding
- **🚀 One-Click Start** - No command line needed
- **⏹️ Easy Stop** - Clean shutdown with one click
- **🌐 Auto-Open Browser** - Automatically opens web interface
- **📊 Real-Time Monitoring** - System status and logs
- **🔄 Hot Reload Ready** - Automatic GitHub updates

### Multiple Launch Options
- **Desktop Shortcut** - Double-click to start
- **Start Menu** - Find in Programs > Juggernaut AI
- **Batch File** - "Launch Juggernaut AI.bat"
- **Direct Python** - `python juggernaut_launcher.py`

## 📱 Launcher Interface

```
🤖 JUGGERNAUT AI LAUNCHER
┌─────────────────────────────────┐
│ 🔴 System: Stopped              │
│ 🎮 GPU: RTX 4070 SUPER (12GB)   │
│ 🧠 Model: Gemma 3 (Ready)       │
│ 🌐 URL: http://localhost:5000   │
└─────────────────────────────────┘

[🚀 START JUGGERNAUT AI] [⏹️ STOP SYSTEM] [🌐 OPEN INTERFACE]

📋 System Logs
┌─────────────────────────────────┐
│ [00:24:15] 🤖 Launcher ready    │
│ [00:24:16] 🚀 Starting system   │
│ [00:24:18] ✅ System running    │
│ [00:24:19] 🌐 Interface opened  │
└─────────────────────────────────┘
```

## ⚡ Features

### System Management
- **Start/Stop Control** - One-click system management
- **Status Monitoring** - Real-time system health
- **Log Viewing** - Live system logs with timestamps
- **Error Handling** - Graceful error management
- **Process Monitoring** - Background Flask monitoring

### User Experience
- **Auto-Detection** - Finds app.py automatically
- **Smart Startup** - Waits for system ready before opening browser
- **Clean Shutdown** - Proper process termination
- **Visual Feedback** - Color-coded status indicators
- **Professional UI** - Modern dark theme interface

## 🔧 Advanced Options

### Create Windows Executable
```powershell
# Run the executable creator
.\create_executable.ps1
```

This creates a standalone `.exe` file that doesn't require Python to be installed.

### Customization
Edit `juggernaut_launcher.py` to customize:
- Window size and appearance
- Status check intervals
- Log display options
- Button colors and text

## 🎯 Perfect For

- **Non-Technical Users** - No command line knowledge needed
- **Daily Use** - Quick startup for regular AI sessions
- **Development** - Easy testing and debugging
- **Demonstrations** - Professional presentation of Juggernaut AI
- **Production** - Reliable system management

## 🚀 Next Steps

1. **Install the launcher** using the quick setup above
2. **Double-click the desktop shortcut** to start Juggernaut AI
3. **Enjoy your one-click AI assistant!**

The launcher will:
- ✅ Start the Flask backend
- ✅ Initialize all AI components
- ✅ Open the web interface automatically
- ✅ Monitor system health
- ✅ Provide easy shutdown

**No more command line - just click and go!** 🎉

