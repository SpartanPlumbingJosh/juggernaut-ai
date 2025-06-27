# Juggernaut AI - Auto-Update System

## NO MORE POWERSHELL COMMANDS!

This system automatically updates from GitHub without any PowerShell commands. Just double-click and run!

## 🚀 ONE-CLICK OPERATION

### Method 1: One-Click Launcher (Recommended)
```
Double-click: juggernaut_launcher.exe.py
```

**Features:**
- ✅ GUI interface with status updates
- ✅ Automatic GitHub update checking
- ✅ One-click start/stop
- ✅ Real-time system logs
- ✅ No PowerShell required

### Method 2: Auto-Updater Direct
```
Double-click: auto_updater.py
```

**Features:**
- ✅ Command-line auto-updater
- ✅ Background GitHub monitoring
- ✅ Automatic system restart on updates
- ✅ 5-minute update intervals

## 🔄 HOW AUTO-UPDATES WORK

1. **Background Monitoring**: System checks GitHub every 5 minutes
2. **Automatic Download**: New commits are downloaded automatically
3. **Smart Backup**: Current version is backed up before update
4. **Seamless Update**: New code is applied without interruption
5. **Auto Restart**: System restarts with new version
6. **Dependency Management**: Requirements are updated automatically

## 📁 FILE STRUCTURE

```
D:\JuggernautAI\
├── juggernaut_launcher.exe.py    # One-click GUI launcher
├── auto_updater.py               # Auto-update engine
├── juggernaut_real.py           # Main AI system (REAL Gemma)
├── real_gemma_engine.py         # REAL AI engine
├── requirements_real.txt        # Dependencies
├── templates/                   # Web interface
├── static/                      # UI assets
├── backup/                      # Automatic backups
└── .current_commit             # Version tracking
```

## 🎯 WHAT GETS AUTO-UPDATED

- ✅ Main AI system code
- ✅ Gemma engine improvements
- ✅ Web interface updates
- ✅ Bug fixes and optimizations
- ✅ New features
- ✅ Dependencies (when needed)

## 🛡️ SAFETY FEATURES

- **Automatic Backups**: Every update creates a timestamped backup
- **Rollback Capability**: Can restore previous version if needed
- **Safe Updates**: Only updates when new commits are available
- **Error Handling**: Continues with current version if update fails
- **Dependency Checking**: Ensures all requirements are met

## 🔧 CONFIGURATION

The system automatically detects your configuration:

- **Model Path**: `D:/Juggernaut_AI/models/ai_models/text/gemma_2_9b_gguf/gemma-2-9b-it-Q4_K_M.gguf`
- **Data Directory**: `D:/JUGGERNAUT_DATA`
- **GPU Layers**: `35` (RTX 4070 SUPER optimized)
- **Update Interval**: `5 minutes`

## 🚨 TROUBLESHOOTING

### If Auto-Update Fails:
1. Check internet connection
2. Verify GitHub repository access
3. Check disk space for updates
4. Review logs in `auto_updater.log`

### If System Won't Start:
1. Run `install_real_gemma.py` to fix dependencies
2. Check model file exists at configured path
3. Verify Python and pip are working
4. Check `juggernaut_real.log` for errors

### Manual Update (Emergency):
If auto-update fails, you can still manually update:
1. Download latest ZIP from GitHub
2. Extract to temporary folder
3. Copy files to your JuggernautAI directory
4. Run `install_real_gemma.py`

## 📊 SYSTEM MONITORING

The launcher shows real-time status:
- ✅ **Green**: System running normally
- 🟡 **Yellow**: Checking for updates
- 🔴 **Red**: Error or stopped

## 🎉 BENEFITS

- **Zero Maintenance**: No manual updates needed
- **Always Current**: Latest features and fixes automatically
- **No Interruption**: Updates happen seamlessly
- **Safe Operation**: Automatic backups protect your setup
- **Simple Usage**: Just double-click to run

## 🔗 GITHUB INTEGRATION

- **Repository**: `SpartanPlumbingJosh/juggernaut-ai`
- **Branch**: `main`
- **Update Source**: GitHub releases and commits
- **Download Method**: Direct ZIP download (no git required)

---

**🎯 RESULT: NO MORE POWERSHELL COMMANDS!**

Just double-click `juggernaut_launcher.exe.py` and everything works automatically!

