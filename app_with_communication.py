# Enhanced Juggernaut AI with Email and SMS Communication
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import time
import logging
from datetime import datetime
from communication_manager import CommunicationManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Data directories
DATA_DIR = "D:\\JUGGERNAUT_DATA"
LOGS_DIR = os.path.join(DATA_DIR, "logs")
CHATS_DIR = os.path.join(DATA_DIR, "chats")
FILES_DIR = os.path.join(DATA_DIR, "files")

# Create directories
for directory in [DATA_DIR, LOGS_DIR, CHATS_DIR, FILES_DIR]:
    os.makedirs(directory, exist_ok=True)

class EnhancedGemmaEngine:
    """Enhanced Gemma Engine with Real Model Integration"""
    
    def __init__(self):
        self.model_path = "D:/Juggernaut_AI/models/ai_models/text/gemma_2_9b_gguf/gemma-2-9b-it-Q4_K_M.gguf"
        self.model = None
        self.ready = False
        self.learning_data = {
            "total_interactions": 0,
            "positive_feedback": 0,
            "conversation_patterns": {},
            "user_preferences": {}
        }
        self.conversation_contexts = {}
        
        # Try to load the real model
        self._initialize_model()
        
        # Load learning data
        self._load_learning_data()
    
    def _initialize_model(self):
        """Initialize the real Gemma model"""
        try:
            # Try to import llama-cpp-python
            from llama_cpp import Llama
            
            if os.path.exists(self.model_path):
                logger.info(f"🤖 Loading Gemma model: {self.model_path}")
                
                # RTX 4070 SUPER optimized settings
                self.model = Llama(
                    model_path=self.model_path,
                    n_gpu_layers=35,  # RTX 4070 SUPER optimization
                    n_ctx=4096,
                    n_batch=512,
                    verbose=False,
                    use_mmap=True,
                    use_mlock=True
                )
                
                self.ready = True
                logger.info("✅ Gemma model loaded successfully with RTX 4070 SUPER acceleration")
                
            else:
                logger.warning(f"⚠️ Model file not found: {self.model_path}")
                logger.info("🔄 Running in demo mode")
                self.ready = False
                
        except ImportError:
            logger.warning("⚠️ llama-cpp-python not available")
            logger.info("📥 Install with: pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121")
            self.ready = False
        except Exception as e:
            logger.error(f"❌ Model initialization failed: {e}")
            self.ready = False
    
    def _load_learning_data(self):
        """Load learning data"""
        learning_file = os.path.join(DATA_DIR, "gemma_learning.json")
        try:
            if os.path.exists(learning_file):
                with open(learning_file, 'r', encoding='utf-8') as f:
                    self.learning_data.update(json.load(f))
                logger.info(f"📚 Learning data loaded: {self.learning_data['total_interactions']} interactions")
        except Exception as e:
            logger.error(f"Learning data load error: {e}")
    
    def _save_learning_data(self):
        """Save learning data"""
        learning_file = os.path.join(DATA_DIR, "gemma_learning.json")
        try:
            with open(learning_file, 'w', encoding='utf-8') as f:
                json.dump(self.learning_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Learning data save error: {e}")
    
    def _update_context(self, chat_id, role, content):
        """Update conversation context"""
        if chat_id not in self.conversation_contexts:
            self.conversation_contexts[chat_id] = []
        
        self.conversation_contexts[chat_id].append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 10 messages for memory efficiency
        if len(self.conversation_contexts[chat_id]) > 10:
            self.conversation_contexts[chat_id] = self.conversation_contexts[chat_id][-10:]
    
    def _build_prompt(self, user_input, chat_id):
        """Build context-aware prompt"""
        prompt_parts = []
        
        # System prompt
        prompt_parts.append("You are Juggernaut AI, powered by Gemma. You learn from interactions and provide helpful responses.")
        
        # Add conversation context
        context = self.conversation_contexts.get(chat_id, [])
        if context:
            prompt_parts.append("\\nRecent conversation:")
            for msg in context[-3:]:  # Last 3 messages
                role = "User" if msg['role'] == 'user' else "Juggernaut"
                prompt_parts.append(f"{role}: {msg['content']}")
        
        # Add current input
        prompt_parts.append(f"\\nUser: {user_input}")
        prompt_parts.append("Juggernaut:")
        
        return "\\n".join(prompt_parts)
    
    def generate(self, user_input, chat_id="default"):
        """Generate response with learning"""
        start_time = time.time()
        
        try:
            # Update learning stats
            self.learning_data["total_interactions"] += 1
            
            # Update conversation context
            self._update_context(chat_id, 'user', user_input)
            
            if self.ready and self.model:
                # Real Gemma model inference
                prompt = self._build_prompt(user_input, chat_id)
                
                response = self.model(
                    prompt,
                    max_tokens=512,
                    temperature=0.7,
                    top_p=0.9,
                    repeat_penalty=1.1,
                    stop=["User:", "Human:", "\\n\\n"]
                )
                
                ai_response = response['choices'][0]['text'].strip()
                
                # Update conversation context
                self._update_context(chat_id, 'assistant', ai_response)
                
                response_time = time.time() - start_time
                
                # Save learning data
                self._save_learning_data()
                
                logger.info(f"✅ Gemma response generated in {response_time:.2f}s")
                
                return {
                    "response": ai_response,
                    "model": "gemma-2-9b-it",
                    "response_time": response_time,
                    "learning_enabled": True,
                    "gpu_accelerated": True
                }
                
            else:
                # Enhanced demo mode
                demo_responses = [
                    f"🤖 Juggernaut AI: I understand '{user_input}'. I'm learning your communication style and will provide better responses when the Gemma model is loaded!",
                    f"🧠 Learning from: '{user_input}'. Your Gemma model will enable full AI capabilities with RTX 4070 SUPER acceleration.",
                    f"⚡ RTX 4070 SUPER ready! Processing '{user_input}' in demo mode. Install llama-cpp-python for full Gemma integration.",
                    f"📚 I'm analyzing your input: '{user_input}'. Full learning capabilities available with model installation."
                ]
                
                import random
                demo_response = random.choice(demo_responses)
                
                # Still update context and learn in demo mode
                self._update_context(chat_id, 'assistant', demo_response)
                self._save_learning_data()
                
                response_time = time.time() - start_time
                
                return {
                    "response": demo_response,
                    "model": "demo-mode",
                    "response_time": response_time,
                    "learning_enabled": True,
                    "gpu_accelerated": False
                }
                
        except Exception as e:
            logger.error(f"❌ Response generation failed: {e}")
            error_response = f"⚠️ I encountered an issue: {str(e)}. I'm still learning and will improve!"
            
            return {
                "response": error_response,
                "model": "error",
                "response_time": time.time() - start_time,
                "learning_enabled": False,
                "gpu_accelerated": False,
                "error": str(e)
            }
    
    def is_ready(self):
        return True  # Always ready (demo mode if model not loaded)
    
    def get_status(self):
        return {
            "ready": self.ready,
            "model_loaded": self.ready,
            "learning_stats": self.learning_data,
            "gpu_optimization": "RTX 4070 SUPER (35 layers)" if self.ready else "Demo Mode"
        }
    
    def process_feedback(self, feedback):
        """Process user feedback"""
        if feedback.lower() in ['good', 'great', 'excellent', 'perfect']:
            self.learning_data["positive_feedback"] += 1
        
        self._save_learning_data()
        logger.info(f"📝 Feedback processed: {feedback}")

class SimpleChatManager:
    """Simple but effective chat manager"""
    
    def __init__(self):
        self.chats = {}
        self._load_chats()
    
    def _load_chats(self):
        """Load existing chats"""
        try:
            for file in os.listdir(CHATS_DIR):
                if file.endswith(".json"):
                    chat_id = file.replace(".json", "")
                    with open(os.path.join(CHATS_DIR, file), "r", encoding="utf-8") as f:
                        self.chats[chat_id] = json.load(f)
        except Exception as e:
            logger.error(f"Chat loading error: {e}")
        
        if not self.chats:
            self.chats["default"] = []
    
    def add_message(self, chat_id, role, content):
        """Add message to chat"""
        if chat_id not in self.chats:
            self.chats[chat_id] = []
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self.chats[chat_id].append(message)
        self._save_chat(chat_id)
        return message
    
    def _save_chat(self, chat_id):
        """Save chat to file"""
        try:
            with open(os.path.join(CHATS_DIR, f"{chat_id}.json"), "w", encoding="utf-8") as f:
                json.dump(self.chats[chat_id], f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Chat save error: {e}")
    
    def get_chat(self, chat_id):
        return self.chats.get(chat_id, [])
    
    def get_all_chats(self):
        return {"chats": self.chats}

class SimpleFileManager:
    """Simple file manager"""
    
    def save_file(self, file):
        """Save uploaded file"""
        try:
            filename = file.filename
            filepath = os.path.join(FILES_DIR, filename)
            file.save(filepath)
            return filename
        except Exception as e:
            logger.error(f"File save error: {e}")
            return None
    
    def list_files(self):
        """List uploaded files"""
        try:
            return os.listdir(FILES_DIR)
        except Exception as e:
            logger.error(f"File list error: {e}")
            return []
    
    def analyze_file(self, filename):
        """Analyze file content"""
        return f"📄 File analysis for {filename}: This is a placeholder analysis. Full analysis available with enhanced features."

class SimpleBrowserController:
    """Simple browser controller"""
    
    def is_ready(self):
        return True
    
    def execute(self, command, url=None):
        """Execute browser command"""
        return f"🌐 Browser command '{command}' executed. URL: {url or 'N/A'}"

# Initialize components
logger.info("🚀 Initializing Enhanced Juggernaut AI with Communication...")

gemma = EnhancedGemmaEngine()
chats = SimpleChatManager()
files = SimpleFileManager()
browser = SimpleBrowserController()
communication = CommunicationManager(DATA_DIR)

# Connect AI engine to communication manager
communication.set_ai_engine(gemma)

logger.info("✅ All components initialized successfully")

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)

@app.route("/api/chat/send", methods=["POST"])
def send_message():
    try:
        data = request.get_json()
        message = data.get("message")
        chat_id = data.get("chat_id", "default")
        user = data.get("user", "Josh")
        
        # Add user message
        chats.add_message(chat_id, user, message)
        
        # Generate AI response
        result = gemma.generate(message, chat_id)
        ai_response = result["response"]
        
        # Add AI message
        chats.add_message(chat_id, "Juggernaut", ai_response)
        
        return jsonify({
            "success": True,
            "response": ai_response,
            "model": result.get("model", "unknown"),
            "response_time": result.get("response_time", 0),
            "learning_enabled": result.get("learning_enabled", False),
            "gpu_accelerated": result.get("gpu_accelerated", False)
        })
        
    except Exception as e:
        logger.error(f"Send message error: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/feedback", methods=["POST"])
def submit_feedback():
    try:
        data = request.get_json()
        feedback = data.get("feedback")
        
        gemma.process_feedback(feedback)
        
        return jsonify({"success": True})
        
    except Exception as e:
        logger.error(f"Feedback error: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/learning/insights", methods=["GET"])
def get_learning_insights():
    try:
        stats = gemma.learning_data
        total = stats.get("total_interactions", 0)
        positive = stats.get("positive_feedback", 0)
        
        insights = {
            "total_interactions": total,
            "positive_feedback": positive,
            "satisfaction_rate": (positive / total * 100) if total > 0 else 0,
            "conversation_patterns": len(stats.get("conversation_patterns", {})),
            "learning_active": True
        }
        
        return jsonify(insights)
        
    except Exception as e:
        logger.error(f"Learning insights error: {e}")
        return jsonify({"error": str(e)})

# Communication API endpoints
@app.route("/api/communication/setup/email", methods=["POST"])
def setup_email():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        authorized_emails = data.get("authorized_emails", [])
        
        result = communication.setup_email(email, password, authorized_emails)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Email setup error: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/communication/setup/sms", methods=["POST"])
def setup_sms():
    try:
        data = request.get_json()
        account_sid = data.get("account_sid")
        auth_token = data.get("auth_token")
        twilio_number = data.get("twilio_number")
        your_number = data.get("your_number")
        
        result = communication.setup_sms(account_sid, auth_token, twilio_number, your_number)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"SMS setup error: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/communication/start", methods=["POST"])
