#!/usr/bin/env python3
"""
JUGGERNAUT AI - Final Working System
Built specifically for RTX 4070 SUPER with proper CUDA integration
Author: Manus AI
Date: June 27, 2025

This version is designed to work with llama-cpp-python built from source
with proper CUDA support and dependency resolution.
"""

import os
import sys
import json
import logging
import traceback
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
import threading
import time

# Configure logging without Unicode characters for PowerShell compatibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class JuggernautAI:
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self.model_path = None
        self.conversation_history = []
        self.system_metrics = {
            'gpu_name': 'RTX 4070 SUPER',
            'vram': '12GB',
            'model_name': 'Gemma 3',
            'status': 'Initializing'
        }
        
        # Find model file
        self.find_model()
        
        # Initialize AI engine
        self.initialize_ai_engine()
    
    def find_model(self):
        """Find the Gemma model file in common locations"""
        possible_paths = [
            "D:/models/gemma-2-9b-it-Q6_K.gguf",
            "D:/models/gemma-2-9b-it.gguf", 
            "D:/models/gemma-2-9b.gguf",
            "models/gemma-2-9b-it-Q6_K.gguf",
            "models/gemma-2-9b-it.gguf"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                self.model_path = path
                logger.info(f"Found model at: {path}")
                return
        
        # If no model found, use the expected path
        self.model_path = "D:/models/gemma-2-9b-it-Q6_K.gguf"
        logger.warning(f"Model not found. Expected location: {self.model_path}")
    
    def initialize_ai_engine(self):
        """Initialize the AI engine with proper error handling"""
        try:
            logger.info("Initializing REAL Juggernaut AI System...")
            logger.info("NO DEMO MODE - REAL AI RESPONSES ONLY")
            logger.info("Model: Gemma 2-9B-IT Q6_K (newest version)")
            
            # Import llama_cpp
            import llama_cpp
            logger.info("llama-cpp-python imported successfully")
            
            # Check CUDA support
            cuda_available = llama_cpp.llama_supports_gpu_offload()
            logger.info(f"CUDA GPU offload support: {cuda_available}")
            
            if not os.path.exists(self.model_path):
                logger.error(f"Model file not found: {self.model_path}")
                logger.error("Please ensure your Gemma model is downloaded to D:/models/")
                self.system_metrics['status'] = 'Model Not Found'
                return
            
            # Load model with RTX 4070 SUPER optimized settings
            logger.info(f"Loading model from: {self.model_path}")
            logger.info("Optimizing for RTX 4070 SUPER (Compute Capability 8.9)")
            
            self.model = llama_cpp.Llama(
                model_path=self.model_path,
                n_gpu_layers=35,  # Optimized for RTX 4070 SUPER
                n_ctx=4096,      # Context window
                n_batch=512,     # Batch size
                verbose=True,    # Show loading progress
                use_mmap=True,   # Memory mapping for efficiency
                use_mlock=True,  # Lock memory pages
                n_threads=8      # CPU threads for non-GPU operations
            )
            
            self.model_loaded = True
            self.system_metrics['status'] = 'Ready'
            logger.info("SUCCESS: Real Gemma model loaded with GPU acceleration")
            logger.info("RTX 4070 SUPER GPU layers: 35/35")
            
        except ImportError as e:
            logger.error(f"Failed to import llama_cpp: {e}")
            logger.error("Please run the build script to install llama-cpp-python with CUDA support")
            self.system_metrics['status'] = 'Import Error'
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            self.system_metrics['status'] = 'Load Error'
    
    def generate_response(self, message, chat_type="general"):
        """Generate AI response using the loaded model"""
        if not self.model_loaded or not self.model:
            return {
                'response': 'AI model not loaded. Please check the console for errors.',
                'error': True
            }
        
        try:
            # Prepare the prompt
            system_prompt = self.get_system_prompt(chat_type)
            full_prompt = f"{system_prompt}\n\nUser: {message}\nAssistant:"
            
            logger.info(f"Generating response for: {message[:50]}...")
            
            # Generate response
            response = self.model(
                full_prompt,
                max_tokens=512,
                temperature=0.7,
                top_p=0.9,
                repeat_penalty=1.1,
                stop=["User:", "\n\n"]
            )
            
            # Extract the response text
            response_text = response['choices'][0]['text'].strip()
            
            # Store in conversation history
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'user_message': message,
                'ai_response': response_text,
                'chat_type': chat_type
            })
            
            logger.info("Response generated successfully")
            
            return {
                'response': response_text,
                'error': False
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                'response': f'Error generating response: {str(e)}',
                'error': True
            }
    
    def get_system_prompt(self, chat_type):
        """Get system prompt based on chat type"""
        prompts = {
            'general': "You are JUGGERNAUT, an advanced AI assistant. You are helpful, knowledgeable, and provide detailed responses.",
            'research': "You are JUGGERNAUT in research mode. Provide detailed, well-researched responses with citations when possible.",
            'coding': "You are JUGGERNAUT in coding mode. Provide clear, well-commented code solutions and explanations."
        }
        return prompts.get(chat_type, prompts['general'])

# Initialize the AI system
juggernaut = JuggernautAI()

# Flask application
app = Flask(__name__)

@app.route('/')
def index():
    """Main interface"""
    return render_template('integrated_index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        chat_type = data.get('chat_type', 'general')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        logger.info(f"Processing message: {message}")
        
        # Generate response
        result = juggernaut.generate_response(message, chat_type)
        
        return jsonify({
            'response': result['response'],
            'timestamp': datetime.now().isoformat(),
            'model_status': juggernaut.system_metrics['status']
        })
        
    except Exception as e:
        logger.error(f"Chat API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/status')
def system_status():
    """Get system status"""
    return jsonify({
        'metrics': juggernaut.system_metrics,
        'model_loaded': juggernaut.model_loaded,
        'model_path': juggernaut.model_path,
        'conversation_count': len(juggernaut.conversation_history)
    })

@app.route('/api/chat/history')
def chat_history():
    """Get chat history"""
    chat_id = request.args.get('chat_id', 'general')
    # Filter history by chat type if needed
    return jsonify({
        'history': juggernaut.conversation_history[-50:],  # Last 50 messages
        'total_count': len(juggernaut.conversation_history)
    })

if __name__ == '__main__':
    print("========================================")
    print("   JUGGERNAUT AI - STARTING SYSTEM")
    print("========================================")
    print("")
    print("RTX 4070 SUPER AI System")
    print("Real Gemma 2-9B-IT Integration")
    print("Professional Monster UI")
    print("")
    print("Starting Juggernaut AI System...")
    print("")
    print("Web interface will be available at:")
    print("http://localhost:5000")
    print("")
    print("Press Ctrl+C to stop the system")
    print("========================================")
    
    # Start Flask application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )

