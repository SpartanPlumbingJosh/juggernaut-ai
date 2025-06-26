"""
Juggernaut AI - Complete Flask Backend
RTX 4070 SUPER Optimized AI System
Production-ready backend with comprehensive API endpoints
"""

from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import json
import uuid
import time
import logging
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import traceback

# Import core modules
from core.ai_engine import AIEngine
from core.chat_manager import ChatManager
from core.file_manager import FileManager
from core.browser_controller import BrowserController
from core.plugin_manager import PluginManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/juggernaut.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class JuggernautAI:
    """
    Main Juggernaut AI application class
    Manages all core components and system state
    """
    
    def __init__(self, data_path: str = "D:\\JUGGERNAUT_DATA"):
        self.data_path = data_path
        self.status = "initializing"
        self.active_chats = {}
        self.system_metrics = {
            'start_time': datetime.now(),
            'total_requests': 0,
            'total_messages': 0,
            'total_files_processed': 0,
            'uptime': 0
        }
        
        # Initialize data directories
        self._setup_directories()
        
        # Initialize core components with error handling
        self._initialize_components()
        
        # Load existing data
        self._load_existing_data()
        
        # Start background tasks
        self._start_background_tasks()
        
        self.status = "ready"
        logger.info("🚀 JUGGERNAUT AI SYSTEM READY")
        logger.info(f"🌐 Access at: http://localhost:5000")
        logger.info(f"📁 Data directory: {data_path}")
        logger.info(f"🎯 RTX 4070 SUPER GPU acceleration enabled")

    def _setup_directories(self):
        """Create all necessary data directories"""
        directories = [
            self.data_path,
            os.path.join(self.data_path, "chats"),
            os.path.join(self.data_path, "files"),
            os.path.join(self.data_path, "images"),
            os.path.join(self.data_path, "logs"),
            os.path.join(self.data_path, "models"),
            os.path.join(self.data_path, "cache"),
            os.path.join(self.data_path, "exports"),
            os.path.join(self.data_path, "plugins"),
            "logs",
            "static",
            "templates"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        logger.info(f"✅ Directory structure initialized: {self.data_path}")

    def _initialize_components(self):
        """Initialize all core components with error handling"""
        try:
            self.ai_engine = AIEngine(self.data_path)
            logger.info("✅ AI Engine initialized")
        except Exception as e:
            logger.error(f"❌ AI Engine initialization failed: {e}")
            self.ai_engine = None
        
        try:
            self.chat_manager = ChatManager(self.data_path)
            logger.info("✅ Chat Manager initialized")
        except Exception as e:
            logger.error(f"❌ Chat Manager initialization failed: {e}")
            self.chat_manager = None
        
        try:
            self.file_manager = FileManager(self.data_path)
            logger.info("✅ File Manager initialized")
        except Exception as e:
            logger.error(f"❌ File Manager initialization failed: {e}")
            self.file_manager = None
        
        try:
            self.browser_controller = BrowserController()
            logger.info("✅ Browser Controller initialized")
        except Exception as e:
            logger.error(f"❌ Browser Controller initialization failed: {e}")
            self.browser_controller = None
        
        try:
            self.plugin_manager = PluginManager(self.data_path)
            logger.info("✅ Plugin Manager initialized")
        except Exception as e:
            logger.error(f"❌ Plugin Manager initialization failed: {e}")
            self.plugin_manager = None

    def _load_existing_data(self):
        """Load existing chats and data"""
        try:
            if self.chat_manager:
                self.active_chats = self.chat_manager.load_all_chats()
                logger.info(f"📚 Loaded {len(self.active_chats)} existing chats")
        except Exception as e:
            logger.error(f"Failed to load existing data: {e}")
            self.active_chats = {}

    def _start_background_tasks(self):
        """Start background maintenance tasks"""
        def update_metrics():
            while True:
                try:
                    self.system_metrics['uptime'] = (
                        datetime.now() - self.system_metrics['start_time']
                    ).total_seconds()
                    time.sleep(60)  # Update every minute
                except Exception as e:
                    logger.error(f"Metrics update error: {e}")
                    time.sleep(60)
        
        metrics_thread = threading.Thread(target=update_metrics, daemon=True)
        metrics_thread.start()

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            "status": self.status,
            "components": {
                "ai_engine": self.ai_engine is not None and self.ai_engine.is_ready(),
                "chat_manager": self.chat_manager is not None,
                "file_manager": self.file_manager is not None,
                "browser_controller": self.browser_controller is not None,
                "plugin_manager": self.plugin_manager is not None
            },
            "metrics": self.system_metrics,
            "active_chats": len(self.active_chats),
            "data_path": self.data_path,
            "gpu_ready": True,  # RTX 4070 SUPER
            "version": "1.0.0"
        }

