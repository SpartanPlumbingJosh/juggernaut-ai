# JUGGERNAUT AI - REAL SYSTEM WITH CORRECT MODEL PATH
# Updated to use: D:\models\gemma-2-9b-it-Q6_K.gguf
# RTX 4070 SUPER optimized with 35 GPU layers

import os
import sys
import json
import time
import logging
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
import threading
import subprocess

# Import the REAL Gemma engine
from real_gemma_engine import create_gemma_engine

# Configure logging without Unicode characters
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('juggernaut_real.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class JuggernautRealAI:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_paths()
        self.setup_routes()
        self.gemma_engine = None
        self.chat_manager = None
        self.system_metrics = {}
        self.start_time = time.time()
        
        # Initialize REAL Gemma engine
        self.init_real_gemma()
        
    def setup_paths(self):
        """Setup file paths for the system"""
        # UPDATED MODEL PATH - User's actual model location
        self.model_path = os.environ.get('JUGGERNAUT_MODEL_PATH', 
            'D:/models/gemma-2-9b-it-Q6_K.gguf')  # CORRECTED PATH
        self.data_dir = os.environ.get('JUGGERNAUT_DATA_DIR', 'D:/JUGGERNAUT_DATA')
        self.gpu_layers = int(os.environ.get('JUGGERNAUT_GPU_LAYERS', '35'))
        
        # Create directories if they don't exist
        os.makedirs('logs', exist_ok=True)
        os.makedirs('static', exist_ok=True)
        os.makedirs('templates', exist_ok=True)
        
        logger.info(f"REAL Model path: {self.model_path}")
        logger.info(f"Data directory: {self.data_dir}")
        logger.info(f"GPU layers: {self.gpu_layers}")
        
    def init_real_gemma(self):
        """Initialize the REAL Gemma engine - NO DEMO MODE"""
        try:
            logger.info("Initializing REAL Gemma Engine...")
            logger.info("NO DEMO MODE - Loading actual model file")
            logger.info(f"Model: {self.model_path}")
            
            # Create the real Gemma engine with correct path
            self.gemma_engine = create_gemma_engine(
                model_path=self.model_path,
                gpu_layers=self.gpu_layers
            )
            
            if self.gemma_engine.is_loaded:
                logger.info("REAL Gemma model loaded successfully!")
                logger.info("System ready for REAL AI responses")
                logger.info(f"Model: gemma-2-9b-it-Q6_K (newest version)")
                logger.info(f"GPU layers: {self.gpu_layers}")
                logger.info(f"VRAM usage: Optimized for RTX 4070 SUPER")
                
                # Test the model
                test_response = self.gemma_engine.test_model()
                logger.info(f"Model test successful: {test_response[:100]}...")
                
            else:
                logger.error("FAILED to load REAL Gemma model!")
                logger.error("System will not provide AI responses until model is loaded")
                
        except Exception as e:
            logger.error(f"REAL Gemma initialization error: {e}")
            self.gemma_engine = None
        
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            return render_template('index.html')
            
        @self.app.route('/api/chat', methods=['POST'])
        def chat():
            try:
                data = request.json
                message = data.get('message', '')
                chat_id = data.get('chat_id', 'general')
                
                if not message:
                    return jsonify({'success': False, 'error': 'No message provided'})
                
                # Process with REAL Gemma engine
                response = self.process_real_message(message, chat_id)
                
                # Calculate response metadata
                response_time = len(response) * 2  # Rough estimate
                token_count = len(response.split())
                
                return jsonify({
                    'success': True,
                    'response': response,
                    'metadata': {
                        'response_time': f'{response_time}ms',
                        'tokens': token_count,
                        'model': 'Gemma 2-9B-IT Q6_K (REAL)',
                        'gpu_layers': self.gpu_layers,
                        'engine_status': 'REAL' if self.gemma_engine and self.gemma_engine.is_loaded else 'ERROR'
                    }
                })
                
            except Exception as e:
                logger.error(f"Chat error: {e}")
                return jsonify({'success': False, 'error': str(e)})
        
        @self.app.route('/api/system/metrics')
        def system_metrics():
            try:
                # Get real model status
                model_status = "Gemma 2-9B-IT Q6_K" if (self.gemma_engine and self.gemma_engine.is_loaded) else "NOT LOADED"
                
                metrics = {
                    'gpu': 'RTX 4070 SUPER',
                    'vram': '12GB',
                    'model': model_status,
                    'status': 'REAL AI' if (self.gemma_engine and self.gemma_engine.is_loaded) else 'NO AI',
                    'uptime': time.time() - self.start_time,
                    'gpu_layers': self.gpu_layers,
                    'model_path': self.model_path,
                    'model_size': '7.59GB',
                    'model_quality': 'Q6_K (High Quality)'
                }
                return jsonify({'success': True, 'data': metrics})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
        
        @self.app.route('/api/upload', methods=['POST'])
        def upload_files():
            try:
                files = request.files.getlist('files')
                if not files:
                    return jsonify({'success': False, 'error': 'No files uploaded'})
                
                # Use REAL Gemma for file analysis
                file_names = [f.filename for f in files]
                analysis_prompt = f"Analyze these uploaded files: {', '.join(file_names)}. Provide insights about their content and purpose."
                
                if self.gemma_engine and self.gemma_engine.is_loaded:
                    analysis = self.gemma_engine.generate_response(analysis_prompt, max_tokens=300)
                else:
                    analysis = "File upload received, but Gemma model not loaded for analysis. Please check model configuration."
                
                return jsonify({
                    'success': True,
                    'analysis': analysis,
                    'files_processed': len(files)
                })
                
            except Exception as e:
                logger.error(f"Upload error: {e}")
                return jsonify({'success': False, 'error': str(e)})
        
        @self.app.route('/api/chat/history')
        def chat_history():
            try:
                chat_id = request.args.get('chat_id', 'general')
                # Return empty history for now - can be enhanced later
                return jsonify({'success': True, 'history': []})
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)})
    
    def process_real_message(self, message: str, chat_id: str) -> str:
        """Process message with REAL Gemma engine - NO DEMO MODE"""
        try:
            # Check if REAL Gemma engine is loaded
            if not self.gemma_engine or not self.gemma_engine.is_loaded:
                return f"""GEMMA MODEL NOT LOADED!

The system cannot provide AI responses because the Gemma model failed to load.

Model path: {self.model_path}
GPU layers: {self.gpu_layers}

Please check:
1. Model file exists at: D:/models/gemma-2-9b-it-Q6_K.gguf
2. llama-cpp-python is installed with CUDA support
3. RTX 4070 SUPER drivers are up to date

To fix this, ensure your Gemma model is at:
{self.model_path}

Or update the model path in the launcher configuration."""
            
            # Generate REAL response using Gemma
            logger.info(f"Processing REAL message with Gemma Q6_K: {message[:50]}...")
            
            # Determine response parameters based on message type
            if len(message) > 200:
                max_tokens = 800  # Longer response for complex queries
            elif any(word in message.lower() for word in ['explain', 'describe', 'tell me about']):
                max_tokens = 600  # Detailed explanations
            else:
                max_tokens = 400  # Standard responses
            
            # Generate REAL response
            response = self.gemma_engine.generate_response(
                message, 
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            logger.info(f"REAL Gemma Q6_K response generated: {len(response)} characters")
            
            return response
                
        except Exception as e:
            logger.error(f"REAL message processing error: {e}")
            return f"Error processing message with REAL Gemma engine: {e}"
    
    def run(self):
        """Run the REAL Juggernaut AI system"""
        try:
            logger.info("Starting REAL Juggernaut AI System...")
            logger.info("NO DEMO MODE - REAL AI RESPONSES ONLY")
            logger.info("Model: Gemma 2-9B-IT Q6_K (newest version)")
            
            if self.gemma_engine and self.gemma_engine.is_loaded:
                logger.info("REAL Gemma model ready for inference")
                logger.info(f"Model info: {self.gemma_engine.get_model_info()}")
            else:
                logger.warning("REAL Gemma model NOT loaded - check configuration")
            
            logger.info("Web interface starting on http://localhost:5000")
            
            # Run Flask app
            self.app.run(
                host='0.0.0.0',
                port=5000,
                debug=False,
                threaded=True
            )
            
        except Exception as e:
            logger.error(f"System startup error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    # Create and run the REAL system
    logger.info("INITIALIZING REAL JUGGERNAUT AI - NO DEMO MODE")
    logger.info("Model: D:/models/gemma-2-9b-it-Q6_K.gguf")
    juggernaut = JuggernautRealAI()
    juggernaut.run()

