#!/usr/bin/env python3
"""
UNIFIED COMMAND PROCESSOR FOR JUGGERNAUT AI
Intelligent command routing and natural language processing
Integrates all capabilities into a single interface
"""

import os
import sys
import re
import subprocess
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UnifiedCommandProcessor:
    """
    Unified command processor that routes commands to appropriate modules
    Provides natural language interface for all Juggernaut AI capabilities
    """
    
    def __init__(self):
        self.capabilities = {
            'image_generation': {
                'enabled': True,
                'script': 'flux_hf_api.py',
                'keywords': ['image', 'picture', 'generate', 'create', 'draw', 'flux', 'visual']
            },
            'web_interface': {
                'enabled': True,
                'script': 'juggernaut_web_fixed.py',
                'keywords': ['web', 'interface', 'browser', 'ui', 'start', 'launch']
            },
            'discord_bot': {
                'enabled': True,
                'script': 'discord_bot.py',
                'keywords': ['discord', 'bot', 'mobile', 'chat']
            }
        }
        
        self.command_history = []
        logger.info("Unified Command Processor initialized")
    
    def process_command(self, command):
        """
        Process a natural language command and route to appropriate capability
        
        Args:
            command (str): Natural language command
            
        Returns:
            dict: Result with success status and output
        """
        try:
            logger.info(f"Processing command: '{command}'")
            
            # Clean and analyze command
            command_lower = command.lower().strip()
            
            # Store in history
            self.command_history.append({
                'command': command,
                'timestamp': datetime.now().isoformat()
            })
            
            # Route command based on intent
            intent = self.analyze_intent(command_lower)
            
            if intent == 'image_generation':
                return self.handle_image_generation(command)
            elif intent == 'web_interface':
                return self.handle_web_interface(command)
            elif intent == 'discord_bot':
                return self.handle_discord_bot(command)
            elif intent == 'help':
                return self.show_help()
            elif intent == 'status':
                return self.show_status()
            else:
                return self.handle_general_command(command)
                
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            return {
                'success': False,
                'error': f'Command processing failed: {str(e)}',
                'command': command
            }
    
    def analyze_intent(self, command):
        """Analyze command intent based on keywords"""
        
        # Help commands
        if any(word in command for word in ['help', '?', 'commands', 'what can you do']):
            return 'help'
        
        # Status commands
        if any(word in command for word in ['status', 'health', 'check', 'info']):
            return 'status'
        
        # Image generation
        image_patterns = [
            r'generate.*image', r'create.*image', r'make.*image',
            r'draw.*', r'flux.*', r'image.*of', r'picture.*of'
        ]
        if any(re.search(pattern, command) for pattern in image_patterns):
            return 'image_generation'
        
        # Web interface
        if any(word in command for word in ['web', 'interface', 'browser', 'start web', 'launch']):
            return 'web_interface'
        
        # Discord bot
        if any(word in command for word in ['discord', 'bot', 'mobile']):
            return 'discord_bot'
        
        return 'general'
    
    def handle_image_generation(self, command):
        """Handle image generation commands"""
        try:
            # Extract prompt from command
            prompt = self.extract_image_prompt(command)
            
            if not prompt:
                return {
                    'success': False,
                    'error': 'Could not extract image prompt from command',
                    'suggestion': 'Try: "Generate an image of a red sports car"'
                }
            
            # Check if flux_hf_api.py exists
            if not os.path.exists('flux_hf_api.py'):
                return {
                    'success': False,
                    'error': 'FLUX image generator not found (flux_hf_api.py)',
                    'suggestion': 'Make sure flux_hf_api.py is in the current directory'
                }
            
            # Run image generation
            logger.info(f"Generating image with prompt: '{prompt}'")
            
            result = subprocess.run([
                'python', 'flux_hf_api.py', prompt
            ], capture_output=True, text=True, timeout=180)
            
            if result.returncode == 0:
                # Parse output to find generated file
                output_lines = result.stdout.strip().split('\n')
                generated_file = None
                
                for line in output_lines:
                    if 'Image saved successfully:' in line:
                        generated_file = line.split('Image saved successfully: ')[-1].strip()
                        break
                
                return {
                    'success': True,
                    'message': 'Image generated successfully',
                    'file_path': generated_file,
                    'prompt': prompt,
                    'output': result.stdout
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr or result.stdout or 'Unknown error',
                    'prompt': prompt
                }
                
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Image generation timed out',
                'prompt': prompt
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Image generation failed: {str(e)}',
                'prompt': prompt if 'prompt' in locals() else 'unknown'
            }
    
    def extract_image_prompt(self, command):
        """Extract image prompt from natural language command"""
        command_lower = command.lower()
        
        # Patterns to extract prompts
        patterns = [
            r'generate.*image.*of\s+(.+)',
            r'create.*image.*of\s+(.+)',
            r'make.*image.*of\s+(.+)',
            r'generate.*image[:\s]+(.+)',
            r'create.*image[:\s]+(.+)',
            r'draw\s+(.+)',
            r'flux\s+(.+)',
            r'image.*:\s*(.+)',
            r'picture.*:\s*(.+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command_lower)
            if match:
                return match.group(1).strip()
        
        # If no pattern matches, try to extract everything after image-related words
        words_to_remove = ['generate', 'create', 'make', 'image', 'picture', 'of', 'a', 'an', 'the', 'draw', 'flux']
        words = command.split()
        
        # Find the first image-related word and take everything after it
        for i, word in enumerate(words):
            if word.lower() in ['image', 'picture', 'draw', 'flux']:
                remaining_words = words[i+1:]
                # Remove common words
                filtered_words = [w for w in remaining_words if w.lower() not in ['of', 'a', 'an', 'the']]
                if filtered_words:
                    return ' '.join(filtered_words)
        
        return None
    
    def handle_web_interface(self, command):
        """Handle web interface commands"""
        try:
            if not os.path.exists('juggernaut_web_fixed.py'):
                return {
                    'success': False,
                    'error': 'Web interface not found (juggernaut_web_fixed.py)',
                    'suggestion': 'Make sure juggernaut_web_fixed.py is in the current directory'
                }
            
            logger.info("Starting web interface...")
            
            # Start web interface in background
            process = subprocess.Popen([
                'python', 'juggernaut_web_fixed.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            return {
                'success': True,
                'message': 'Web interface started',
                'url': 'http://localhost:5002',
                'process_id': process.pid,
                'instruction': 'Open http://localhost:5002 in your browser'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to start web interface: {str(e)}'
            }
    
    def handle_discord_bot(self, command):
        """Handle Discord bot commands"""
        try:
            if not os.path.exists('discord_bot.py'):
                return {
                    'success': False,
                    'error': 'Discord bot not found (discord_bot.py)',
                    'suggestion': 'Make sure discord_bot.py is in the current directory'
                }
            
            # Check if bot token is set
            bot_token = os.getenv('DISCORD_BOT_TOKEN', '')
            if not bot_token:
                return {
                    'success': False,
                    'error': 'Discord bot token not set',
                    'instruction': 'Set DISCORD_BOT_TOKEN environment variable',
                    'setup_url': 'https://discord.com/developers/applications'
                }
            
            logger.info("Starting Discord bot...")
            
            # Start Discord bot
            process = subprocess.Popen([
                'python', 'discord_bot.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            return {
                'success': True,
                'message': 'Discord bot started',
                'process_id': process.pid,
                'instruction': 'Bot should now be online in your Discord server'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to start Discord bot: {str(e)}'
            }
    
    def handle_general_command(self, command):
        """Handle general commands that don't fit specific categories"""
        return {
            'success': True,
            'message': 'Command received but no specific handler found',
            'command': command,
            'suggestion': 'Try: "generate image of...", "start web interface", or "help"'
        }
    
    def show_help(self):
        """Show help information"""
        help_text = """
🚀 JUGGERNAUT AI UNIFIED COMMAND PROCESSOR

Available Commands:

🎨 IMAGE GENERATION:
  • "Generate an image of a red sports car"
  • "Create image: futuristic city at sunset"
  • "Draw a cat wearing a business suit"
  • "Flux: beautiful landscape"

🌐 WEB INTERFACE:
  • "Start web interface"
  • "Launch browser interface"
  • "Open web UI"

📱 DISCORD BOT:
  • "Start Discord bot"
  • "Launch mobile bot"

📊 SYSTEM:
  • "Help" or "?" - Show this help
  • "Status" - System status
  • "Check health" - System health

💡 TIPS:
  • Use natural language - no need for exact commands
  • Image generation requires HF_TOKEN environment variable
  • Discord bot requires DISCORD_BOT_TOKEN environment variable
  • Web interface opens at http://localhost:5002

Examples:
  python unified_command_processor.py "generate image of a sunset"
  python unified_command_processor.py "start web interface"
  python unified_command_processor.py "help"
        """
        
        return {
            'success': True,
            'message': 'Help information',
            'help_text': help_text.strip()
        }
    
    def show_status(self):
        """Show system status"""
        status = {
            'success': True,
            'message': 'System status',
            'timestamp': datetime.now().isoformat(),
            'capabilities': {}
        }
        
        # Check each capability
        for name, config in self.capabilities.items():
            script_exists = os.path.exists(config['script'])
            status['capabilities'][name] = {
                'enabled': config['enabled'],
                'script': config['script'],
                'available': script_exists,
                'status': '✅ Ready' if script_exists else '❌ Missing'
            }
        
        # Check environment variables
        status['environment'] = {
            'HF_TOKEN': '✅ Set' if os.getenv('HF_TOKEN') else '❌ Not set',
            'DISCORD_BOT_TOKEN': '✅ Set' if os.getenv('DISCORD_BOT_TOKEN') else '❌ Not set'
        }
        
        # Check generated images
        if os.path.exists('generated_images'):
            images = [f for f in os.listdir('generated_images') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            status['generated_images'] = len(images)
        else:
            status['generated_images'] = 0
        
        return status

def main():
    """Main function for command line usage"""
    if len(sys.argv) < 2:
        print("🚀 JUGGERNAUT AI UNIFIED COMMAND PROCESSOR")
        print("=" * 50)
        print()
        print("Usage: python unified_command_processor.py \"your command here\"")
        print()
        print("Examples:")
        print('  python unified_command_processor.py "generate image of a red car"')
        print('  python unified_command_processor.py "start web interface"')
        print('  python unified_command_processor.py "help"')
        print('  python unified_command_processor.py "status"')
        print()
        return
    
    # Get command from arguments
    command = " ".join(sys.argv[1:])
    
    # Create processor and handle command
    processor = UnifiedCommandProcessor()
    result = processor.process_command(command)
    
    # Display result
    if result['success']:
        print(f"✅ {result['message']}")
        
        if 'help_text' in result:
            print(result['help_text'])
        elif 'file_path' in result:
            print(f"📁 File: {result['file_path']}")
        elif 'url' in result:
            print(f"🌐 URL: {result['url']}")
        elif 'instruction' in result:
            print(f"📋 {result['instruction']}")
        
        if 'capabilities' in result:
            print("\n📊 SYSTEM STATUS:")
            for name, info in result['capabilities'].items():
                print(f"  {name}: {info['status']}")
            
            print("\n🔧 ENVIRONMENT:")
            for var, status in result['environment'].items():
                print(f"  {var}: {status}")
            
            print(f"\n🎨 Generated Images: {result['generated_images']}")
    
    else:
        print(f"❌ {result['error']}")
        if 'suggestion' in result:
            print(f"💡 {result['suggestion']}")
        if 'instruction' in result:
            print(f"📋 {result['instruction']}")

if __name__ == "__main__":
    main()