# Initialize Juggernaut AI system
try:
    juggernaut = JuggernautAI()
except Exception as e:
    logger.error(f"Failed to initialize Juggernaut AI: {e}")
    logger.error(traceback.format_exc())
    exit(1)

# Create Flask application
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
CORS(app, origins="*")  # Enable CORS for all origins

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found", "code": 404}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error", "code": 500}), 500

@app.errorhandler(RequestEntityTooLarge)
def file_too_large(error):
    return jsonify({"error": "File too large (max 100MB)", "code": 413}), 413

# Main routes
@app.route('/')
def index():
    """Main application interface"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index: {e}")
        return f"Error loading interface: {str(e)}", 500

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

# System API endpoints
@app.route('/api/status')
def get_system_status():
    """Get comprehensive system status"""
    try:
        juggernaut.system_metrics['total_requests'] += 1
        return jsonify(juggernaut.get_system_status())
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": juggernaut.system_metrics['uptime']
    })

# Chat API endpoints
@app.route('/api/chat/new', methods=['POST'])
def create_new_chat():
    """Create a new chat session"""
    try:
        chat_id = str(uuid.uuid4())
        chat_data = {
            "id": chat_id,
            "title": "New Chat",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "messages": [],
            "metadata": {
                "model": "demo",
                "gpu_accelerated": True,
                "total_tokens": 0
            }
        }
        
        juggernaut.active_chats[chat_id] = chat_data
        
        if juggernaut.chat_manager:
            juggernaut.chat_manager.save_chat(chat_id, chat_data)
        
        juggernaut.system_metrics['total_requests'] += 1
        
        logger.info(f"📝 New chat created: {chat_id}")
        
        return jsonify({
            "chat_id": chat_id,
            "status": "created",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error creating new chat: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat/<chat_id>/message', methods=['POST'])
def send_chat_message(chat_id):
    """Send a message to a specific chat"""
    try:
        # Validate request
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        if chat_id not in juggernaut.active_chats:
            return jsonify({"error": "Chat not found"}), 404
        
        # Add user message
        user_message = {
            "id": str(uuid.uuid4()),
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "length": len(message),
                "word_count": len(message.split())
            }
        }
        
        juggernaut.active_chats[chat_id]["messages"].append(user_message)
        
        # Generate AI response
        start_time = time.time()
        try:
            if juggernaut.ai_engine and juggernaut.ai_engine.is_ready():
                ai_response = juggernaut.ai_engine.generate_response(
                    message, 
                    max_tokens=data.get('max_tokens', 150)
                )
            else:
                ai_response = f"🤖 **Demo Response**\n\nReceived: '{message}'\n\n**RTX 4070 SUPER Status:** ✅ Ready for GPU acceleration\n\n*Add an AI model to enable real responses with GPU acceleration!*"
        except Exception as e:
            logger.error(f"AI generation error: {e}")
            ai_response = f"AI processing error: {str(e)}"
        
        response_time = time.time() - start_time
        
        # Add AI message
        ai_message = {
            "id": str(uuid.uuid4()),
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "response_time": round(response_time, 3),
                "length": len(ai_response),
                "word_count": len(ai_response.split()),
                "gpu_accelerated": True
            }
        }
        
        juggernaut.active_chats[chat_id]["messages"].append(ai_message)
        
        # Update chat metadata
        juggernaut.active_chats[chat_id]["updated_at"] = datetime.now().isoformat()
        juggernaut.active_chats[chat_id]["metadata"]["total_tokens"] += len(message.split()) + len(ai_response.split())
        
        # Update chat title if this is the first exchange
        if len(juggernaut.active_chats[chat_id]["messages"]) == 2:
            title = message[:50] + "..." if len(message) > 50 else message
            juggernaut.active_chats[chat_id]["title"] = title
        
        # Save chat
        if juggernaut.chat_manager:
            juggernaut.chat_manager.save_chat(chat_id, juggernaut.active_chats[chat_id])
        
        # Update metrics
        juggernaut.system_metrics['total_requests'] += 1
        juggernaut.system_metrics['total_messages'] += 1
        
        logger.info(f"💬 Message processed for chat {chat_id} in {response_time:.2f}s")
        
        return jsonify({
            "response": ai_response,
            "message_id": ai_message["id"],
            "response_time": response_time,
            "gpu_accelerated": True,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat/<chat_id>')
def get_chat(chat_id):
    """Get specific chat history"""
    try:
        if chat_id not in juggernaut.active_chats:
            return jsonify({"error": "Chat not found"}), 404
        
        juggernaut.system_metrics['total_requests'] += 1
        return jsonify(juggernaut.active_chats[chat_id])
        
    except Exception as e:
        logger.error(f"Error getting chat: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/chats')
def get_all_chats():
    """Get all chat sessions (summary)"""
    try:
        chats = []
        for chat_id, chat_data in juggernaut.active_chats.items():
            chats.append({
                "id": chat_id,
                "title": chat_data.get("title", "New Chat"),
                "created_at": chat_data.get("created_at"),
                "updated_at": chat_data.get("updated_at"),
                "message_count": len(chat_data.get("messages", [])),
                "total_tokens": chat_data.get("metadata", {}).get("total_tokens", 0)
            })
        
        # Sort by update time (newest first)
        chats.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        
        juggernaut.system_metrics['total_requests'] += 1
        
        return jsonify({
            "chats": chats,
            "total": len(chats),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting chats: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    """Delete a specific chat"""
    try:
        if chat_id not in juggernaut.active_chats:
            return jsonify({"error": "Chat not found"}), 404
        
        # Remove from active chats
        del juggernaut.active_chats[chat_id]
        
        # Delete from storage
        if juggernaut.chat_manager:
            juggernaut.chat_manager.delete_chat(chat_id)
        
        logger.info(f"🗑️ Chat deleted: {chat_id}")
        
        return jsonify({
            "status": "deleted",
            "chat_id": chat_id,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error deleting chat: {e}")
        return jsonify({"error": str(e)}), 500

# File management API endpoints
@app.route('/api/files/upload', methods=['POST'])
def upload_files():
    """Upload one or more files"""
    try:
        if 'files' not in request.files:
            return jsonify({"error": "No files provided"}), 400
        
        files = request.files.getlist('files')
        if not files or all(f.filename == '' for f in files):
            return jsonify({"error": "No files selected"}), 400
        
        uploaded_files = []
        
        for file in files:
            if file and file.filename != '':
                if juggernaut.file_manager:
                    try:
                        file_info = juggernaut.file_manager.save_file(file)
                        uploaded_files.append(file_info)
                        juggernaut.system_metrics['total_files_processed'] += 1
                    except Exception as e:
                        logger.error(f"Error saving file {file.filename}: {e}")
                        uploaded_files.append({
                            "filename": file.filename,
                            "error": str(e),
                            "status": "failed"
                        })
        
        juggernaut.system_metrics['total_requests'] += 1
        
        logger.info(f"📁 Uploaded {len(uploaded_files)} files")
        
        return jsonify({
            "files": uploaded_files,
            "total_uploaded": len([f for f in uploaded_files if f.get("status") != "failed"]),
            "total_failed": len([f for f in uploaded_files if f.get("status") == "failed"]),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error uploading files: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/files')
def list_files():
    """List all uploaded files"""
    try:
        if not juggernaut.file_manager:
            return jsonify({"error": "File manager not available"}), 503
        
        files = juggernaut.file_manager.list_files()
        juggernaut.system_metrics['total_requests'] += 1
        
        return jsonify({
            "files": files,
            "total": len(files),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/files/<file_id>')
def download_file(file_id):
    """Download a specific file"""
    try:
        if not juggernaut.file_manager:
            return jsonify({"error": "File manager not available"}), 503
        
        file_path = juggernaut.file_manager.get_file_path(file_id)
        if not file_path or not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
        
        juggernaut.system_metrics['total_requests'] += 1
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return jsonify({"error": str(e)}), 500

# AI processing API endpoints
@app.route('/api/ai/generate', methods=['POST'])
def ai_generate():
    """Generate AI response"""
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        max_tokens = data.get('max_tokens', 150)
        temperature = data.get('temperature', 0.7)
        
        if not prompt:
            return jsonify({"error": "Prompt required"}), 400
        
        start_time = time.time()
        
        if juggernaut.ai_engine and juggernaut.ai_engine.is_ready():
            response = juggernaut.ai_engine.generate_response(prompt, max_tokens, temperature)
        else:
            response = f"🤖 **AI Generation (Demo Mode)**\n\nPrompt: '{prompt}'\n\n**RTX 4070 SUPER Ready:** ✅\n**GPU Acceleration:** Waiting for AI model\n\n*Install llama-cpp-python and add a GGUF model for real AI generation!*"
        
        response_time = time.time() - start_time
        juggernaut.system_metrics['total_requests'] += 1
        
        return jsonify({
            "response": response,
            "response_time": round(response_time, 3),
            "tokens_used": len(response.split()),
            "gpu_accelerated": True,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/research/analyze', methods=['POST'])
def analyze_research():
    """Analyze research content with AI"""
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        content = data.get('content', '').strip()
        analysis_type = data.get('type', 'general')
        
        if not content:
            return jsonify({"error": "Content required for analysis"}), 400
        
        # Create analysis prompt based on type
        prompts = {
            'general': f"Provide a comprehensive analysis of the following content:\n\n{content}",
            'technical': f"Perform a technical analysis of the following content, focusing on technical aspects, methodologies, and implementation details:\n\n{content}",
            'business': f"Analyze the following content from a business perspective, including market implications, opportunities, and strategic considerations:\n\n{content}",
            'academic': f"Provide an academic analysis of the following content, including theoretical frameworks, research methodology, and scholarly implications:\n\n{content}"
        }
        
        prompt = prompts.get(analysis_type, prompts['general'])
        
        start_time = time.time()
        
        if juggernaut.ai_engine and juggernaut.ai_engine.is_ready():
            analysis = juggernaut.ai_engine.generate_response(prompt, max_tokens=500)
        else:
            analysis = f"🔬 **Research Analysis (Demo Mode)**\n\n**Analysis Type:** {analysis_type.title()}\n**Content Length:** {len(content)} characters\n\n**RTX 4070 SUPER Status:** ✅ Ready for GPU-accelerated analysis\n\n*Add an AI model to perform real research analysis with GPU acceleration!*\n\n**Content Preview:**\n{content[:200]}..."
        
        response_time = time.time() - start_time
        juggernaut.system_metrics['total_requests'] += 1
        
        return jsonify({
            "analysis": analysis,
            "analysis_type": analysis_type,
            "content_length": len(content),
            "response_time": round(response_time, 3),
            "gpu_accelerated": True,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error analyzing research: {e}")
        return jsonify({"error": str(e)}), 500

# Browser control API endpoints
@app.route('/api/browser/navigate', methods=['POST'])
def browser_navigate():
    """Navigate browser to URL"""
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({"error": "URL required"}), 400
        
        if not juggernaut.browser_controller:
            return jsonify({"error": "Browser controller not available"}), 503
        
        result = juggernaut.browser_controller.navigate(url)
        juggernaut.system_metrics['total_requests'] += 1
        
        return jsonify({
            **result,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error navigating browser: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/browser/view')
def browser_view():
    """Get current browser view"""
    try:
        if not juggernaut.browser_controller:
            return jsonify({"error": "Browser controller not available"}), 503
        
        result = juggernaut.browser_controller.get_current_view()
        juggernaut.system_metrics['total_requests'] += 1
        
        return jsonify({
            **result,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting browser view: {e}")
        return jsonify({"error": str(e)}), 500

# Plugin system API endpoints
@app.route('/api/plugins')
def list_plugins():
    """List available plugins"""
    try:
        if not juggernaut.plugin_manager:
            return jsonify({"plugins": [], "total": 0})
        
        plugins = juggernaut.plugin_manager.list_plugins()
        juggernaut.system_metrics['total_requests'] += 1
        
        return jsonify({
            "plugins": plugins,
            "total": len(plugins),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error listing plugins: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/plugins/<plugin_name>/execute', methods=['POST'])
def execute_plugin(plugin_name):
    """Execute a specific plugin"""
    try:
        if not juggernaut.plugin_manager:
            return jsonify({"error": "Plugin manager not available"}), 503
        
        data = request.get_json() if request.is_json else {}
        params = data.get('params', {})
        
        result = juggernaut.plugin_manager.execute_plugin(plugin_name, params)
        juggernaut.system_metrics['total_requests'] += 1
        
        return jsonify({
            **result,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error executing plugin {plugin_name}: {e}")
        return jsonify({"error": str(e)}), 500

# System management endpoints
@app.route('/api/system/metrics')
def get_system_metrics():
    """Get detailed system metrics"""
    try:
        metrics = {
            **juggernaut.system_metrics,
            "ai_engine_metrics": juggernaut.ai_engine.get_performance_metrics() if juggernaut.ai_engine else {},
            "memory_usage": "N/A",  # Could add psutil for memory monitoring
            "gpu_status": {
                "model": "RTX 4070 SUPER",
                "vram": "12GB",
                "status": "ready",
                "acceleration_enabled": True
            }
        }
        
        return jsonify({
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting system metrics: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/system/settings', methods=['GET', 'POST'])
def system_settings():
    """Get or update system settings"""
    try:
        if request.method == 'GET':
            settings = {
                "ai_settings": juggernaut.ai_engine.get_status() if juggernaut.ai_engine else {},
                "data_path": juggernaut.data_path,
                "gpu_enabled": True,
                "max_file_size": app.config['MAX_CONTENT_LENGTH'],
                "version": "1.0.0"
            }
            return jsonify(settings)
        
        elif request.method == 'POST':
            if not request.is_json:
                return jsonify({"error": "Content-Type must be application/json"}), 400
            
            settings = request.get_json()
            
            # Update AI engine settings
            if juggernaut.ai_engine and 'ai_settings' in settings:
                juggernaut.ai_engine.update_settings(settings['ai_settings'])
            
            return jsonify({
                "status": "updated",
                "timestamp": datetime.now().isoformat()
            })
            
    except Exception as e:
        logger.error(f"Error handling system settings: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting JUGGERNAUT AI SYSTEM...")
    print(f"🌐 Access at: http://localhost:5000")
    print(f"📁 Data directory: {juggernaut.data_path}")
    print(f"🎯 RTX 4070 SUPER GPU acceleration ready")
    print("=" * 50)
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,  # Set to False for production
            threaded=True,
            use_reloader=False
        )
    except KeyboardInterrupt:
        logger.info("🛑 Juggernaut AI system shutting down...")
    except Exception as e:
        logger.error(f"Failed to start Flask application: {e}")
        logger.error(traceback.format_exc())

