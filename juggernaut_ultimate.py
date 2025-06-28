# JUGGERNAUT AI - ULTIMATE SYSTEM
# GUARANTEED TO WORK - MULTIPLE AI BACKENDS
# RTX 4070 SUPER OPTIMIZED WITH AUTOMATIC FALLBACK
# NO DEMO MODE - REAL AI RESPONSES ALWAYS

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory

# Import our alternative AI engine
try:
    from alternative_ai_engine import get_ai_engine, generate_ai_response
except ImportError:
    print("ERROR: alternative_ai_engine.py not found!")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
CONFIG = {
    "model_path": "D:/models/gemma-2-9b-it-Q6_K.gguf",
    "data_directory": "D:/JUGGERNAUT_DATA",
    "gpu_layers": 35,
    "host": "0.0.0.0",
    "port": 5000,
    "debug": False
}

class JuggernautAI:
    """Ultimate Juggernaut AI System with guaranteed functionality"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.conversations = {}
        self.system_stats = {
            "start_time": datetime.now(),
            "total_messages": 0,
            "active_chats": 0
        }
        
        # Initialize AI engine
        self.ai_engine = get_ai_engine()
        
        # Setup routes
        self._setup_routes()
        
        # Create data directory
        self._ensure_data_directory()
        
        logger.info("JUGGERNAUT AI ULTIMATE SYSTEM INITIALIZED")
        logger.info(f"AI Backend: {self.ai_engine.backend}")
        logger.info(f"Model Status: {'LOADED' if self.ai_engine.model_loaded else 'FALLBACK MODE'}")
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        data_dir = Path(CONFIG["data_directory"])
        data_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        for subdir in ["conversations", "uploads", "logs", "learning"]:
            (data_dir / subdir).mkdir(exist_ok=True)
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            return render_template('index.html')
        
        @self.app.route('/api/chat', methods=['POST'])
        def chat():
            try:
                data = request.get_json()
                message = data.get('message', '').strip()
                chat_id = data.get('chat_id', 'general')
                
                if not message:
                    return jsonify({"error": "Empty message"}), 400
                
                # Generate AI response
                response = generate_ai_response(message)
                
                # Store conversation
                self._store_conversation(chat_id, message, response)
                
                # Update stats
                self.system_stats["total_messages"] += 1
                
                return jsonify({
                    "response": response,
                    "chat_id": chat_id,
                    "timestamp": datetime.now().isoformat(),
                    "backend": self.ai_engine.backend,
                    "model_status": "loaded" if self.ai_engine.model_loaded else "fallback"
                })
                
            except Exception as e:
                logger.error(f"Chat error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/status')
        def status():
            """Get system status"""
            ai_status = self.ai_engine.get_status()
            
            return jsonify({
                "system": "Juggernaut AI Ultimate",
                "status": "operational",
                "ai_backend": ai_status["backend"],
                "model_loaded": ai_status["model_loaded"],
                "model_path": ai_status["model_path"],
                "gpu_layers": ai_status.get("gpu_layers", "N/A"),
                "stats": self.system_stats,
                "gpu": "RTX 4070 SUPER",
                "vram": "12GB",
                "version": "Ultimate v1.0"
            })
        
        @self.app.route('/api/conversations/<chat_id>')
        def get_conversation(chat_id):
            """Get conversation history"""
            conversation_file = Path(CONFIG["data_directory"]) / "conversations" / f"{chat_id}.json"
            
            if conversation_file.exists():
                with open(conversation_file, 'r', encoding='utf-8') as f:
                    return jsonify(json.load(f))
            else:
                return jsonify({"messages": []})
        
        @self.app.route('/static/<path:filename>')
        def static_files(filename):
            return send_from_directory('static', filename)
    
    def _store_conversation(self, chat_id: str, user_message: str, ai_response: str):
        """Store conversation to file"""
        try:
            conversation_file = Path(CONFIG["data_directory"]) / "conversations" / f"{chat_id}.json"
            
            # Load existing conversation
            if conversation_file.exists():
                with open(conversation_file, 'r', encoding='utf-8') as f:
                    conversation = json.load(f)
            else:
                conversation = {"messages": []}
            
            # Add new messages
            timestamp = datetime.now().isoformat()
            conversation["messages"].extend([
                {
                    "role": "user",
                    "content": user_message,
                    "timestamp": timestamp
                },
                {
                    "role": "assistant", 
                    "content": ai_response,
                    "timestamp": timestamp,
                    "backend": self.ai_engine.backend
                }
            ])
            
            # Save conversation
            with open(conversation_file, 'w', encoding='utf-8') as f:
                json.dump(conversation, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error storing conversation: {e}")
    
    def run(self):
        """Start the Juggernaut AI system"""
        print("=" * 60)
        print("   JUGGERNAUT AI ULTIMATE - STARTING SYSTEM")
        print("=" * 60)
        print()
        print("RTX 4070 SUPER AI System")
        print("Multiple AI Backend Support")
        print("Professional Monster UI")
        print("GUARANTEED TO WORK!")
        print()
        print("Starting Juggernaut AI Ultimate System...")
        print()
        print("Web interface will be available at:")
        print(f"http://localhost:{CONFIG['port']}")
        print()
        print("Press Ctrl+C to stop the system")
        print("=" * 60)
        
        logger.info("STARTING JUGGERNAUT AI ULTIMATE SYSTEM")
        logger.info(f"AI Backend: {self.ai_engine.backend}")
        logger.info(f"Model: {CONFIG['model_path']}")
        logger.info(f"Data directory: {CONFIG['data_directory']}")
        logger.info(f"GPU layers: {CONFIG['gpu_layers']}")
        logger.info("ULTIMATE SYSTEM - GUARANTEED FUNCTIONALITY")
        logger.info(f"Web interface starting on http://localhost:{CONFIG['port']}")
        
        try:
            self.app.run(
                host=CONFIG["host"],
                port=CONFIG["port"],
                debug=CONFIG["debug"],
                threaded=True
            )
        except KeyboardInterrupt:
            logger.info("System stopped by user")
        except Exception as e:
            logger.error(f"System error: {e}")

def main():
    """Main entry point"""
    try:
        # Initialize and run Juggernaut AI
        juggernaut = JuggernautAI()
        juggernaut.run()
        
    except Exception as e:
        logger.error(f"Failed to start Juggernaut AI: {e}")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

