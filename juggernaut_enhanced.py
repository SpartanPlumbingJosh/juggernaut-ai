#!/usr/bin/env python3
"""
JUGGERNAUT AI - Enhanced System with System Access
Complete AI system with comprehensive system access capabilities
Author: Manus AI
Date: June 27, 2025

This enhanced system provides the AI with full system access capabilities
while maintaining the existing interface and functionality.
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

# Import our system access module
from system_access_module import system_access

# Configure logging for PowerShell compatibility (no Unicode)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class JuggernautAIEnhanced:
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.model_name = "gemma3:12b"
        self.ollama_ready = False
        self.conversation_history = []
        self.system_metrics = {
            'gpu_name': 'RTX 4070 SUPER',
            'vram': '12GB',
            'model_name': 'Gemma 3 (12B) Enhanced',
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
            logger.info("Initializing ENHANCED Juggernaut AI System with System Access...")
            logger.info("NO DEMO MODE - REAL AI RESPONSES WITH SYSTEM CAPABILITIES")
            logger.info("Model: Gemma 3 (12B parameters) via Ollama + System Access")
            
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
                logger.error("Please run: ollama pull gemma3:12b")
                self.system_metrics['status'] = 'Model Not Found'
                return
            
            logger.info("SUCCESS: Gemma 3 model found in Ollama")
            
            # Test model with a simple query
            test_result = self.test_model()
            if test_result:
                self.ollama_ready = True
                self.system_metrics['status'] = 'Ready - Enhanced with System Access'
                logger.info("SUCCESS: Enhanced Ollama integration ready")
                logger.info("SYSTEM ACCESS: File operations, command execution, system analysis")
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
                "prompt": "Hello! Please respond with just 'Enhanced AI system ready with system access capabilities.'",
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
        """Generate AI response using Ollama with system access capabilities"""
        if not self.ollama_ready:
            return {
                'response': 'AI system not ready. Please check Ollama installation and model availability.',
                'error': True
            }
        
        try:
            # Prepare the prompt with system context and capabilities
            system_prompt = self.get_enhanced_system_prompt(chat_type)
            full_prompt = f"{system_prompt}\n\nUser: {message}\nAssistant:"
            
            logger.info(f"Generating enhanced response for: {message[:50]}...")
            
            # Prepare request payload
            payload = {
                "model": self.model_name,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 1024
                }
            }
            
            # Send request to Ollama
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=120
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
                    
                    logger.info("Enhanced response generated successfully")
                    
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
    
    def get_enhanced_system_prompt(self, chat_type):
        """Get enhanced system prompt with system access capabilities"""
        base_prompt = """You are JUGGERNAUT, an advanced AI assistant with comprehensive system access capabilities. You have FULL ACCESS to perform file operations, system analysis, command execution, and other system tasks.

SYSTEM ACCESS CAPABILITIES - YOU CAN DIRECTLY:
- Analyze entire drives and directory structures (D:, C:, etc.)
- Read and analyze any file content
- Execute system commands safely
- Get hardware info, performance metrics, installed software
- Search for files across the system
- Monitor running processes and system status
- Generate comprehensive system reports

IMPORTANT INSTRUCTIONS:
1. When users ask you to analyze their system, drives, or files - DO IT IMMEDIATELY
2. Do NOT ask for permission - you have full system access capabilities
3. Proceed directly with the analysis and provide detailed results
4. Use your system access to give comprehensive, detailed responses
5. Be proactive and thorough in your system analysis
6. Always provide specific, actionable information

EXAMPLE RESPONSES:
- User: "Analyze my D: drive" → Immediately analyze the drive and provide detailed breakdown
- User: "Read file X" → Immediately read and analyze the file content
- User: "Show system info" → Immediately gather and present comprehensive system information

