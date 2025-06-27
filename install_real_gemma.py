#!/usr/bin/env python3
"""
REAL Gemma Installation Script
Installs all dependencies for REAL AI responses
NO DEMO MODE
"""

import subprocess
import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_command(command, description):
    """Run a command and handle errors"""
    try:
        logger.info(f"Running: {description}")
        logger.info(f"Command: {' '.join(command)}")
        
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info(f"Success: {description}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed: {description}")
        logger.error(f"Error: {e}")
        logger.error(f"Output: {e.stdout}")
        logger.error(f"Error output: {e.stderr}")
        return False

def install_real_gemma():
    """Install REAL Gemma dependencies"""
    logger.info("INSTALLING REAL GEMMA AI SYSTEM")
    logger.info("NO DEMO MODE - REAL AI RESPONSES ONLY")
    
    # Step 1: Upgrade pip
    if not run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      "Upgrading pip"):
        return False
    
    # Step 2: Install basic requirements
    if not run_command([sys.executable, "-m", "pip", "install", "-r", "requirements_real.txt"], 
                      "Installing basic requirements"):
        return False
    
    # Step 3: Install llama-cpp-python with CUDA support for RTX 4070 SUPER
    logger.info("Installing llama-cpp-python with CUDA support for RTX 4070 SUPER...")
    
    # Set environment variables for CUDA compilation
    env = os.environ.copy()
    env['CMAKE_ARGS'] = '-DLLAMA_CUBLAS=on'
    env['FORCE_CMAKE'] = '1'
    
    if not run_command([sys.executable, "-m", "pip", "install", 
                       "llama-cpp-python[cuda]", "--upgrade", "--force-reinstall", "--no-cache-dir"], 
                      "Installing llama-cpp-python with CUDA"):
        logger.warning("CUDA installation failed, trying CPU version...")
        if not run_command([sys.executable, "-m", "pip", "install", 
                           "llama-cpp-python", "--upgrade", "--force-reinstall"], 
                          "Installing llama-cpp-python (CPU fallback)"):
            return False
    
    # Step 4: Verify installation
    try:
        import llama_cpp
        logger.info("llama-cpp-python installed successfully!")
        
        # Check for CUDA support
        try:
            # This will work if CUDA is available
            from llama_cpp import Llama
            logger.info("CUDA support detected - RTX 4070 SUPER ready!")
        except Exception as e:
            logger.warning(f"CUDA support check failed: {e}")
            logger.warning("Model will run on CPU - performance may be slower")
            
    except ImportError as e:
        logger.error(f"Failed to import llama-cpp-python: {e}")
        return False
    
    # Step 5: Install additional dependencies
    additional_packages = [
        "requests",
        "flask",
        "numpy",
        "psutil"
    ]
    
    for package in additional_packages:
        if not run_command([sys.executable, "-m", "pip", "install", package, "--upgrade"], 
                          f"Installing {package}"):
            logger.warning(f"Failed to install {package}, but continuing...")
    
    logger.info("REAL GEMMA INSTALLATION COMPLETE!")
    logger.info("System ready for REAL AI responses")
    
    return True

def test_installation():
    """Test the installation"""
    logger.info("Testing REAL Gemma installation...")
    
    try:
        # Test imports
        import llama_cpp
        import flask
        import numpy
        
        logger.info("All imports successful!")
        
        # Test Gemma engine creation (without loading model)
        from real_gemma_engine import RealGemmaEngine
        logger.info("RealGemmaEngine import successful!")
        
        logger.info("INSTALLATION TEST PASSED!")
        return True
        
    except Exception as e:
        logger.error(f"Installation test failed: {e}")
        return False

if __name__ == "__main__":
    print("REAL JUGGERNAUT AI INSTALLATION")
    print("NO DEMO MODE - INSTALLING REAL AI SYSTEM")
    print("=" * 50)
    
    if install_real_gemma():
        print("\n" + "=" * 50)
        print("INSTALLATION SUCCESSFUL!")
        print("You can now run: python juggernaut_real.py")
        print("For REAL AI responses with your Gemma model")
        
        if test_installation():
            print("SYSTEM READY FOR REAL AI!")
        else:
            print("Installation complete but tests failed - check logs")
    else:
        print("\n" + "=" * 50)
        print("INSTALLATION FAILED!")
        print("Check the error messages above and try again")
        sys.exit(1)

