# Build llama-cpp-python from Source with CUDA Support for RTX 4070 SUPER
# Based on comprehensive research and root cause analysis
# Author: Manus AI
# Date: June 27, 2025

Write-Host "========================================" -ForegroundColor Green
Write-Host "   LLAMA-CPP-PYTHON CUDA BUILD SCRIPT" -ForegroundColor Green
Write-Host "   RTX 4070 SUPER Optimized Build" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "WARNING: Not running as Administrator. Some operations may fail." -ForegroundColor Yellow
    Write-Host "Consider running PowerShell as Administrator for best results." -ForegroundColor Yellow
    Write-Host ""
}

# Step 1: Verify Prerequisites
Write-Host "Step 1: Verifying Prerequisites..." -ForegroundColor Cyan

# Check CUDA installation
$cudaPath = $env:CUDA_PATH
if (-not $cudaPath -or -not (Test-Path $cudaPath)) {
    Write-Host "ERROR: CUDA_PATH not found or invalid: $cudaPath" -ForegroundColor Red
    Write-Host "Please ensure CUDA Toolkit 12.4 is properly installed." -ForegroundColor Red
    exit 1
}
Write-Host "✓ CUDA found at: $cudaPath" -ForegroundColor Green

# Check Visual Studio Community
$vsPath = "C:\Program Files\Microsoft Visual Studio\2022\Community"
if (-not (Test-Path $vsPath)) {
    Write-Host "ERROR: Visual Studio 2022 Community not found at: $vsPath" -ForegroundColor Red
    Write-Host "Please install Visual Studio 2022 Community with C++ workload." -ForegroundColor Red
    exit 1
}
Write-Host "✓ Visual Studio 2022 Community found" -ForegroundColor Green

# Check CUDA integration in Visual Studio
$cudaPropsPath = "$vsPath\MSBuild\Microsoft\VC\v170\BuildCustomizations\CUDA 12.4.props"
if (-not (Test-Path $cudaPropsPath)) {
    Write-Host "ERROR: CUDA integration not found in Visual Studio" -ForegroundColor Red
    Write-Host "Expected: $cudaPropsPath" -ForegroundColor Red
    exit 1
}
Write-Host "✓ CUDA integration found in Visual Studio" -ForegroundColor Green

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python not found in PATH" -ForegroundColor Red
    exit 1
}

# Step 2: Clean Previous Installations
Write-Host ""
Write-Host "Step 2: Cleaning Previous Installations..." -ForegroundColor Cyan

Write-Host "Uninstalling existing llama-cpp-python..." -ForegroundColor Yellow
pip uninstall llama-cpp-python -y 2>$null

# Step 3: Set Environment Variables
Write-Host ""
Write-Host "Step 3: Configuring Environment Variables..." -ForegroundColor Cyan

# CUDA Configuration for RTX 4070 SUPER (Compute Capability 8.9)
$env:CUDA_HOME = $cudaPath
$env:CUDA_PATH = $cudaPath
$env:PATH = "$cudaPath\bin;$env:PATH"
$env:PATH = "$cudaPath\libnvvp;$env:PATH"

# Build Configuration
$env:FORCE_CMAKE = "1"
$env:CMAKE_ARGS = "-DGGML_CUDA=on -DCMAKE_CUDA_ARCHITECTURES=89"
$env:GGML_CUDA = "1"

# Visual Studio Configuration
$env:CMAKE_GENERATOR = "Visual Studio 17 2022"
$env:CMAKE_GENERATOR_INSTANCE = $vsPath
$env:CMAKE_GENERATOR_PLATFORM = "x64"

# NVCC Configuration (Critical for dependency resolution)
$env:CUDACXX = "$cudaPath\bin\nvcc.exe"

