# REAL GEMMA ENGINE - NO DEMO MODE
# Actual Gemma 3 model integration with llama-cpp-python
# RTX 4070 SUPER optimized with 35 GPU layers

import os
import sys
import json
import time
import logging
from pathlib import Path
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealGemmaEngine:
    def __init__(self, model_path: str, gpu_layers: int = 35, context_length: int = 4096):
        self.model_path = model_path
        self.gpu_layers = gpu_layers
        self.context_length = context_length
        self.model = None
        self.is_loaded = False
        
        # Initialize the model
        self.load_model()
    
    def load_model(self):
        """Load the actual Gemma model using llama-cpp-python"""
        try:
            logger.info(f"Loading REAL Gemma model from: {self.model_path}")
            
            # Check if model file exists
            if not os.path.exists(self.model_path):
                logger.error(f"Model file not found: {self.model_path}")
                self.is_loaded = False
                return False
            
            # Try to import llama-cpp-python
            try:
                from llama_cpp import Llama
                logger.info("llama-cpp-python found - loading model with GPU acceleration")
            except ImportError:
                logger.error("llama-cpp-python not installed! Installing now...")
                self.install_llama_cpp()
                from llama_cpp import Llama
            
            # Load the model with RTX 4070 SUPER optimization
            logger.info(f"Loading model with {self.gpu_layers} GPU layers for RTX 4070 SUPER")
            
            self.model = Llama(
                model_path=self.model_path,
                n_gpu_layers=self.gpu_layers,  # RTX 4070 SUPER optimized
                n_ctx=self.context_length,     # Context window
                n_batch=512,                   # Batch size for RTX 4070 SUPER
                verbose=False,                 # Reduce output noise
                use_mmap=True,                 # Memory mapping for efficiency
                use_mlock=True,                # Lock memory for performance
                n_threads=8,                   # CPU threads
                f16_kv=True,                   # Use FP16 for key-value cache
            )
            
            self.is_loaded = True
            logger.info("REAL Gemma model loaded successfully!")
            logger.info(f"GPU layers: {self.gpu_layers}")
            logger.info(f"Context length: {self.context_length}")
            logger.info("Model ready for inference")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to load Gemma model: {e}")
            self.is_loaded = False
            return False
    
    def install_llama_cpp(self):
        """Install llama-cpp-python with CUDA support"""
        try:
            import subprocess
            logger.info("Installing llama-cpp-python with CUDA support...")
            
            # Install with CUDA support for RTX 4070 SUPER
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "llama-cpp-python[cuda]", "--upgrade", "--force-reinstall"
            ])
            
            logger.info("llama-cpp-python installed successfully!")
            
        except Exception as e:
            logger.error(f"Failed to install llama-cpp-python: {e}")
            raise
    
    def generate_response(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> str:
        """Generate a real response using the loaded Gemma model"""
        if not self.is_loaded or not self.model:
            return "ERROR: Gemma model not loaded. Please check model path and try again."
        
        try:
            logger.info(f"Generating response for prompt: {prompt[:50]}...")
            
            # Format prompt for Gemma
            formatted_prompt = self.format_gemma_prompt(prompt)
            
            # Generate response
            start_time = time.time()
            
            response = self.model(
                formatted_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,
                top_k=40,
                repeat_penalty=1.1,
                stop=["<|im_end|>", "\n\nUser:", "\n\nHuman:"],
                echo=False
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # Extract the generated text
            generated_text = response['choices'][0]['text'].strip()
            
            logger.info(f"Response generated in {response_time:.2f} seconds")
            logger.info(f"Tokens generated: {response['usage']['completion_tokens']}")
            
            return generated_text
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"ERROR: Failed to generate response - {e}"
    
    def format_gemma_prompt(self, user_input: str) -> str:
        """Format prompt for Gemma model"""
        system_prompt = """You are Juggernaut AI, a powerful AI assistant running on RTX 4070 SUPER hardware. You are knowledgeable, helpful, and direct in your responses. You have access to advanced capabilities including file analysis, web browsing, and system monitoring."""
        
        formatted_prompt = f"""<|im_start|>system
{system_prompt}<|im_end|>
<|im_start|>user
{user_input}<|im_end|>
<|im_start|>assistant
"""
        
        return formatted_prompt
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        if not self.is_loaded:
            return {
                "status": "Not loaded",
                "model_path": self.model_path,
                "gpu_layers": self.gpu_layers,
                "context_length": self.context_length
            }
        
        return {
            "status": "Loaded and ready",
            "model_path": self.model_path,
            "gpu_layers": self.gpu_layers,
            "context_length": self.context_length,
            "model_type": "Gemma 3 (9B parameters)",
            "optimization": "RTX 4070 SUPER (12GB VRAM)"
        }
    
    def test_model(self) -> str:
        """Test the model with a simple prompt"""
        if not self.is_loaded:
            return "Model not loaded - cannot test"
        
        test_prompt = "Hello! Please introduce yourself as Juggernaut AI."
        return self.generate_response(test_prompt, max_tokens=100)

# Factory function to create the engine
def create_gemma_engine(model_path: str = None, gpu_layers: int = 35) -> RealGemmaEngine:
    """Create and return a real Gemma engine instance"""
    
    # Default model path for user's setup
    if model_path is None:
        model_path = "D:/Juggernaut_AI/models/ai_models/text/gemma_2_9b_gguf/gemma-2-9b-it-Q4_K_M.gguf"
    
    # Alternative paths to check
    alternative_paths = [
        "D:/Juggernaut_AI/models/gemma-2-9b-it-Q4_K_M.gguf",
        "D:/models/gemma-2-9b-it-Q4_K_M.gguf",
        "./models/gemma-2-9b-it-Q4_K_M.gguf",
        os.path.join(os.getcwd(), "models", "gemma-2-9b-it-Q4_K_M.gguf")
    ]
    
    # Check if primary path exists
    if not os.path.exists(model_path):
        logger.warning(f"Primary model path not found: {model_path}")
        logger.info("Checking alternative paths...")
        
        # Try alternative paths
        for alt_path in alternative_paths:
            if os.path.exists(alt_path):
                logger.info(f"Found model at alternative path: {alt_path}")
                model_path = alt_path
                break
        else:
            logger.error("No Gemma model found in any expected location!")
            logger.error("Please ensure your model is at one of these paths:")
            for path in [model_path] + alternative_paths:
                logger.error(f"  - {path}")
    
    return RealGemmaEngine(model_path, gpu_layers)

if __name__ == "__main__":
    # Test the engine
    print("Testing REAL Gemma Engine...")
    
    engine = create_gemma_engine()
    
    if engine.is_loaded:
        print("Model loaded successfully!")
        print("Model info:", engine.get_model_info())
        
        # Test response
        test_response = engine.test_model()
        print(f"Test response: {test_response}")
    else:
        print("Failed to load model!")

