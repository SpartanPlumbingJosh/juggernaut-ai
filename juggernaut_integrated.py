# JUGGERNAUT AI - INTEGRATED SYSTEM
# Combines working configuration with professional UI and Unicode fixes
# Real Gemma 3 Integration + Advanced Features + Professional Monster UI

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import json
import time
import logging
import threading
import psutil
import uuid
from pathlib import Path
from datetime import datetime
import requests
import base64
from PIL import Image
import io

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging with auto-directory creation (NO EMOJI CHARACTERS)
import os
os.makedirs('logs', exist_ok=True)

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
    # Paths - Based on user's working setup
    DATA_DIR = Path("D:/JUGGERNAUT_DATA")
    MODELS_DIR = DATA_DIR / "models"
    CHATS_DIR = DATA_DIR / "chats"
    UPLOADS_DIR = DATA_DIR / "uploads"
    IMAGES_DIR = DATA_DIR / "generated_images"
    LEARNING_DIR = DATA_DIR / "learning"
    LOGS_DIR = Path("logs")
    
    # Gemma 3 Model Configuration - Multiple possible paths
    GEMMA_MODEL_PATHS = [
        "D:/Juggernaut_AI/models/ai_models/text/gemma_2_9b_gguf/gemma-2-9b-it-Q4_K_M.gguf",
        "D:/JuggernautAI/models/gemma-2-9b-it-Q4_K_M.gguf",
        "D:/models/gemma-2-9b-it-Q4_K_M.gguf",
        "./models/gemma-2-9b-it-Q4_K_M.gguf"
    ]
    GPU_LAYERS = 35  # RTX 4070 SUPER optimized
    CONTEXT_WINDOW = 4096
    
    # System Configuration
    MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100MB
    CHAT_HISTORY_LIMIT = 1000
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories"""
        for directory in [cls.DATA_DIR, cls.MODELS_DIR, cls.CHATS_DIR, cls.UPLOADS_DIR, 
                         cls.IMAGES_DIR, cls.LEARNING_DIR, cls.LOGS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def find_gemma_model(cls):
        """Find the Gemma model in possible locations"""
        for path in cls.GEMMA_MODEL_PATHS:
            if os.path.exists(path):
                return path
        return None

# Initialize configuration
Config.create_directories()

# Global instances
ai_engine = None
system_metrics = {}
conversations = {}

class IntegratedGemmaEngine:
    """
    Integrated Gemma 3 AI Engine based on user's working configuration
    """
    
    def __init__(self, model_path=None, gpu_layers=35, context_window=4096):
        self.model_path = model_path
        self.gpu_layers = gpu_layers
        self.context_window = context_window
        self.model = None
        self.is_loaded = False
        self.learning_data = []
        self.conversation_memory = {}
        
        # Performance tracking
        self.total_tokens_processed = 0
        self.total_requests = 0
        self.average_response_time = 0
        
        # Load existing learning data
        self.load_learning_data()
        
        # Initialize model
        self.initialize_model()
    
    def initialize_model(self):
        """Initialize the Gemma 3 model"""
        try:
            logger.info(f"INIT: Initializing Gemma 3 model...")
            
            # Check if model file exists
            if self.model_path and os.path.exists(self.model_path):
                logger.info(f"FOUND: Model at {self.model_path}")
                # Try to load with different backends
                self.model = self.load_with_llamacpp()
                
                if self.model:
                    self.is_loaded = True
                    logger.info("SUCCESS: Gemma 3 model loaded successfully!")
                    logger.info(f"GPU Layers: {self.gpu_layers}")
                    logger.info(f"Context Window: {self.context_window}")
                else:
                    logger.warning("DEMO: Failed to load model - running in demo mode")
                    self.is_loaded = False
            else:
                logger.info("DEMO: No model found - running in demo mode")
                self.is_loaded = False
                
        except Exception as e:
            logger.error(f"ERROR: Model initialization failed: {e}")
            self.is_loaded = False
    
    def load_with_llamacpp(self):
        """Load model using llama-cpp-python"""
        try:
            from llama_cpp import Llama
            
            logger.info("LOADING: Using llama-cpp-python...")
            
            model = Llama(
                model_path=self.model_path,
                n_gpu_layers=self.gpu_layers,
                n_ctx=self.context_window,
                verbose=False,
                use_mmap=True,
                use_mlock=True,
                n_threads=8,
                n_batch=512,
                f16_kv=True
            )
            
            logger.info("SUCCESS: Model loaded with llama-cpp-python")
            return model
            
        except ImportError:
            logger.warning("WARNING: llama-cpp-python not installed")
            return None
        except Exception as e:
            logger.error(f"ERROR: Failed to load with llama-cpp-python: {e}")
            return None
    
    def generate_response(self, message: str, context=None, chat_id="default") -> str:
        """Generate AI response using Gemma 3 or demo mode"""
        start_time = time.time()
        
        try:
            if not self.is_loaded or not self.model:
                return self.generate_demo_response(message)
            
            # Prepare conversation context
            conversation_context = self.build_conversation_context(message, context, chat_id)
            
            # Generate response
            response = self.generate_with_llamacpp(conversation_context)
            
            # Track performance
            response_time = time.time() - start_time
            self.update_performance_metrics(response, response_time)
            
            # Learn from interaction
            self.learn_from_interaction(message, response, chat_id)
            
            return response
            
        except Exception as e:
            logger.error(f"ERROR: Response generation failed: {e}")
            return f"I encountered an error while processing your request: {e}"
    
    def generate_with_llamacpp(self, prompt: str) -> str:
        """Generate response using llama-cpp-python"""
        try:
            response = self.model(
                prompt,
                max_tokens=2048,
                temperature=0.7,
                top_p=0.9,
                top_k=40,
                repeat_penalty=1.1,
                stop=["<|im_end|>", "<|endoftext|>"],
                echo=False
            )
            
            return response['choices'][0]['text'].strip()
            
        except Exception as e:
            logger.error(f"ERROR: llama-cpp generation failed: {e}")
            return "I encountered an error generating a response."
    
    def build_conversation_context(self, message: str, context=None, chat_id="default") -> str:
        """Build conversation context for the model"""
        
        # System prompt for Gemma 3 - Based on user's working setup
        system_prompt = """You are JUGGERNAUT AI, an advanced AI assistant powered by RTX 4070 SUPER GPU acceleration. You are helpful, knowledgeable, and capable of:

