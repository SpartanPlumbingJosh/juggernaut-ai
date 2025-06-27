#!/usr/bin/env python3
"""
JUGGERNAUT AI - Complete Working System with Ollama
Reliable Gemma AI integration using Ollama instead of llama-cpp-python
Author: Manus AI
Date: June 27, 2025

This system uses Ollama for reliable AI responses without DLL dependency issues.
Features GPU acceleration with automatic CPU fallback.
"""

import os
import sys
import json
import logging
import traceback
import requests
import time
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
import threading
import subprocess

# Configure logging for PowerShell compatibility (no Unicode)
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
        self.ollama_url = "http://localhost:11434"
        self.model_name = "gemma3:12b"
        self.ollama_ready = False
        self.conversation_history = []
        self.system_metrics = {
            'gpu_name': 'RTX 4070 SUPER',
            'vram': '12GB',
            'model_name': 'Gemma 3 (12B)',
            'status': 'Initializing'
        }
        
        # Initialize Ollama connection
        self.initialize_ollama()
    
    def check_ollama_service(self):
        """Check if Ollama service is running"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def start_ollama_service(self):
        """Start Ollama service if not running"""
        try:
            # Try to start Ollama service
            subprocess.Popen(["ollama", "serve"], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL,
                           creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            
            # Wait for service to start
            for i in range(10):
                time.sleep(1)
                if self.check_ollama_service():
                    return True
            return False
        except:
            return False
    
    def check_model_availability(self):
        """Check if Gemma model is available in Ollama"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                for model in models:
                    if 'gemma3' in model.get('name', '').lower():
                        return True
            return False
        except:
            return False
    
    def initialize_ollama(self):
        """Initialize Ollama connection and verify setup"""
        try:
            logger.info("Initializing REAL Juggernaut AI System with Ollama...")
            logger.info("NO DEMO MODE - REAL AI RESPONSES ONLY")
            logger.info("Model: Gemma 3 (12B parameters) via Ollama")
            
            # Check if Ollama service is running
            if not self.check_ollama_service():
                logger.info("Ollama service not detected, attempting to start...")
                if not self.start_ollama_service():
                    logger.error("Failed to start Ollama service")
                    logger.error("Please ensure Ollama is installed and run: ollama serve")
                    self.system_metrics['status'] = 'Ollama Service Not Running'
                    return
            
            logger.info("SUCCESS: Ollama service is running")
            
            # Check if Gemma model is available
            if not self.check_model_availability():
                logger.error("Gemma model not found in Ollama")
                logger.error("Please run: ollama pull gemma3:9b")
                self.system_metrics['status'] = 'Model Not Found'
                return
            
            logger.info("SUCCESS: Gemma 3 model found in Ollama")
            
            # Test model with a simple query
            test_result = self.test_model()
            if test_result:
                self.ollama_ready = True
                self.system_metrics['status'] = 'Ready'
                logger.info("SUCCESS: Ollama integration ready for real AI responses")
                logger.info("GPU acceleration: Automatic (when available)")
                logger.info("CPU fallback: Automatic")
            else:
                logger.error("Model test failed")
                self.system_metrics['status'] = 'Model Test Failed'
                
        except Exception as e:
            logger.error(f"Failed to initialize Ollama: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            self.system_metrics['status'] = 'Initialization Error'
    
    def test_model(self):
        """Test the model with a simple query"""
        try:
            test_payload = {
                "model": self.model_name,
                "prompt": "Hello! Please respond with just 'AI system ready.'",
                "stream": False
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=test_payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('response'):
                    logger.info(f"Model test successful: {result['response'][:50]}...")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Model test failed: {e}")
            return False
    
    def generate_response(self, message, chat_type="general"):
        """Generate AI response using Ollama"""
        if not self.ollama_ready:
            return {
                'response': 'AI system not ready. Please check Ollama installation and model availability.',
                'error': True
            }
        
        try:
            # Prepare the prompt with system context
            system_prompt = self.get_system_prompt(chat_type)
            full_prompt = f"{system_prompt}\n\nUser: {message}\nAssistant:"
            
            logger.info(f"Generating response for: {message[:50]}...")
            
            # Prepare request payload
            payload = {
                "model": self.model_name,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 512
                }
            }
            
            # Send request to Ollama
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '').strip()
                
                if response_text:
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
                else:
                    return {
                        'response': 'Empty response received from AI model.',
                        'error': True
                    }
            else:
                return {
                    'response': f'AI service error: HTTP {response.status_code}',
                    'error': True
                }
                
        except requests.exceptions.Timeout:
            logger.error("Request timeout while generating response")
            return {
                'response': 'Request timeout. The AI model may be processing a complex query.',
                'error': True
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
            'general': "You are JUGGERNAUT, an advanced AI assistant. You are helpful, knowledgeable, and provide detailed responses. Always be professional and accurate.",
            'research': "You are JUGGERNAUT in research mode. Provide detailed, well-researched responses with analysis and insights. Be thorough and cite reasoning when possible.",
            'coding': "You are JUGGERNAUT in coding mode. Provide clear, well-commented code solutions with explanations. Focus on best practices and efficiency."
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
        
        if result['error']:
            return jsonify({
                'success': False,
                'error': result['response']
            }), 500
        
        return jsonify({
            'success': True,
            'response': result['response'],
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'model_status': juggernaut.system_metrics['status'],
                'response_time': 2000  # Placeholder for response time
            }
        })
        
    except Exception as e:
        logger.error(f"Chat API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/metrics')
def system_metrics():
    """Get system metrics for the UI"""
    return jsonify({
        'gpu_name': juggernaut.system_metrics['gpu_name'],
        'vram': juggernaut.system_metrics['vram'],
        'model_name': juggernaut.system_metrics['model_name'],
        'status': juggernaut.system_metrics['status'],
        'ollama_ready': juggernaut.ollama_ready,
        'conversation_count': len(juggernaut.conversation_history)
    })

@app.route('/api/system/status')
def system_status():
    """Get system status"""
    return jsonify({
        'metrics': juggernaut.system_metrics,
        'ollama_ready': juggernaut.ollama_ready,
        'model_name': juggernaut.model_name,
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
    print("   JUGGERNAUT AI - OLLAMA SYSTEM")
    print("========================================")
    print("")
    print("RTX 4070 SUPER AI System")
    print("Real Gemma 3 (12B) via Ollama")
    print("Professional Monster UI")
    print("GPU Acceleration: Automatic")
    print("CPU Fallback: Automatic")
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

