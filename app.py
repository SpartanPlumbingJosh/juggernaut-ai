"""
ULTIMATE JUGGERNAUT UNIFIED INTERFACE
Main application entry point - modular and maintainable
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import threading
from datetime import datetime
import uuid

# Import modular components
from core.ai_engine import AIEngine
from core.browser_controller import BrowserController
from core.plugin_manager import PluginManager
from core.file_manager import FileManager
from core.chat_manager import ChatManager

app = Flask(__name__)

class JuggernautUnified:
    def __init__(self):
        """Initialize the unified Juggernaut system"""
        self.data_path = "D:\\JUGGERNAUT_DATA"
        self.setup_directories()
        
        # Initialize modular components
        self.ai_engine = AIEngine(self.data_path)
        self.browser_controller = BrowserController(self.data_path)
        self.plugin_manager = PluginManager(self.data_path)
        self.file_manager = FileManager(self.data_path)
        self.chat_manager = ChatManager(self.data_path)
        
        # System state
        self.status = "initializing"
        self.active_chats = {}
        self.current_chat_id = None
        
        print("🚀 JUGGERNAUT UNIFIED INTERFACE READY")
    
    def setup_directories(self):
        """Setup all required directories on D: drive"""
        directories = [
            self.data_path,
            f"{self.data_path}\\chats",
            f"{self.data_path}\\images",
            f"{self.data_path}\\files",
            f"{self.data_path}\\screenshots",
            f"{self.data_path}\\research",
            f"{self.data_path}\\logs",
            f"{self.data_path}\\plugins"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        print(f"✅ Data directories ready: {self.data_path}")

# Global instance
juggernaut = JuggernautUnified()

@app.route('/')
def index():
    """Main interface"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get system status"""
    return jsonify({
        "status": juggernaut.status,
        "ai_ready": juggernaut.ai_engine.is_ready(),
        "browser_ready": juggernaut.browser_controller.is_ready(),
        "active_chats": len(juggernaut.active_chats),
        "plugins_loaded": juggernaut.plugin_manager.get_plugin_count()
    })

@app.route('/api/chat/new', methods=['POST'])
def new_chat():
    """Create new chat"""
    chat_id = str(uuid.uuid4())[:8]
    chat_data = juggernaut.chat_manager.create_chat(chat_id)
    juggernaut.active_chats[chat_id] = chat_data
    juggernaut.current_chat_id = chat_id
    
    return jsonify({
        "success": True,
        "chat_id": chat_id,
        "chat_data": chat_data
    })

@app.route('/api/chat/<chat_id>/message', methods=['POST'])
def send_message(chat_id):
    """Send message to AI"""
    data = request.get_json()
    message = data.get('message', '')
    
    # Process with AI engine
    response = juggernaut.ai_engine.process_message(message, chat_id)
    
    # Save to chat
    juggernaut.chat_manager.add_message(chat_id, "user", message)
    juggernaut.chat_manager.add_message(chat_id, "assistant", response)
    
    return jsonify({
        "success": True,
        "response": response,
        "chat_id": chat_id
    })

@app.route('/api/chat/<chat_id>/edit', methods=['POST'])
def edit_message(chat_id):
    """Edit a message in chat"""
    data = request.get_json()
    message_id = data.get('message_id')
    new_content = data.get('content')
    
    success = juggernaut.chat_manager.edit_message(chat_id, message_id, new_content)
    
    return jsonify({"success": success})

@app.route('/api/browser/view')
def browser_view():
    """Get current browser view"""
    return jsonify(juggernaut.browser_controller.get_current_view())

@app.route('/api/browser/navigate', methods=['POST'])
def browser_navigate():
    """Navigate browser"""
    data = request.get_json()
    url = data.get('url')
    mode = data.get('mode', 'ai')  # 'ai' or 'user'
    
    result = juggernaut.browser_controller.navigate(url, mode)
    return jsonify(result)

@app.route('/api/files/upload', methods=['POST'])
def upload_file():
    """Handle file uploads for research"""
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file provided"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No file selected"})
    
    result = juggernaut.file_manager.save_uploaded_file(file)
    return jsonify(result)

@app.route('/api/image/generate', methods=['POST'])
def generate_image():
    """Generate image inline"""
    data = request.get_json()
    prompt = data.get('prompt')
    chat_id = data.get('chat_id')
    
    result = juggernaut.plugin_manager.generate_image(prompt, chat_id)
    return jsonify(result)

@app.route('/api/research/analyze', methods=['POST'])
def analyze_research():
    """Analyze uploaded files for research"""
    data = request.get_json()
    file_path = data.get('file_path')
    
    result = juggernaut.ai_engine.analyze_file(file_path)
    return jsonify(result)

@app.route('/api/image/<image_id>')
def serve_image(image_id):
    """Serve generated images"""
    image_data = juggernaut.plugin_manager.get_image(image_id)
    if image_data and os.path.exists(image_data['filepath']):
        return send_file(image_data['filepath'])
    return jsonify({"error": "Image not found"}), 404

@app.route('/api/chats')
def get_all_chats():
    """Get all chat summaries"""
    chats = juggernaut.chat_manager.get_all_chats()
    return jsonify(chats)

@app.route('/api/chat/<chat_id>')
def get_chat(chat_id):
    """Get specific chat data"""
    chat_data = juggernaut.chat_manager.get_chat(chat_id)
    if chat_data:
        return jsonify(chat_data)
    return jsonify({"error": "Chat not found"}), 404

@app.route('/api/browser/manus', methods=['POST'])
def read_manus():
    """Read Manus chats"""
    result = juggernaut.browser_controller.read_manus_chats()
    return jsonify(result)

@app.route('/api/files')
def list_files():
    """List uploaded files"""
    files = juggernaut.file_manager.list_files()
    return jsonify(files)

@app.route('/api/images')
def list_images():
    """List generated images"""
    images = juggernaut.plugin_manager.list_images()
    return jsonify(images)

if __name__ == '__main__':
    print("🚀 Starting JUGGERNAUT UNIFIED INTERFACE...")
    print("🌐 Open browser to: http://localhost:5000")
    print("📁 All data saves to: D:\\JUGGERNAUT_DATA")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