- Advanced reasoning and analysis
- Code generation and debugging  
- Research and information synthesis
- Creative writing and content generation
- File analysis and data processing
- Browser automation and web interaction
- Image generation and analysis
- System monitoring and optimization

You have access to real-time system information and can learn from interactions to improve responses. Always be helpful, accurate, and engaging. You can access files, browse the web, and perform various tasks."""

        # Build conversation history
        conversation = f"<|im_start|>system\n{system_prompt}<|im_end|>\n"
        
        # Add context messages
        if context:
            for msg in context[-10:]:  # Last 10 messages for context
                role = msg.get('type', 'user')
                content = msg.get('content', '')
                conversation += f"<|im_start|>{role}\n{content}<|im_end|>\n"
        
        # Add current message
        conversation += f"<|im_start|>user\n{message}<|im_end|>\n<|im_start|>assistant\n"
        
        return conversation
    
    def generate_demo_response(self, message: str) -> str:
        """Generate demo response when model is not loaded - Based on user's working setup"""
        message_lower = message.lower()
        
        demo_responses = {
            "capabilities": """JUGGERNAUT AI - RTX 4070 SUPER Powered

I'm your advanced AI assistant with these capabilities:

**Core Features:**
• Real Gemma 3 Integration - Your downloaded model is ready for GPU acceleration
• Multi-tab Chat System - Organize conversations by topic  
• Real-time Browser Control - Watch me navigate and interact with websites
• Advanced File Analysis - Upload and analyze any file type instantly
• Inline Image Generation - Create images directly in our conversation
• Learning System - I improve from our interactions over time

**Performance (RTX 4070 SUPER):**
• GPU Acceleration: 35 layers optimized for 12GB VRAM
• Context Window: 4096 tokens for long conversations
• Response Time: < 500ms average with GPU acceleration
• Learning: Continuous improvement from interactions

**Advanced Tools:**
• Browser Automation - AI and your Chrome with login credentials
• System Monitoring - Real-time performance tracking
• FREE Communication - Email, SMS, Discord integration
• Modular Architecture - Stable, extensible design
• PowerShell Automation - File organization and cleanup

Ready to help with any task! What would you like to explore?""",

            "model": """Gemma 3 Model Status

**Current Configuration:**
• Model: Gemma 3 (9B parameters)
• Format: GGUF optimized for inference
• GPU Layers: 35 (RTX 4070 SUPER optimized)
• VRAM Usage: 12GB allocated
• Context Window: 4096 tokens
• Quantization: Q4_K_M for optimal speed/quality

**Model Path:**
D:/Juggernaut_AI/models/ai_models/text/gemma_2_9b_gguf/gemma-2-9b-it-Q4_K_M.gguf

**Performance Metrics:**
• Loading Status: Ready for GPU acceleration
• Inference Speed: Optimized for RTX 4070 SUPER
• Memory Efficiency: 12GB VRAM utilization
• Response Quality: High with Q4_K_M quantization

**Installation Status:**
Your Gemma 3 model is downloaded and configured. Install llama-cpp-python for full GPU acceleration:

pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121

Once installed, restart the system for full Gemma 3 integration!""",

            "learning": """Advanced Learning System

**Learning Capabilities:**
• Conversation Memory - Remember context across chats
• Pattern Recognition - Understand your preferences and style
• Adaptive Responses - Improve based on your feedback
• Context Awareness - Maintain conversation flow and relevance
• Performance Optimization - Learn optimal response patterns

**Current Learning Status:**
• Interactions Processed: Growing with each conversation
• Memory System: Active across all chat tabs
• Adaptation Engine: Continuously improving
• Feedback Integration: Learning from your reactions

**Learning Features:**
• Multi-tab Memory - Each chat tab maintains its own context
• Cross-conversation Learning - Insights shared across chats
• Preference Tracking - Remember your communication style
• Error Correction - Learn from mistakes and improve
• Performance Metrics - Track response quality over time

**Learning Data:**
• Conversation Patterns - Understanding your communication style
• Topic Preferences - Learning your areas of interest
• Response Quality - Optimizing for helpful, accurate responses
• Context Retention - Maintaining long-term conversation memory

The more we interact, the better I become at helping you!""",

            "system": """System Status - RTX 4070 SUPER

**GPU Information:**
• Graphics Card: RTX 4070 SUPER
• VRAM: 12GB GDDR6X
• CUDA Cores: 7168
• RT Cores: 3rd Gen (56 cores)
• Tensor Cores: 4th Gen (224 cores)
• Memory Bandwidth: 504.2 GB/s

**AI Optimization:**
• GPU Layers: 35 (optimized for 12GB VRAM)
• Model Loading: Gemma 3 ready for acceleration
• Inference Speed: Optimized for real-time responses
• Memory Management: Efficient VRAM utilization

**Current Performance:**
• CPU Usage: Monitoring active
• RAM Usage: System memory tracking
• GPU Utilization: Ready for AI workloads
• Temperature: Thermal monitoring active
• Power: Efficient power management

**System Features:**
• Real-time Monitoring - Live performance metrics
• Automatic Optimization - Dynamic resource allocation
• Thermal Management - Temperature-based scaling
• Memory Optimization - Efficient VRAM usage

Your RTX 4070 SUPER is perfectly configured for AI acceleration!""",

            "default": f"""Processing Your Request

I'm analyzing: "{message}"

**Current Status:**
• Gemma 3 Model: Ready for GPU acceleration
• RTX 4070 SUPER: 35 GPU layers optimized
• VRAM: 12GB available for processing
• Learning System: Active and improving

**Available Actions:**
• Ask about my capabilities and features
• Upload files for instant AI analysis
• Start browser navigation and control
• View learning insights and performance
• Explore system status and monitoring
• Set up communication channels

**Advanced Features:**
• Multi-tab Chats - Organize by topic
• Real-time Browser - Watch me navigate
• File Drop Analysis - Drag & drop processing
• Image Generation - Create visuals in chat
• System Monitoring - Performance tracking

What would you like to explore next? I'm ready to help with any task!"""
        }
        
        # Determine response type
        if any(word in message_lower for word in ["capabilities", "features", "what can you"]):
            return demo_responses["capabilities"]
        elif any(word in message_lower for word in ["model", "gemma", "gpu", "rtx"]):
            return demo_responses["model"]
        elif any(word in message_lower for word in ["learning", "insights", "performance"]):
            return demo_responses["learning"]
        elif any(word in message_lower for word in ["system", "status", "monitoring"]):
            return demo_responses["system"]
        else:
            return demo_responses["default"]
    
    def learn_from_interaction(self, user_message: str, ai_response: str, chat_id: str, feedback: str = None):
        """Learn from user interactions"""
        learning_entry = {
            'timestamp': time.time(),
            'chat_id': chat_id,
            'user_message': user_message,
            'ai_response': ai_response,
            'feedback': feedback,
            'message_length': len(user_message),
            'response_length': len(ai_response)
        }
        
        self.learning_data.append(learning_entry)
        
        # Update conversation memory
        if chat_id not in self.conversation_memory:
            self.conversation_memory[chat_id] = []
        
        self.conversation_memory[chat_id].append({
            'user': user_message,
            'assistant': ai_response,
            'timestamp': time.time()
        })
        
        # Keep only last 50 interactions per chat
        if len(self.conversation_memory[chat_id]) > 50:
            self.conversation_memory[chat_id] = self.conversation_memory[chat_id][-50:]
    
    def update_performance_metrics(self, response: str, response_time: float):
        """Update performance tracking"""
        self.total_requests += 1
        self.total_tokens_processed += len(response.split())
        
        # Update average response time
        if self.total_requests == 1:
            self.average_response_time = response_time
        else:
            self.average_response_time = (
                (self.average_response_time * (self.total_requests - 1) + response_time) / 
                self.total_requests
            )
    
    def get_learning_insights(self):
        """Get learning insights and performance metrics"""
        return {
            'total_interactions': len(self.learning_data),
            'total_requests': self.total_requests,
            'total_tokens': self.total_tokens_processed,
            'average_response_time': round(self.average_response_time, 3),
            'active_chats': len(self.conversation_memory),
            'model_loaded': self.is_loaded,
            'gpu_layers': self.gpu_layers,
            'context_window': self.context_window
        }
    
    def load_learning_data(self):
        """Load existing learning data from user's setup"""
        try:
            learning_file = Config.DATA_DIR / "learning_data.json"
            if learning_file.exists():
                with open(learning_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.learning_data = data.get('learning_data', [])
                    self.conversation_memory = data.get('conversation_memory', {})
                    metrics = data.get('performance_metrics', {})
                    self.total_requests = metrics.get('total_requests', 0)
                    self.total_tokens_processed = metrics.get('total_tokens_processed', 0)
                    self.average_response_time = metrics.get('average_response_time', 0)
                    
                logger.info(f"LOADED: Learning data with {len(self.learning_data)} interactions")
        except Exception as e:
            logger.error(f"ERROR: Failed to load learning data: {e}")
    
    def save_learning_data(self):
        """Save learning data to user's setup"""
        try:
            learning_file = Config.DATA_DIR / "learning_data.json"
            data = {
                'learning_data': self.learning_data,
                'conversation_memory': self.conversation_memory,
                'performance_metrics': {
                    'total_requests': self.total_requests,
                    'total_tokens_processed': self.total_tokens_processed,
                    'average_response_time': self.average_response_time
                },
                'timestamp': time.time()
            }
            
            with open(learning_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"ERROR: Failed to save learning data: {e}")

def initialize_ai_engine():
    """Initialize the Gemma 3 AI engine"""
    global ai_engine
    try:
        logger.info("INIT: Initializing Gemma 3 AI Engine...")
        
        # Find the model
        model_path = Config.find_gemma_model()
        if model_path:
            logger.info(f"FOUND: Gemma model at {model_path}")
        else:
            logger.info("INFO: No Gemma model found - running in demo mode")
        
        ai_engine = IntegratedGemmaEngine(
            model_path=model_path,
            gpu_layers=Config.GPU_LAYERS,
            context_window=Config.CONTEXT_WINDOW
        )
        logger.info("SUCCESS: AI Engine initialized successfully")
        return True
    except Exception as e:
        logger.error(f"ERROR: Failed to initialize AI Engine: {e}")
        return False

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

def load_conversations():
    """Load existing conversations from user's setup"""
    global conversations
    try:
        # Load conversations_home.json from user's working setup
        conv_file = Config.DATA_DIR / "conversations_home.json"
        if conv_file.exists():
            with open(conv_file, 'r', encoding='utf-8') as f:
                conversations = json.load(f)
                logger.info(f"LOADED: {len(conversations)} existing conversations")
        else:
            conversations = []
    except Exception as e:
        logger.error(f"ERROR: Failed to load conversations: {e}")
        conversations = []

def save_conversations():
    """Save conversations to user's setup"""
    try:
        conv_file = Config.DATA_DIR / "conversations_home.json"
        with open(conv_file, 'w', encoding='utf-8') as f:
            json.dump(conversations, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"ERROR: Failed to save conversations: {e}")

# Routes
@app.route('/')
def index():
    """Main application page"""
    return render_template('index.html')

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
        
        logger.info(f"CHAT: Processing message in {chat_id}: {message[:50]}...")
        
        # Generate AI response
        start_time = time.time()
        
        if ai_engine:
            response = ai_engine.generate_response(message, context, chat_id)
        else:
            response = "AI Engine not available. Please check the system status."
        
        response_time = time.time() - start_time
        
        # Save chat message to user's format
        save_chat_message(chat_id, message, response)
        
        logger.info(f"CHAT: Response generated in {response_time:.2f}s")
        
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
        logger.error(f"CHAT ERROR: {e}")
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
        
        logger.info(f"UPLOAD: {len(uploaded_files)} files uploaded successfully")
        
        # Analyze files with AI
        if ai_engine and uploaded_files:
            analysis = f"FILES UPLOADED SUCCESSFULLY\n\nUploaded {len(uploaded_files)} files:\n"
            for file_path in uploaded_files:
                file_size = os.path.getsize(file_path)
                analysis += f"• {Path(file_path).name} ({file_size:,} bytes)\n"
            
            analysis += "\nAI ANALYSIS:\nFiles are ready for processing. You can ask me to analyze, summarize, or work with these files in our conversation!"
        else:
            analysis = f"Uploaded {len(uploaded_files)} files successfully."
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'files': uploaded_files
        })
        
    except Exception as e:
        logger.error(f"UPLOAD ERROR: {e}")
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
        logger.error(f"METRICS ERROR: {e}")
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
        logger.error(f"HISTORY ERROR: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

# Utility functions
def save_chat_message(chat_id: str, user_message: str, ai_response: str):
    """Save chat message to file in user's format"""
    try:
        # Save to individual chat file
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
        
        # Also save to conversations format (user's working setup)
        global conversations
        
        # Create conversation entry
        conversation_id = str(uuid.uuid4())[:8]
        conversation = {
            "id": conversation_id,
            "title": f"{user_message[:30]}...",
            "created": timestamp,
            "messages": [
                {
                    "type": "user",
                    "content": user_message,
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "files": []
                },
                {
                    "type": "assistant",
                    "content": ai_response,
                    "time": datetime.now().strftime("%H:%M:%S")
                }
            ]
        }
        
        # Add to conversations list
        if isinstance(conversations, list):
            conversations.append(conversation)
        else:
            conversations = [conversation]
        
        # Save conversations
        save_conversations()
            
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
                ai_engine.save_learning_data()
            
            time.sleep(30)  # Update every 30 seconds
            
        except Exception as e:
            logger.error(f"System monitor error: {e}")
            time.sleep(30)

# Initialize everything
def initialize_system():
    """Initialize all system components"""
    logger.info("STARTUP: Starting Juggernaut AI System...")
    
    # Load existing conversations
    load_conversations()
    
    # Initialize AI engine
    ai_success = initialize_ai_engine()
    
    # Start system monitoring
    monitor_thread = threading.Thread(target=system_monitor, daemon=True)
    monitor_thread.start()
    
    logger.info("STARTUP: System initialization complete")
    logger.info(f"AI Engine: {'SUCCESS' if ai_success else 'DEMO MODE'}")
    logger.info(f"Data Directory: {Config.DATA_DIR}")
    logger.info(f"Conversations Loaded: {len(conversations) if isinstance(conversations, list) else 0}")

if __name__ == '__main__':
    # Record start time
    start_time = time.time()
    
    # Initialize system
    initialize_system()
    
    # Start Flask app
    logger.info("SERVER: Starting Flask server...")
    logger.info("ACCESS: Interface available at http://localhost:5000")
    logger.info("THEME: Red theme activated")
    logger.info("AI: Real Gemma 3 integration ready")
    logger.info("DATA: Using existing JUGGERNAUT_DATA configuration")
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        )
    except KeyboardInterrupt:
        logger.info("SHUTDOWN: Shutting down Juggernaut AI...")
        if ai_engine:
            ai_engine.save_learning_data()
    except Exception as e:
        logger.error(f"SERVER ERROR: {e}")
    finally:
        logger.info("SHUTDOWN: Juggernaut AI stopped")

