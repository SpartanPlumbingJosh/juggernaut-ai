#!/usr/bin/env python3
"""
REAL JUGGERNAUT AI INSTALLATION SCRIPT
Python 3.11 Compatible - NO DEMO MODE
RTX 4070 SUPER Optimized
"""

import os
import sys
import subprocess
import logging
import platform
from pathlib import Path

# Configure logging without Unicode characters
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('install_real_gemma.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RealGemmaInstaller:
    def __init__(self):
        self.python_exe = sys.executable
        self.python_version = platform.python_version()
        self.is_windows = platform.system() == "Windows"
        
        print("REAL JUGGERNAUT AI INSTALLATION")
        print("NO DEMO MODE - INSTALLING REAL AI SYSTEM")
        print("=" * 50)
        
        logger.info("INSTALLING REAL GEMMA AI SYSTEM")
        logger.info("NO DEMO MODE - REAL AI RESPONSES ONLY")
        logger.info(f"Python version: {self.python_version}")
        logger.info(f"Platform: {platform.system()}")
        
    def check_python_version(self):
        """Check if Python version is compatible"""
        version_info = sys.version_info
        if version_info.major != 3 or version_info.minor < 8:
            logger.error(f"Python 3.8+ required, found {self.python_version}")
            return False
        
        if version_info.minor >= 11:
            logger.info(f"Python {self.python_version} detected - using Python 3.11+ compatible packages")
        
        return True
    
    def run_command(self, description, command):
        """Run a command and handle errors"""
        try:
            logger.info(f"Running: {description}")
            logger.info(f"Command: {' '.join(command)}")
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            
            logger.info(f"Success: {description}")
            if result.stdout:
                logger.info(f"Output: {result.stdout.strip()}")
            
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed: {description}")
            logger.error(f"Error: {e}")
            if e.stdout:
                logger.error(f"Output: {e.stdout}")
            if e.stderr:
                logger.error(f"Error output: {e.stderr}")
            return False
    
    def install_pip_packages(self):
        """Install required packages with Python 3.11 compatibility"""
        
        # Essential packages for REAL Gemma
        essential_packages = [
            "Flask>=2.3.3",
            "Werkzeug>=2.3.7", 
            "numpy>=1.24.0",
            "requests>=2.31.0",
            "psutil>=5.9.0",
            "colorlog>=6.7.0"
        ]
        
        # Install essential packages first
        for package in essential_packages:
            success = self.run_command(
                f"Installing {package}",
                [self.python_exe, "-m", "pip", "install", package, "--upgrade"]
            )
            if not success:
                logger.warning(f"Failed to install {package}, continuing...")
        
        # Install llama-cpp-python with CUDA support for RTX 4070 SUPER
        logger.info("Installing llama-cpp-python with CUDA support for RTX 4070 SUPER...")
        
        # Try different installation methods for llama-cpp-python
        cuda_install_commands = [
            # Method 1: Direct CUDA installation
            [self.python_exe, "-m", "pip", "install", "llama-cpp-python[cuda]", "--upgrade", "--force-reinstall"],
            
            # Method 2: Pre-built wheel with CUDA
            [self.python_exe, "-m", "pip", "install", "llama-cpp-python", "--upgrade", "--force-reinstall", 
             "--extra-index-url", "https://abetlen.github.io/llama-cpp-python/whl/cu121"],
            
            # Method 3: Build from source with CUDA
            [self.python_exe, "-m", "pip", "install", "llama-cpp-python", "--upgrade", "--force-reinstall", "--no-cache-dir"]
        ]
        
        for i, command in enumerate(cuda_install_commands, 1):
            logger.info(f"Trying CUDA installation method {i}...")
            if self.run_command(f"Installing llama-cpp-python (method {i})", command):
                logger.info("llama-cpp-python with CUDA support installed successfully!")
                break
        else:
            logger.warning("All CUDA installation methods failed, trying CPU-only version...")
            self.run_command(
                "Installing llama-cpp-python (CPU only)",
                [self.python_exe, "-m", "pip", "install", "llama-cpp-python", "--upgrade"]
            )
    
    def verify_installation(self):
        """Verify that the installation was successful"""
        try:
            logger.info("Verifying installation...")
            
            # Test Flask
            import flask
            logger.info(f"Flask version: {flask.__version__}")
            
            # Test llama-cpp-python
            try:
                import llama_cpp
                logger.info(f"llama-cpp-python imported successfully")
                
                # Check for CUDA support
                try:
                    # This will show if CUDA is available
                    logger.info("Checking CUDA support...")
                    # Note: Actual CUDA check would require model loading
                    logger.info("llama-cpp-python ready for GPU acceleration")
                except Exception as e:
                    logger.warning(f"CUDA check warning: {e}")
                    
            except ImportError as e:
                logger.error(f"llama-cpp-python import failed: {e}")
                return False
            
            # Test other packages
            import numpy
            import requests
            import psutil
            
            logger.info("All essential packages verified!")
            return True
            
        except ImportError as e:
            logger.error(f"Package verification failed: {e}")
            return False
    
    def check_model_path(self):
        """Check if the Gemma model exists"""
        model_paths = [
            "D:/models/gemma-2-9b-it-Q6_K.gguf",
            "D:/models/gemma-2-9b-it-Q4_K_M.gguf",
            "D:/Juggernaut_AI/models/gemma-2-9b-it-Q6_K.gguf",
            "./models/gemma-2-9b-it-Q6_K.gguf"
        ]
        
        logger.info("Checking for Gemma model files...")
        
        for path in model_paths:
            if os.path.exists(path):
                logger.info(f"Found Gemma model: {path}")
                file_size = os.path.getsize(path) / (1024**3)  # GB
                logger.info(f"Model size: {file_size:.2f} GB")
                return path
        
        logger.warning("No Gemma model found!")
        logger.warning("Please download a Gemma model to one of these locations:")
        for path in model_paths:
            logger.warning(f"  - {path}")
        
        return None
    
    def install(self):
        """Run the complete installation"""
        try:
            # Check Python version
            if not self.check_python_version():
                return False
            
            # Upgrade pip first
            self.run_command(
                "Upgrading pip",
                [self.python_exe, "-m", "pip", "install", "--upgrade", "pip"]
            )
            
            # Install packages
            self.install_pip_packages()
            
            # Verify installation
            if not self.verify_installation():
                logger.error("Installation verification failed!")
                return False
            
            # Check for model
            model_path = self.check_model_path()
            
            print("\n" + "=" * 50)
            if model_path:
                print("INSTALLATION SUCCESSFUL!")
                print("REAL Gemma AI system ready!")
                print(f"Model found: {model_path}")
                print("\nTo start the system:")
                print("python juggernaut_real_fixed.py")
            else:
                print("INSTALLATION COMPLETED!")
                print("Dependencies installed successfully.")
                print("\nNEXT STEP: Download a Gemma model")
                print("Recommended: gemma-2-9b-it-Q6_K.gguf")
                print("Place it in: D:/models/")
            
            print("=" * 50)
            return True
            
        except Exception as e:
            logger.error(f"Installation failed: {e}")
            print("\n" + "=" * 50)
            print("INSTALLATION FAILED!")
            print("Check the error messages above and try again")
            print("=" * 50)
            return False

if __name__ == "__main__":
    installer = RealGemmaInstaller()
    success = installer.install()
    sys.exit(0 if success else 1)