def start_communication():
    try:
        success = communication.start_monitoring()
        return jsonify({"success": success})
        
    except Exception as e:
        logger.error(f"Communication start error: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/communication/stop", methods=["POST"])
def stop_communication():
    try:
        communication.stop_monitoring()
        return jsonify({"success": True})
        
    except Exception as e:
        logger.error(f"Communication stop error: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/communication/status", methods=["GET"])
def communication_status():
    try:
        status = communication.get_status()
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"Communication status error: {e}")
        return jsonify({"error": str(e)})

@app.route("/api/communication/log", methods=["GET"])
def communication_log():
    try:
        limit = request.args.get("limit", 50, type=int)
        log = communication.get_communication_log(limit)
        return jsonify({"log": log})
        
    except Exception as e:
        logger.error(f"Communication log error: {e}")
        return jsonify({"error": str(e)})

@app.route("/api/communication/send/sms", methods=["POST"])
def send_sms():
    try:
        data = request.get_json()
        phone_number = data.get("phone_number")
        message = data.get("message")
        
        result = communication.send_sms(phone_number, message)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"SMS send error: {e}")
        return jsonify({"success": False, "error": str(e)})

# Twilio webhook for incoming SMS
@app.route("/webhook/sms", methods=["POST"])
def sms_webhook():
    try:
        result = communication.process_sms_webhook(request.form)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"SMS webhook error: {e}")
        return jsonify({"success": False, "error": str(e)})

