#!/usr/bin/env python3
"""
JUGGERNAUT AI - Ultimate Real System
RTX 4070 SUPER Optimized with Proper CUDA Integration
No Demo Mode - Real AI Responses Only
"""

import os
import sys
import json
import time
import logging
import traceback
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory

# Configure logging without emoji characters (Windows PowerShell compatible)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('juggernaut.log')
    ]
)
logger = logging.getLogger(__name__)

class RealGemmaEngine:
    """Real Gemma Engine with proper CUDA support for RTX 4070 SUPER"""
    
    def __init__(self, model_path=None, gpu_layers=35):
        self.model_path = model_path or self.find_model_path()
        self.gpu_layers = gpu_layers
        self.model = None
        self.loaded = False
        
        logger.info("Initializing REAL Gemma Engine...")
        logger.info(f"NO DEMO MODE - Loading actual model file")
        logger.info(f"Model: {self.model_path}")
        
    def find_model_path(self):
        """Find the user's Gemma model file"""
        possible_paths = [
            "D:/models/gemma-2-9b-it-Q6_K.gguf",
            "D:/models/gemma-2-9b-it-Q4_K_M.gguf",
            "D:/Juggernaut_AI/models/ai_models/text/gemma_2_9b_gguf/gemma-2-9b-it-Q6_K.gguf",
            "D:/Juggernaut_AI/models/ai_models/text/gemma_2_9b_gguf/gemma-2-9b-it-Q4_K_M.gguf"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"Found model at: {path}")
                return path
                
        logger.error("No Gemma model found! Please ensure model is in D:/models/")
        return None
    
    def load_model(self):
        """Load the Gemma model with CUDA support"""
        if not self.model_path or not os.path.exists(self.model_path):
            logger.error("Model path not found or invalid")
            return False
            
        try:
            logger.info(f"Loading REAL Gemma model from: {self.model_path}")
            
            # Import llama-cpp-python
            from llama_cpp import Llama
            
            # Load model with RTX 4070 SUPER optimized settings
            self.model = Llama(
                model_path=self.model_path,
                n_gpu_layers=self.gpu_layers,  # Use 35 layers for RTX 4070 SUPER
                n_ctx=4096,  # Context length
                n_batch=512,  # Batch size
                verbose=True,  # Show CUDA initialization
                use_mmap=True,
                use_mlock=False
            )
            
            self.loaded = True
            logger.info("REAL Gemma model loaded successfully!")
            logger.info(f"GPU layers: {self.gpu_layers}")
            logger.info("CUDA acceleration active")
            
            return True
            
        except ImportError as e:
            logger.error(f"llama-cpp-python not installed or not working: {e}")
            logger.error("Please run the CUDA installer first")
            return False
            
        except Exception as e:
            logger.error(f"Failed to load Gemma model: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    def generate_response(self, prompt, max_tokens=2048, temperature=0.7):
        """Generate real AI response using Gemma model"""
        if not self.loaded or not self.model:
            logger.error("Model not loaded - cannot generate response")
            return "ERROR: Gemma model not loaded. Please check installation."
            
        try:
            logger.info(f"Generating response for prompt: {prompt[:50]}...")
            
            # Create the full prompt with proper formatting
            full_prompt = f"<start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n"
            
            # Generate response using the model
            response = self.model(
                full_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,
                repeat_penalty=1.1,
                stop=["<end_of_turn>", "<start_of_turn>"],
                echo=False
            )
            
            # Extract the generated text
            generated_text = response['choices'][0]['text'].strip()
            
            logger.info("Response generated successfully")
            return generated_text
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"Error generating response: {str(e)}"

class JuggernautDataManager:
    """Manage Juggernaut data and conversations"""
    
    def __init__(self, data_dir="D:/JUGGERNAUT_DATA"):
        self.data_dir = Path(data_dir)
        self.conversations_file = self.data_dir / "conversations.json"
        self.learning_file = self.data_dir / "learning_data.json"
        
        # Create data directory if it doesn't exist
        self.data_dir.mkdir(exist_ok=True)
        
        logger.info(f"Data directory: {self.data_dir}")
        
    def load_conversations(self):
        """Load conversation history"""
        try:
            if self.conversations_file.exists():
                with open(self.conversations_file, 'r') as f:
                    return json.load(f)
            return {"conversations": []}
        except Exception as e:
            logger.error(f"Error loading conversations: {e}")
            return {"conversations": []}
    
    def save_conversation(self, user_message, ai_response):
        """Save conversation to history"""
        try:
            conversations = self.load_conversations()
            
            conversation_entry = {
                "type": "conversation",
                "timestamp": datetime.now().isoformat(),
                "user_message": user_message,
                "ai_response": ai_response
            }
            
            conversations["conversations"].append(conversation_entry)
            
            with open(self.conversations_file, 'w') as f:
                json.dump(conversations, f, indent=2)
                
            logger.info("Conversation saved")
            
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")

class JuggernautAI:
    """Main Juggernaut AI System"""
    
    def __init__(self):
        logger.info("INITIALIZING REAL JUGGERNAUT AI - NO DEMO MODE")
        
        # Initialize components
        self.gemma_engine = RealGemmaEngine()
        self.data_manager = JuggernautDataManager()
        
        # System info
        self.system_info = {
            "gpu": "RTX 4070 SUPER",
            "vram": "12GB",
            "model": "Gemma 2-9B-IT Q6_K (newest version)",
            "status": "Real AI System",
            "demo_mode": False
        }
        
        logger.info(f"Model: {self.gemma_engine.model_path}")
        logger.info(f"REAL Model path: {self.gemma_engine.model_path}")
        logger.info(f"Data directory: {self.data_manager.data_dir}")
        logger.info(f"GPU layers: {self.gemma_engine.gpu_layers}")
        
        # Load the model
        logger.info("Initializing REAL Gemma Engine...")
        model_loaded = self.gemma_engine.load_model()
        
        if model_loaded:
            logger.info("REAL Gemma model loaded successfully!")
            self.system_info["model_status"] = "Loaded"
        else:
            logger.error("FAILED to load REAL Gemma model!")
            logger.error("System will not provide AI responses until model is loaded")
            self.system_info["model_status"] = "Failed"
    
    def process_message(self, message):
        """Process user message and generate AI response"""
        logger.info(f"Processing message: {message[:50]}...")
        
        if not self.gemma_engine.loaded:
            return "ERROR: Gemma model not loaded. Please check the installation and model path."
        
        # Generate response using real Gemma model
        response = self.gemma_engine.generate_response(message)
        
        # Save conversation
        self.data_manager.save_conversation(message, response)
        
        return response
    
    def get_system_status(self):
        """Get current system status"""
        return {
            **self.system_info,
            "model_loaded": self.gemma_engine.loaded,
            "timestamp": datetime.now().isoformat()
        }

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'juggernaut_ai_secret_key'

# Initialize Juggernaut AI system
juggernaut = JuggernautAI()

@app.route('/')
def index():
    """Main interface"""
    return render_template('integrated_index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Process message with real AI
        response = juggernaut.process_message(message)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'model': 'Gemma 2-9B-IT (Real)',
            'demo_mode': False
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    """Get system status"""
    return jsonify(juggernaut.get_system_status())

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

def main():
    """Main function to start the system"""
    print("=" * 40)
    print("   JUGGERNAUT AI - STARTING SYSTEM")
    print("=" * 40)
    print()
    print("RTX 4070 SUPER AI System")
    print("Real Gemma 2-9B-IT Integration") 
    print("Professional Monster UI")
    print()
    print("Starting Juggernaut AI System...")
    print()
    print("Web interface will be available at:")
    print("http://localhost:5000")
    print()
    print("Press Ctrl+C to stop the system")
    print("=" * 40)
    
    logger.info("Starting REAL Juggernaut AI System...")
    logger.info("NO DEMO MODE - REAL AI RESPONSES ONLY")
    logger.info(f"Model: {juggernaut.system_info['model']}")
    
    if not juggernaut.gemma_engine.loaded:
        logger.warning("REAL Gemma model NOT loaded - check configuration")
    
    logger.info("Web interface starting on http://localhost:5000")
    
    # Start Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )

if __name__ == '__main__':
    main()

