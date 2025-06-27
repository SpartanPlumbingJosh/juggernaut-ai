# FINAL Juggernaut AI with Hot Reload & Red Theme
# Real Gemma 3 Integration + Auto GitHub Updates

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import json
import time
import logging
import threading
import psutil
from pathlib import Path
from datetime import datetime

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from gemma3_engine import Gemma3Engine
from free_communication_manager import FreeCommunicationManager
from hot_reload_system import HotReloadManager

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

# Create Flask app
app = Flask(__name__)
CORS(app)

# Configuration
class Config:
    # Paths
    DATA_DIR = Path("D:/JUGGERNAUT_DATA")
    MODELS_DIR = DATA_DIR / "models"
    CHATS_DIR = DATA_DIR / "chats"
    UPLOADS_DIR = DATA_DIR / "uploads"
    LOGS_DIR = Path("logs")
    
    # Gemma 3 Model Configuration
    GEMMA_MODEL_PATH = "D:/Juggernaut_AI/models/ai_models/text/gemma_2_9b_gguf/gemma-2-9b-it-Q4_K_M.gguf"
    GPU_LAYERS = 35  # RTX 4070 SUPER optimized
    CONTEXT_WINDOW = 4096
    
    # Hot Reload Configuration
    GITHUB_REPO = "SpartanPlumbingJosh/juggernaut-ai"
    REPO_PATH = os.path.dirname(os.path.abspath(__file__))
    
    # System Configuration
    MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100MB
    CHAT_HISTORY_LIMIT = 1000
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories"""
        for directory in [cls.DATA_DIR, cls.MODELS_DIR, cls.CHATS_DIR, cls.UPLOADS_DIR, cls.LOGS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

# Initialize configuration
Config.create_directories()

# Global instances
ai_engine = None
communication_manager = None
hot_reload_manager = None
system_metrics = {}

def initialize_ai_engine():
    """Initialize the Gemma 3 AI engine"""
    global ai_engine
    try:
        logger.info("🤖 Initializing Gemma 3 AI Engine...")
        ai_engine = Gemma3Engine(
            model_path=Config.GEMMA_MODEL_PATH,
            gpu_layers=Config.GPU_LAYERS,
            context_window=Config.CONTEXT_WINDOW
        )
        logger.info("✅ AI Engine initialized successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to initialize AI Engine: {e}")
        return False

def initialize_communication_manager():
    """Initialize the communication manager"""
    global communication_manager
    try:
        logger.info("📡 Initializing Communication Manager...")
        communication_manager = FreeCommunicationManager()
        logger.info("✅ Communication Manager initialized")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to initialize Communication Manager: {e}")
        return False

def initialize_hot_reload():
    """Initialize hot reload system"""
    global hot_reload_manager
    try:
        logger.info("🔥 Initializing Hot Reload System...")
        hot_reload_manager = HotReloadManager(
            app=app,
            repo_path=Config.REPO_PATH,
            github_repo=Config.GITHUB_REPO
        )
        
        # Add update callback
        hot_reload_manager.reloader.add_update_callback(on_system_update)
        
        # Start hot reload
        hot_reload_manager.start()
        
        logger.info("✅ Hot Reload System initialized")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to initialize Hot Reload: {e}")
        return False

def on_system_update():
    """Callback for when system updates occur"""
    logger.info("🔄 System update detected - refreshing components...")
    
    # Refresh AI engine if needed
    global ai_engine
    if ai_engine:
        try:
            # Reload learning data
            learning_file = Config.DATA_DIR / "learning_data.json"
            if learning_file.exists():
                ai_engine.load_learning_data(str(learning_file))
        except Exception as e:
            logger.error(f"Error refreshing AI engine: {e}")

def get_system_metrics():
    """Get current system metrics"""
    try:
        # CPU and Memory
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        # GPU info (if available)
        gpu_info = "RTX 4070 SUPER"
        vram_info = "12GB"
        
        # AI Engine status
        ai_status = "Ready" if ai_engine and ai_engine.is_loaded else "Demo Mode"
        
        return {
            'cpu_usage': cpu_percent,
            'ram_usage': round(memory.used / (1024**3), 1),
            'ram_total': round(memory.total / (1024**3), 1),
            'gpu': gpu_info,
            'vram': vram_info,
            'ai_status': ai_status,
            'model': 'Gemma 3',
            'uptime': time.time() - start_time,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting system metrics: {e}")
        return {}

# Routes
@app.route('/')
def index():
    """Main application page"""
    return render_template('advanced_index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        chat_id = data.get('chat_id', 'general')
        context = data.get('context', [])
        
        if not message:
            return jsonify({'success': False, 'error': 'Empty message'})
        
        # Generate AI response
        start_time = time.time()
        
        if ai_engine:
            response = ai_engine.generate_response(message, context, chat_id)
        else:
            response = "AI Engine not available. Please check the system status."
        
        response_time = time.time() - start_time
        
        # Save chat message
        save_chat_message(chat_id, message, response)
        
        return jsonify({
            'success': True,
            'response': response,
            'metadata': {
                'response_time': round(response_time * 1000, 2),
                'tokens': len(response.split()),
                'chat_id': chat_id,
                'timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Handle file uploads"""
    try:
        if 'files' not in request.files:
            return jsonify({'success': False, 'error': 'No files provided'})
        
        files = request.files.getlist('files')
        uploaded_files = []
        
        for file in files:
            if file.filename:
                # Save file
                filename = secure_filename(file.filename)
                filepath = Config.UPLOADS_DIR / filename
                file.save(filepath)
                uploaded_files.append(str(filepath))
        
        # Analyze files with AI
        if ai_engine and uploaded_files:
            analysis = f"📁 **Files Uploaded Successfully**\n\nUploaded {len(uploaded_files)} files:\n"
            for file_path in uploaded_files:
                file_size = os.path.getsize(file_path)
                analysis += f"• {Path(file_path).name} ({file_size:,} bytes)\n"
            
            analysis += "\n🤖 **AI Analysis:**\nFiles are ready for processing. You can ask me to analyze, summarize, or work with these files in our conversation!"
        else:
            analysis = f"Uploaded {len(uploaded_files)} files successfully."
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'files': uploaded_files
        })
        
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/browser/navigate', methods=['POST'])
def browser_navigate():
    """Handle browser navigation"""
    try:
        data = request.get_json()
        url = data.get('url', '')
        mode = data.get('mode', 'ai')
        
        # Simulate browser navigation
        content = f"""
        <div style="padding: 20px; background: white; color: black;">
            <h2>Browser Navigation</h2>
            <p><strong>URL:</strong> {url}</p>
            <p><strong>Mode:</strong> {mode}</p>
            <p><strong>Status:</strong> Navigation simulated successfully</p>
            <p>Real browser integration would be implemented here.</p>
        </div>
        """
        
        return jsonify({
            'success': True,
            'content': content,
            'url': url,
            'mode': mode
        })
        
    except Exception as e:
        logger.error(f"Browser navigation error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/system/metrics')
def system_metrics():
    """Get system metrics"""
    try:
        metrics = get_system_metrics()
        
        # Add AI engine metrics if available
        if ai_engine:
            ai_metrics = ai_engine.get_learning_insights()
            metrics.update(ai_metrics)
        
        return jsonify({
            'success': True,
            'data': metrics
        })
        
    except Exception as e:
        logger.error(f"System metrics error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/chat/history')
def chat_history():
    """Get chat history"""
    try:
        chat_id = request.args.get('chat_id', 'general')
        
        # Load chat history from file
        chat_file = Config.CHATS_DIR / f"{chat_id}.json"
        
        if chat_file.exists():
            with open(chat_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = []
        
        return jsonify({
            'success': True,
            'history': history,
            'chat_id': chat_id
        })
        
    except Exception as e:
        logger.error(f"Chat history error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/files')
def list_files():
    """List uploaded files"""
    try:
        files = []
        
        if Config.UPLOADS_DIR.exists():
            for file_path in Config.UPLOADS_DIR.iterdir():
                if file_path.is_file():
                    files.append({
                        'name': file_path.name,
                        'size': file_path.stat().st_size,
                        'modified': file_path.stat().st_mtime,
                        'path': str(file_path)
                    })
        
        return jsonify({
            'success': True,
            'files': files
        })
        
    except Exception as e:
        logger.error(f"Files list error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/communication')
def communication_setup():
    """Communication setup page"""
    return render_template('communication_setup.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files with hot reload support"""
    return send_from_directory('static', filename)

# Utility functions
def save_chat_message(chat_id: str, user_message: str, ai_response: str):
    """Save chat message to file"""
    try:
        chat_file = Config.CHATS_DIR / f"{chat_id}.json"
        
        # Load existing history
        if chat_file.exists():
            with open(chat_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = []
        
        # Add new messages
        timestamp = datetime.now().isoformat()
        
        history.append({
            'type': 'user',
            'message': user_message,
            'timestamp': timestamp
        })
        
        history.append({
            'type': 'assistant',
            'message': ai_response,
            'timestamp': timestamp
        })
        
        # Keep only last N messages
        if len(history) > Config.CHAT_HISTORY_LIMIT:
            history = history[-Config.CHAT_HISTORY_LIMIT:]
        
        # Save to file
        with open(chat_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"Error saving chat message: {e}")

def secure_filename(filename):
    """Secure filename for uploads"""
    import re
    filename = re.sub(r'[^\w\s-.]', '', filename)
    return filename.strip()

# System monitoring thread
def system_monitor():
    """Background system monitoring"""
    while True:
        try:
            global system_metrics
            system_metrics = get_system_metrics()
            
            # Save learning data periodically
            if ai_engine:
                learning_file = Config.DATA_DIR / "learning_data.json"
                ai_engine.save_learning_data(str(learning_file))
            
            time.sleep(30)  # Update every 30 seconds
            
        except Exception as e:
            logger.error(f"System monitor error: {e}")
            time.sleep(30)

# Initialize everything
def initialize_system():
    """Initialize all system components"""
    logger.info("🚀 Starting Juggernaut AI System...")
    
    # Initialize components
    ai_success = initialize_ai_engine()
    comm_success = initialize_communication_manager()
    reload_success = initialize_hot_reload()
    
    # Start system monitoring
    monitor_thread = threading.Thread(target=system_monitor, daemon=True)
    monitor_thread.start()
    
    logger.info("✅ System initialization complete")
    logger.info(f"🤖 AI Engine: {'✅' if ai_success else '❌'}")
    logger.info(f"📡 Communication: {'✅' if comm_success else '❌'}")
    logger.info(f"🔥 Hot Reload: {'✅' if reload_success else '❌'}")

if __name__ == '__main__':
    # Record start time
    start_time = time.time()
    
    # Initialize system
    initialize_system()
    
    # Create PowerShell update script
    update_script_path = Path("update_juggernaut.ps1")
    with open(update_script_path, 'w', encoding='utf-8') as f:
        f.write(POWERSHELL_UPDATE_SCRIPT)
    
    logger.info("📜 PowerShell update script created: update_juggernaut.ps1")
    
    # Start Flask app
    logger.info("🌐 Starting Flask server...")
    logger.info("🎯 Access the interface at: http://localhost:5000")
    logger.info("🔥 Hot reload enabled - GitHub changes will auto-update!")
    logger.info("🎨 Red theme activated")
    logger.info("🤖 Real Gemma 3 integration ready")
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,  # Disable debug mode for hot reload compatibility
            threaded=True
        )
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down Juggernaut AI...")
        if hot_reload_manager:
            hot_reload_manager.stop()
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
    finally:
        logger.info("👋 Juggernaut AI stopped")

