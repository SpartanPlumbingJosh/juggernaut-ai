# Juggernaut AI - Model Setup Guide

## 🤖 AI Model Configuration

Juggernaut AI is designed to work with your locally downloaded AI models. The models are **NOT** included in this repository due to their large size (several GB each).

## 📁 Model Locations

The system will automatically search for your Gemma 3 model in these locations:

### Primary Location (Recommended):
```
D:/Juggernaut_AI/models/ai_models/text/gemma_2_9b_gguf/gemma-2-9b-it-Q4_K_M.gguf
```

### Alternative Locations:
```
D:/JuggernautAI/models/gemma-2-9b-it-Q4_K_M.gguf
D:/models/gemma-2-9b-it-Q4_K_M.gguf
./models/gemma-2-9b-it-Q4_K_M.gguf
```

## 🔧 Setup Instructions

### 1. Download Gemma 3 Model
- Download the Gemma 2 9B model in GGUF format
- Recommended: `gemma-2-9b-it-Q4_K_M.gguf` (balanced quality/speed)
- Sources: Hugging Face, LM Studio, or other GGUF repositories

### 2. Place Model File
Create the directory structure and place your model:
```powershell
# Create the directory
mkdir "D:\Juggernaut_AI\models\ai_models\text\gemma_2_9b_gguf"

# Copy your downloaded model file to:
# D:\Juggernaut_AI\models\ai_models\text\gemma_2_9b_gguf\gemma-2-9b-it-Q4_K_M.gguf
```

### 3. Install Dependencies (Optional)
For full GPU acceleration with your RTX 4070 SUPER:
```powershell
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
```

## ⚡ RTX 4070 SUPER Optimization

The system is pre-configured for optimal performance on RTX 4070 SUPER:
- **GPU Layers:** 35 (optimized for 12GB VRAM)
- **Context Window:** 4096 tokens
- **Quantization:** Q4_K_M for best speed/quality balance
- **Memory Management:** Efficient VRAM utilization

## 🎯 Demo Mode

If no model is found, Juggernaut AI will run in **Demo Mode**:
- ✅ Full UI functionality
- ✅ All features working
- ✅ Simulated AI responses
- ⚠️ No real AI model processing

## 🔍 Troubleshooting

### Model Not Found
If you see "Model file not found" in the logs:
1. Check the file path matches exactly
2. Ensure the file isn't corrupted
3. Verify file permissions
4. Try placing in alternative locations

### GPU Not Working
If GPU acceleration isn't working:
1. Install `llama-cpp-python` with CUDA support
2. Verify NVIDIA drivers are updated
3. Check CUDA installation
4. Restart the system after installation

### Memory Issues
If you encounter VRAM issues:
- Reduce GPU layers (try 30 or 25)
- Close other GPU-intensive applications
- Monitor VRAM usage in Task Manager

## 📊 Model Information

### Recommended Model: Gemma 2 9B IT Q4_K_M
- **Size:** ~5.5GB
- **Quality:** High
- **Speed:** Fast on RTX 4070 SUPER
- **VRAM Usage:** ~6-8GB
- **Context:** 4096 tokens

### Alternative Models
You can use other GGUF models by updating the filename in the code:
- Gemma 2 2B (smaller, faster)
- Gemma 2 27B (larger, higher quality)
- Other Llama/Mistral models in GGUF format

## 🚀 Getting Started

1. **Download and place your model** in the recommended location
2. **Start Juggernaut AI** using the desktop launcher
3. **Check the logs** to confirm model loading
4. **Enjoy your RTX 4070 SUPER powered AI assistant!**

## 💡 Tips

- **First startup** may take longer as the model loads into VRAM
- **Keep models on SSD** for faster loading times
- **Monitor temperatures** during intensive AI workloads
- **Use demo mode** to test the interface before model setup

---

**Need help?** Check the main README.md for additional setup instructions and troubleshooting.