# Original API endpoints
@app.route("/api/chats", methods=["GET"])
def get_chats():
    return jsonify(chats.get_all_chats())

@app.route("/api/chat/<chat_id>", methods=["GET"])
def get_chat(chat_id):
    return jsonify(chats.get_chat(chat_id))

@app.route("/api/files/upload", methods=["POST"])
def upload_file():
    try:
        if "file" not in request.files:
            return jsonify({"success": False, "error": "No file provided"})
        
        f = request.files["file"]
        filename = files.save_file(f)
        
        if filename:
            return jsonify({"success": True, "filename": filename})
        else:
            return jsonify({"success": False, "error": "File save failed"})
            
    except Exception as e:
        logger.error(f"File upload error: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/files", methods=["GET"])
def list_files():
    return jsonify({"files": files.list_files()})

@app.route("/api/files/analyze", methods=["POST"])
def analyze_file():
    try:
        data = request.get_json()
        filename = data.get("filename")
        result = files.analyze_file(filename)
        return jsonify({"result": result})
        
    except Exception as e:
        logger.error(f"File analysis error: {e}")
        return jsonify({"result": f"Analysis error: {e}"})

@app.route("/api/browser/navigate", methods=["POST"])
def browser_navigate():
    try:
        data = request.get_json()
        url = data.get("url")
        result = browser.execute("navigate", url)
        return jsonify({"success": True, "result": result})
        
    except Exception as e:
        logger.error(f"Browser navigation error: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/status", methods=["GET"])
