# Juggernaut AI Enhanced System - Setup Instructions

## 🚀 Quick Setup (5 Minutes)

### 1. Pull the Enhanced System
```powershell
cd D:\JuggernautAI
git pull origin main
```

### 2. Set Your Hugging Face Token
```powershell
# Get your token from: https://huggingface.co/settings/tokens
set HF_TOKEN=your_hugging_face_token_here
```

### 3. Test Everything Works
```powershell
# Test FLUX image generation (should work immediately)
python flux_hf_api.py "a red sports car"

# Test unified command processor
python unified_command_processor.py "help"

# Test natural language commands
python unified_command_processor.py "generate image of a sunset"

# Your original system (unchanged)
python juggernaut_web_fixed.py
```

## 🎯 What You Get

✅ **FLUX Image Generation** - High-quality AI images
✅ **Unified Command Processor** - Natural language interface
✅ **Discord Bot** - Mobile access (optional)
✅ **Your Original System** - Still works exactly the same

## 📱 Optional: Discord Bot Setup

1. **Create Discord Bot:**
   - Go to https://discord.com/developers/applications
   - Create new application and bot
   - Copy bot token

2. **Set Token and Run:**
   ```powershell
   set DISCORD_BOT_TOKEN=your_bot_token_here
   python discord_bot.py
   ```

## 🎨 Usage Examples

### Natural Language Commands
```powershell
python unified_command_processor.py "generate image of a futuristic city"
python unified_command_processor.py "create image: cat wearing business suit"
python unified_command_processor.py "start web interface"
python unified_command_processor.py "status"
```

### Direct FLUX Generation
```powershell
python flux_hf_api.py "a beautiful sunset"
python flux_hf_api.py "a dragon flying over mountains"
```

### Web Interface Integration
In your existing web interface, use:
```
Execute: python flux_hf_api.py "your prompt here"
Execute: python unified_command_processor.py "generate image of a car"
```

## 🔧 Files You'll Have

- **`flux_hf_api.py`** - FLUX image generator (secure)
- **`unified_command_processor.py`** - Natural language interface
- **`discord_bot.py`** - Mobile Discord bot
- **`README_ENHANCED.md`** - Complete documentation
- **`.env.example`** - Environment configuration template
- **`SETUP_INSTRUCTIONS.md`** - This file

## ✅ Everything Works

- Your original `juggernaut_web_fixed.py` works exactly as before
- FLUX image generation works with environment variables
- Unified processor provides natural language interface
- Discord bot gives you mobile access
- All secure with no hardcoded tokens

## 🆘 If Something Doesn't Work

1. **FLUX not working?** Make sure `HF_TOKEN` is set
2. **Files missing?** Run `git pull origin main` again
3. **Original system?** `python juggernaut_web_fixed.py` still works
4. **Need help?** Run `python unified_command_processor.py "help"`

---

**Simple, working, enhanced AI system that builds on what you already have!** 🚀

