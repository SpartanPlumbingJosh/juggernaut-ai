#!/usr/bin/env python3
"""
GEMMA 3 COMMAND LINE INTERFACE
Direct PowerShell integration - No web interface, no bullshit
Real execution, honest responses
"""

import sys
import os
import json
import subprocess
import requests
import argparse
from datetime import datetime
import shutil
import psutil

class GemmaCLI:
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.model = "gemma2:27b"
        self.system_prompt = """You are Gemma 3, a direct and honest AI assistant running via command line.

CRITICAL RULES:
1. NEVER simulate or fake command outputs
2. When asked to execute commands, use the provided system functions
3. Be direct and concise in responses
4. If you can't do something, say so clearly
5. Always provide real, accurate information
6. No web interface nonsense - just direct command execution

You have access to:
- File operations (read, write, delete, copy)
- System commands via subprocess
- Directory operations
- System information gathering
- Real disk usage and system stats

Be helpful, direct, and NEVER fake data."""

    def check_ollama(self):
        """Check if Ollama is running and model is available"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get('models', [])
                available_models = [model['name'] for model in models]
                
                # Try different Gemma model names
                gemma_models = ['gemma2:27b', 'gemma2:9b', 'gemma2', 'gemma:7b', 'gemma']
                for model in gemma_models:
                    if model in available_models:
                        self.model = model
                        print(f"✅ Using model: {model}")
                        return True
                
                print(f"❌ No Gemma models found. Available: {available_models}")
                return False
            else:
                print("❌ Ollama not responding")
                return False
        except Exception as e:
            print(f"❌ Ollama connection failed: {e}")
            return False

    def execute_command(self, command):
        """Execute a real system command"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {'error': 'Command timed out after 30 seconds'}
        except Exception as e:
            return {'error': str(e)}

    def get_system_info(self):
        """Get real system information"""
        try:
            info = {
                'platform': sys.platform,
                'python_version': sys.version,
                'current_directory': os.getcwd(),
                'cpu_count': psutil.cpu_count(),
                'memory_total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
                'memory_available_gb': round(psutil.virtual_memory().available / (1024**3), 2),
                'disk_usage': {}
            }
            
            # Get disk usage for all drives
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

    def chat_with_gemma(self, message, include_system_info=False):
        """Send message to Gemma 3 via Ollama"""
        try:
            # Add system info if requested
            if include_system_info:
                sys_info = self.get_system_info()
                message = f"SYSTEM INFO: {json.dumps(sys_info, indent=2)}\n\nUSER REQUEST: {message}"

            payload = {
                "model": self.model,
                "prompt": message,
                "system": self.system_prompt,
                "stream": False
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", json=payload)
            
            if response.status_code == 200:
                return response.json().get('response', 'No response received')
            else:
                return f"Error: HTTP {response.status_code}"
                
        except Exception as e:
            return f"Error communicating with Gemma: {e}"

    def run_interactive(self):
        """Run interactive command line interface"""
        print("🚀 GEMMA 3 COMMAND LINE INTERFACE")
        print("=" * 50)
        print("Direct PowerShell integration - Real execution only")
        print("Type 'exit' to quit, 'help' for commands")
        print("=" * 50)
        
        if not self.check_ollama():
            print("❌ Cannot connect to Ollama. Make sure it's running.")
            return
        
        while True:
            try:
                user_input = input("\n🤖 Gemma CLI> ").strip()
                
                if user_input.lower() in ['exit', 'quit']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    print("""
AVAILABLE COMMANDS:
- Any natural language request
- 'sysinfo' - Get current system information
- 'exec <command>' - Execute a system command
- 'exit' - Quit the interface

EXAMPLES:
- "Show me disk usage for all drives"
- "exec dir D:\\"
- "Analyze my system performance"
- "Fix the file D:\\JuggernautAI\\static\\integrated_ui.js"
                    """)
                    continue
                
                if user_input.lower() == 'sysinfo':
                    sys_info = self.get_system_info()
                    print(json.dumps(sys_info, indent=2))
                    continue
                
                if user_input.lower().startswith('exec '):
                    command = user_input[5:]
                    print(f"🔧 Executing: {command}")
                    result = self.execute_command(command)
                    
                    if 'error' in result:
                        print(f"❌ Error: {result['error']}")
                    else:
                        if result['stdout']:
                            print(f"📤 Output:\n{result['stdout']}")
                        if result['stderr']:
                            print(f"⚠️ Errors:\n{result['stderr']}")
                        print(f"📊 Return code: {result['returncode']}")
                    continue
                
                # Send to Gemma
                print("🤔 Thinking...")
                response = self.chat_with_gemma(user_input, include_system_info=True)
                print(f"🤖 Gemma: {response}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Gemma 3 Command Line Interface')
    parser.add_argument('--message', '-m', help='Send a single message')
    parser.add_argument('--command', '-c', help='Execute a single command')
    parser.add_argument('--sysinfo', action='store_true', help='Show system information')
    
    args = parser.parse_args()
    
    cli = GemmaCLI()
    
    if args.sysinfo:
        sys_info = cli.get_system_info()
        print(json.dumps(sys_info, indent=2))
        return
    
    if args.command:
        result = cli.execute_command(args.command)
        print(json.dumps(result, indent=2))
        return
    
    if args.message:
        if not cli.check_ollama():
            print("❌ Cannot connect to Ollama")
            return
        response = cli.chat_with_gemma(args.message, include_system_info=True)
        print(response)
        return
    
    # Run interactive mode
    cli.run_interactive()

if __name__ == "__main__":
    main()

