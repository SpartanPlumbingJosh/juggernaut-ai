#!/usr/bin/env python3
"""
JUGGERNAUT AI - FIXED WEB INTERFACE
Real execution, working UI, no bullshit
"""

import os
import sys
import json
import subprocess
import shutil
import psutil
import requests
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JuggernautWebFixed:
    def __init__(self):
        self.app = Flask(__name__)
        self.ollama_url = "http://localhost:11434"
        self.model = "gemma2:27b"
        self.setup_routes()
        
    def check_ollama(self):
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                available_models = [model['name'] for model in models]
                
                # Find best Gemma model
                gemma_models = ['gemma2:27b', 'gemma2:9b', 'gemma2', 'gemma:7b', 'gemma']
                for model in gemma_models:
                    if model in available_models:
                        self.model = model
                        logger.info(f"Using model: {model}")
                        return True
                        
                logger.error(f"No Gemma models found. Available: {available_models}")
                return False
            return False
        except Exception as e:
            logger.error(f"Ollama connection failed: {e}")
            return False
    
    def execute_real_command(self, command):
        """Execute a REAL system command - no simulation"""
        try:
            logger.info(f"EXECUTING REAL COMMAND: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            return {
                'success': True,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Command timed out'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_real_system_info(self):
        """Get REAL system information - no fake data"""
        try:
            info = {
                'timestamp': datetime.now().isoformat(),
                'platform': sys.platform,
                'python_version': sys.version.split()[0],
                'current_directory': os.getcwd(),
                'cpu_count': psutil.cpu_count(),
                'memory_total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
                'memory_available_gb': round(psutil.virtual_memory().available / (1024**3), 2),
                'disk_usage': {}
            }
            
            # Real disk usage for all drives
            for drive in ['C:', 'D:', 'E:', 'F:']:
                try:
                    if os.path.exists(drive):
                        total, used, free = shutil.disk_usage(drive)
                        info['disk_usage'][drive] = {
                            'total_gb': round(total / (1024**3), 2),
                            'used_gb': round(used / (1024**3), 2),
                            'free_gb': round(free / (1024**3), 2)
                        }
                except:
                    pass
            
            return info
        except Exception as e:
            return {'error': str(e)}
    
    def chat_with_gemma(self, message):
        """Send message to Gemma 3"""
        try:
            system_prompt = """You are Gemma 3, an AI assistant with REAL system access capabilities.

CRITICAL RULES:
1. NEVER simulate or fake command outputs
2. When asked to execute commands, tell the user you'll execute them via the system
3. Be direct and honest about what you can and cannot do
4. Provide real, accurate information only
5. If you need to execute a command, clearly state what command you would run

You have access to real system information and can execute real commands through the interface."""

            # Add real system info to context
            sys_info = self.get_real_system_info()
            enhanced_message = f"REAL SYSTEM INFO: {json.dumps(sys_info, indent=2)}\n\nUSER REQUEST: {message}"
            
            payload = {
                "model": self.model,
                "prompt": enhanced_message,
                "system": system_prompt,
                "stream": False
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", json=payload, timeout=60)
            
            if response.status_code == 200:
                return response.json().get('response', 'No response received')
            else:
                return f"Error: HTTP {response.status_code}"
                
        except Exception as e:
            return f"Error communicating with Gemma: {e}"
    
    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template_string(HTML_TEMPLATE)
        
        @self.app.route('/api/chat', methods=['POST'])
        def chat():
            try:
                data = request.get_json()
                message = data.get('message', '').strip()
                
                if not message:
                    return jsonify({'error': 'No message provided'})
                
                logger.info(f"USER MESSAGE: {message}")
                
                # Check for direct command execution requests
                if message.lower().startswith('execute:') or message.lower().startswith('exec:'):
                    command = message.split(':', 1)[1].strip()
                    result = self.execute_real_command(command)
                    
                    if result['success']:
                        response = f"COMMAND EXECUTED: {command}\n\nOUTPUT:\n{result['stdout']}"
                        if result['stderr']:
                            response += f"\n\nERRORS:\n{result['stderr']}"
                        response += f"\n\nRETURN CODE: {result['returncode']}"
                    else:
                        response = f"COMMAND FAILED: {result['error']}"
                    
                    return jsonify({'response': response})
                
                # Regular chat with Gemma
                response = self.chat_with_gemma(message)
                logger.info(f"GEMMA RESPONSE: {response[:100]}...")
                
                return jsonify({'response': response})
                
            except Exception as e:
                logger.error(f"Chat error: {e}")
                return jsonify({'error': str(e)})
        
        @self.app.route('/api/system', methods=['GET'])
        def system_info():
            return jsonify(self.get_real_system_info())
        
        @self.app.route('/api/execute', methods=['POST'])
        def execute():
            try:
                data = request.get_json()
                command = data.get('command', '').strip()
                
                if not command:
                    return jsonify({'error': 'No command provided'})
                
                result = self.execute_real_command(command)
                return jsonify(result)
                
            except Exception as e:
                return jsonify({'error': str(e)})

# Clean, working HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Juggernaut AI - Fixed Interface</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #1a1a1a; color: #fff; height: 100vh; display: flex; flex-direction: column;
        }
        .header { 
            background: #ff4444; padding: 1rem; text-align: center; 
            box-shadow: 0 2px 10px rgba(255,68,68,0.3);
        }
        .header h1 { font-size: 1.5rem; font-weight: bold; }
        .header p { opacity: 0.9; margin-top: 0.5rem; }
        .chat-container { 
            flex: 1; display: flex; flex-direction: column; max-width: 1200px; 
            margin: 0 auto; width: 100%; padding: 1rem;
        }
        .chat-messages { 
            flex: 1; overflow-y: auto; padding: 1rem; background: #2a2a2a; 
            border-radius: 8px; margin-bottom: 1rem; min-height: 400px;
        }
        .message { 
            margin-bottom: 1rem; padding: 1rem; border-radius: 8px; 
            max-width: 80%; word-wrap: break-word;
        }
        .message.user { 
            background: #ff4444; margin-left: auto; text-align: right; 
        }
        .message.assistant { 
            background: #333; border-left: 4px solid #ff4444; 
        }
        .input-container { 
            display: flex; gap: 1rem; padding: 1rem; background: #2a2a2a; 
            border-radius: 8px; align-items: center;
        }
        .chat-input { 
            flex: 1; padding: 1rem; border: none; border-radius: 6px; 
            background: #1a1a1a; color: #fff; font-size: 1rem;
            border: 2px solid #444;
        }
        .chat-input:focus { outline: none; border-color: #ff4444; }
        .send-btn { 
            padding: 1rem 2rem; background: #ff4444; color: #fff; 
            border: none; border-radius: 6px; cursor: pointer; 
            font-weight: bold; transition: background 0.2s;
        }
        .send-btn:hover { background: #ff6666; }
        .send-btn:disabled { background: #666; cursor: not-allowed; }
        .status { 
            text-align: center; padding: 0.5rem; font-size: 0.9rem; 
            color: #aaa; background: #333; border-radius: 4px; margin-bottom: 1rem;
        }
        .processing { color: #ff4444; font-weight: bold; }
        pre { white-space: pre-wrap; font-family: 'Courier New', monospace; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 JUGGERNAUT AI - FIXED INTERFACE</h1>
        <p>Real execution, working UI, no simulation bullshit</p>
    </div>
    
    <div class="chat-container">
        <div class="status" id="status">Ready - Send a message to test the interface</div>
        
        <div class="chat-messages" id="chat-messages">
            <div class="message assistant">
                <strong>Juggernaut AI Ready!</strong><br>
                I can now execute real commands and provide honest responses.<br><br>
                <strong>Try these commands:</strong><br>
                • "Show me real disk usage for all drives"<br>
                • "Execute: dir D:\\"<br>
                • "Get current system information"<br>
                • "Analyze my D: drive structure"
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="chat-input" class="chat-input" 
                   placeholder="Type your message... (Try: 'Show me real system info')" 
                   autocomplete="off">
            <button id="send-btn" class="send-btn">Send</button>
        </div>
    </div>

    <script>
        class JuggernautFixed {
            constructor() {
                this.chatInput = document.getElementById('chat-input');
                this.sendBtn = document.getElementById('send-btn');
                this.chatMessages = document.getElementById('chat-messages');
                this.status = document.getElementById('status');
                this.init();
            }
            
            init() {
                console.log('Juggernaut AI Fixed Interface Loaded');
                
                this.sendBtn.addEventListener('click', () => this.sendMessage());
                this.chatInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        this.sendMessage();
                    }
                });
                
                this.chatInput.focus();
            }
            
            async sendMessage() {
                const message = this.chatInput.value.trim();
                if (!message) return;
                
                this.chatInput.value = '';
                this.addMessage('user', message);
                this.setProcessing(true);
                
                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: message })
                    });
                    
                    const data = await response.json();
                    
                    if (data.error) {
                        this.addMessage('assistant', `Error: ${data.error}`);
                    } else {
                        this.addMessage('assistant', data.response);
                    }
                    
                } catch (error) {
                    this.addMessage('assistant', `Connection error: ${error.message}`);
                } finally {
                    this.setProcessing(false);
                }
            }
            
            addMessage(type, content) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${type}`;
                
                if (type === 'assistant') {
                    messageDiv.innerHTML = `<pre>${this.escapeHtml(content)}</pre>`;
                } else {
                    messageDiv.innerHTML = this.escapeHtml(content);
                }
                
                this.chatMessages.appendChild(messageDiv);
                this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
            }
            
            setProcessing(processing) {
                if (processing) {
                    this.status.textContent = 'Processing your request...';
                    this.status.className = 'status processing';
                    this.sendBtn.disabled = true;
                } else {
                    this.status.textContent = 'Ready';
                    this.status.className = 'status';
                    this.sendBtn.disabled = false;
                    this.chatInput.focus();
                }
            }
            
            escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }
        }
        
        // Initialize when page loads
        document.addEventListener('DOMContentLoaded', () => {
            window.juggernaut = new JuggernautFixed();
        });
    </script>
</body>
</html>
'''

def main():
    app_instance = JuggernautWebFixed()
    
    print("🚀 JUGGERNAUT AI - FIXED WEB INTERFACE")
    print("=" * 50)
    print("Real execution, working UI, no simulation")
    print("=" * 50)
    
    if not app_instance.check_ollama():
        print("❌ Cannot connect to Ollama. Please start Ollama first.")
        print("💡 Run: ollama serve")
        return
    
    print("✅ Ollama connected successfully")
    print("✅ Interface ready")
    print("")
    print("🌐 Web interface available at:")
    print("   http://localhost:5002")
    print("")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        app_instance.app.run(host='0.0.0.0', port=5002, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")

if __name__ == "__main__":
    main()