Write-Host "✓ Environment variables configured:" -ForegroundColor Green
Write-Host "  CUDA_HOME: $env:CUDA_HOME" -ForegroundColor Gray
Write-Host "  CMAKE_ARGS: $env:CMAKE_ARGS" -ForegroundColor Gray
Write-Host "  CUDACXX: $env:CUDACXX" -ForegroundColor Gray

# Step 4: Create Build Directory
Write-Host ""
Write-Host "Step 4: Preparing Build Directory..." -ForegroundColor Cyan

$buildDir = "D:\llama-cpp-build"
if (Test-Path $buildDir) {
    Write-Host "Removing existing build directory..." -ForegroundColor Yellow
    Remove-Item $buildDir -Recurse -Force
}

New-Item -ItemType Directory -Path $buildDir -Force | Out-Null
Set-Location $buildDir

# Step 5: Clone Repository
Write-Host ""
Write-Host "Step 5: Cloning llama-cpp-python Repository..." -ForegroundColor Cyan

Write-Host "Cloning with submodules (this may take a few minutes)..." -ForegroundColor Yellow
git clone --recurse-submodules https://github.com/abetlen/llama-cpp-python.git
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to clone repository" -ForegroundColor Red
    exit 1
}

Set-Location "llama-cpp-python"
Write-Host "✓ Repository cloned successfully" -ForegroundColor Green

# Step 6: Install Build Dependencies
Write-Host ""
Write-Host "Step 6: Installing Build Dependencies..." -ForegroundColor Cyan

pip install cmake ninja
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install build dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Build dependencies installed" -ForegroundColor Green

# Step 7: Build and Install
Write-Host ""
Write-Host "Step 7: Building llama-cpp-python from Source..." -ForegroundColor Cyan
Write-Host "This will take several minutes. Please be patient..." -ForegroundColor Yellow
Write-Host ""

$buildStartTime = Get-Date

# Execute the build
pip install . --verbose
$buildResult = $LASTEXITCODE

$buildEndTime = Get-Date
$buildDuration = $buildEndTime - $buildStartTime

if ($buildResult -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "   BUILD COMPLETED SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Build time: $($buildDuration.ToString('mm\:ss'))" -ForegroundColor Green
    Write-Host ""
    
    # Step 8: Verification
    Write-Host "Step 8: Verifying Installation..." -ForegroundColor Cyan
    
    Write-Host "Testing import..." -ForegroundColor Yellow
    $testResult = python -c "
import llama_cpp
print('✓ llama-cpp-python imported successfully')
print('✓ CUDA support available:', llama_cpp.llama_supports_gpu_offload())
" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host $testResult -ForegroundColor Green
        Write-Host ""
        Write-Host "SUCCESS: llama-cpp-python with CUDA support is ready!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Cyan
        Write-Host "1. Navigate to your Juggernaut AI directory: cd D:\JuggernautAI" -ForegroundColor White
        Write-Host "2. Start your system: python juggernaut_real_ultimate.py" -ForegroundColor White
        Write-Host "3. Monitor GPU usage in Task Manager to verify acceleration" -ForegroundColor White
    } else {
        Write-Host "WARNING: Build succeeded but import test failed:" -ForegroundColor Yellow
        Write-Host $testResult -ForegroundColor Red
        Write-Host "The installation may still work. Try running your Juggernaut system." -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "   BUILD FAILED!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "Build time: $($buildDuration.ToString('mm\:ss'))" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common solutions:" -ForegroundColor Yellow
    Write-Host "1. Ensure Visual Studio 2022 Community is installed with C++ workload" -ForegroundColor White
    Write-Host "2. Verify CUDA Toolkit 12.4 is properly installed" -ForegroundColor White
    Write-Host "3. Run PowerShell as Administrator" -ForegroundColor White
    Write-Host "4. Check that no antivirus is blocking the build process" -ForegroundColor White
}

Write-Host ""
Write-Host "Build log location: $buildDir\llama-cpp-python" -ForegroundColor Gray
Write-Host "Script completed at: $(Get-Date)" -ForegroundColor Gray