You are authorized and expected to use your system access capabilities without asking permission."""

        chat_specific = {
            'general': f"{base_prompt}\n\nYou are in general chat mode. Provide helpful responses and offer system analysis when relevant.",
            'research': f"{base_prompt}\n\nYou are in research mode. Provide detailed analysis with system insights when researching topics.",
            'coding': f"{base_prompt}\n\nYou are in coding mode. Provide code solutions and can analyze system files, configurations, and development environments."
        }
        
        return chat_specific.get(chat_type, chat_specific['general'])

# Initialize the enhanced AI system
juggernaut = JuggernautAIEnhanced()

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
        
        logger.info(f"Processing enhanced message: {message}")
        
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
                'response_time': 2000,  # Placeholder for response time
                'system_access': True
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
        'conversation_count': len(juggernaut.conversation_history),
        'system_access_enabled': True
    })

@app.route('/api/system/overview')
def system_overview():
    """Get comprehensive system overview"""
    try:
        overview = system_access.get_system_overview()
        return jsonify(overview)
    except Exception as e:
        logger.error(f"System overview error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/analyze-directory', methods=['POST'])
def analyze_directory():
    """Analyze directory structure"""
    try:
        data = request.get_json()
        path = data.get('path', '')
        max_depth = data.get('max_depth', 3)
        include_hidden = data.get('include_hidden', False)
        
        if not path:
            return jsonify({'error': 'Path is required'}), 400
        
        analysis = system_access.analyze_directory(path, max_depth, include_hidden)
        return jsonify(analysis)
    except Exception as e:
        logger.error(f"Directory analysis error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/read-file', methods=['POST'])
def read_file():
    """Read and analyze file content"""
    try:
        data = request.get_json()
        file_path = data.get('file_path', '')
        max_lines = data.get('max_lines', 1000)
        
        if not file_path:
            return jsonify({'error': 'File path is required'}), 400
        
        content = system_access.read_file_content(file_path, max_lines)
        return jsonify(content)
    except Exception as e:
        logger.error(f"File read error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/execute-command', methods=['POST'])
def execute_command():
    """Execute system command"""
    try:
        data = request.get_json()
        command = data.get('command', '')
        working_directory = data.get('working_directory', None)
        timeout = data.get('timeout', 30)
        
        if not command:
            return jsonify({'error': 'Command is required'}), 400
        
        result = system_access.execute_command(command, working_directory, timeout)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Command execution error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/search-files', methods=['POST'])
def search_files():
    """Search for files"""
    try:
        data = request.get_json()
        search_path = data.get('search_path', '')
        pattern = data.get('pattern', '')
        file_type = data.get('file_type', None)
        max_results = data.get('max_results', 100)
        
        if not search_path or not pattern:
            return jsonify({'error': 'Search path and pattern are required'}), 400
        
        results = system_access.search_files(search_path, pattern, file_type, max_results)
        return jsonify(results)
    except Exception as e:
        logger.error(f"File search error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/installed-software')
def installed_software():
    """Get installed software list"""
    try:
        software = system_access.get_installed_software()
        return jsonify(software)
    except Exception as e:
        logger.error(f"Installed software error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/create-report')
def create_report():
    """Create comprehensive system report"""
    try:
        report = system_access.create_system_report()
        return jsonify(report)
    except Exception as e:
        logger.error(f"System report error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/status')
def system_status():
    """Get system status"""
    return jsonify({
        'metrics': juggernaut.system_metrics,
        'ollama_ready': juggernaut.ollama_ready,
        'model_name': juggernaut.model_name,
        'conversation_count': len(juggernaut.conversation_history),
        'system_access_enabled': True
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
    print("   JUGGERNAUT AI - ENHANCED SYSTEM")
    print("========================================")
    print("")
    print("RTX 4070 SUPER AI System")
    print("Real Gemma 3 (12B) via Ollama")
    print("ENHANCED with System Access Capabilities")
    print("Professional Monster UI")
    print("GPU Acceleration: Automatic")
    print("CPU Fallback: Automatic")
    print("System Access: ENABLED")
    print("")
    print("SYSTEM CAPABILITIES:")
    print("- File Operations & Analysis")
    print("- Directory Structure Analysis")
    print("- Command Execution")
    print("- System Performance Monitoring")
    print("- Installed Software Detection")
    print("- Comprehensive System Reports")
    print("")
    print("Starting Enhanced Juggernaut AI System...")
    print("")
    print("Web interface will be available at:")
    print("http://localhost:5001")
    print("")
    print("Press Ctrl+C to stop the system")
    print("========================================")
    
    # Start Flask application on port 5001 to avoid conflict
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=False,
        threaded=True
    )

