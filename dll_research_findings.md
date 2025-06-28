# llama-cpp-python DLL Dependency Research

## Issue Summary
The user is experiencing a persistent "Could not find module 'llama.dll' (or one of its dependencies)" error when trying to import llama-cpp-python on Windows with RTX 4070 SUPER.

## Key Findings from GitHub Issue #1150

### Problem Description
- Error occurs during import: `from llama_cpp import Llama`
- Error message: "Failed to load shared library 'llama.dll': Could not find module 'llama.dll' (or one of its dependencies)"
- The DLL file exists but its dependencies cannot be found
- Affects Windows 10/11 systems with CUDA installations

### Solutions Found

#### Solution 1: NVCC Environment Variable (puff-dayo)
```bash
$env:CMAKE_ARGS="-DLLAMA_CUBLAS=on"
$env:CUDACXX="C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin\nvcc.exe"
python -m pip install llama-cpp-python --prefer-binary --no-cache-dir --extra-index-url=https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/AVX2/cu118
```

#### Solution 2: CUDA_PATH Environment Variable (GromoshtanniK)
- Set ENV variable CUDA_PATH to cuda installation
- Comment out `cdll_args["winmode"] = ctypes.RTLD_GLOBAL` in llama_cpp.py

#### Solution 3: Reinstall CUDA Toolkit (GheorgheMorari)
- The issue is that llama.dll depends on CUDA toolkit
- Solution: Install NVIDIA CUDA toolkit and restart
- URL: https://developer.nvidia.com/cuda-downloads

### Root Cause Analysis
The core issue is that llama.dll has dependencies on CUDA runtime libraries that are not being found by the Windows DLL loader, even when:
1. CUDA Toolkit is installed
2. Visual C++ Redistributables are installed  
3. The llama.dll file exists

## User's Current State
- Windows system with RTX 4070 SUPER
- CUDA Toolkit 12.4 installed
- Visual C++ 2022 Redistributables installed
- llama.dll file exists in the correct location
- Multiple Visual Studio installations (BuildTools and Community)

## Next Research Steps
1. Investigate CUDA runtime DLL dependencies specifically
2. Research Windows DLL loading path issues
3. Find definitive solution for CUDA 12.4 + RTX 4070 SUPER



## Solution 4: Build from Source (Eddie Offermann - Medium)

### Key Insight
The article explains that there is **no official wheel for llama-cpp with GPU support** due to the many possible configurations (different GPUs, CUDA versions, etc.). This explains why pre-built wheels often have DLL dependency issues.

### Build from Source Steps
1. **Environment Setup**
   ```bash
   conda create -n llamaconda python=3.10.11
   conda activate llamaconda
   ```

2. **Clone with Submodules**
   ```bash
   git clone --recurse-submodules https://github.com/abetlen/llama-cpp-python.git
   cd llama-cpp-python
   ```

3. **Install Build Tools**
   ```bash
   pip install cmake ninja
   ```
   - Requires Visual Studio 2019 with "Desktop development with C++" workload

4. **Set Environment Variables**
   ```bash
   set CUDA_HOME=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.3
   set PATH=%CUDA_HOME%\bin;%PATH%
   set PATH=%CUDA_HOME%\libnvvp;%PATH%
   set FORCE_CMAKE=1
   set CMAKE_ARGS=-DGGML_CUDA=on
   set GGML_CUDA=1
   ```

5. **Build and Install**
   ```bash
   pip install .
   ```

### Why This Works
- Builds specifically for the user's exact system configuration
- Ensures all CUDA dependencies are properly linked
- Creates a wheel that matches the exact CUDA version and GPU architecture

### Verification Method
- Check Task Manager for Dedicated GPU memory usage during model loading
- Look for version string with `+cu122` or similar in `pip freeze`

## Critical Analysis
This approach addresses the root cause: **pre-built wheels don't match the user's specific system configuration**. The DLL dependency errors occur because the pre-built wheels were compiled against different CUDA versions or with different dependency paths than what exists on the user's system.