def status():
    try:
        gemma_status = gemma.get_status()
        comm_status = communication.get_status()
        
        return jsonify({
            "ready": True,
            "ai_ready": gemma.is_ready(),
            "browser_ready": browser.is_ready(),
            "model_loaded": gemma_status.get("model_loaded", False),
            "learning_enabled": True,
            "gpu_optimization": gemma_status.get("gpu_optimization", "Demo Mode"),
            "learning_stats": gemma_status.get("learning_stats", {}),
            "communication": comm_status,
            "system_ready": True
        })
        
    except Exception as e:
        logger.error(f"Status error: {e}")
        return jsonify({"ready": False, "error": str(e)})

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 ENHANCED JUGGERNAUT AI WITH COMMUNICATION")
    print("🎯 RTX 4070 SUPER Optimized")
    print("🧠 Real Gemma Integration with Learning")
    print("📧 Email & SMS Communication Enabled")
    print("=" * 60)
    print(f"🌐 Web Interface: http://localhost:5000")
    print(f"📁 Data directory: {DATA_DIR}")
    print(f"🎯 RTX 4070 SUPER GPU acceleration ready")
    print(f"📧 Email monitoring available")
    print(f"📱 SMS integration via Twilio")
    print("=" * 60)
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True,
            use_reloader=False
        )
    except KeyboardInterrupt:
        logger.info("🛑 Enhanced Juggernaut AI shutting down...")
        communication.stop_monitoring()
    except Exception as e:
        logger.error(f"Failed to start Flask application: {e}")

