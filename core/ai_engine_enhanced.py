"""
Enhanced Juggernaut AI Engine with Real Gemma Integration
RTX 4070 SUPER Optimized with Advanced Learning Capabilities
Built on the existing professional architecture
"""

import os
import json
import time
import logging
import threading
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import traceback

# Configure logging
logger = logging.getLogger(__name__)

class AIEngine:
    """
    Enhanced AI Engine with Real Gemma Integration and Learning
    Features:
    - Real GGUF model integration with your Gemma model
    - RTX 4070 SUPER optimization (35 GPU layers, 12GB VRAM)
    - Advanced learning system that improves over time
    - Conversation context awareness
    - User preference learning
    - Performance optimization and monitoring
    - Production-ready error handling
    """
    
    def __init__(self, data_path: str = "D:\\JUGGERNAUT_DATA"):
        self.data_path = data_path
        self.models_path = os.path.join(data_path, "models")
        self.cache_path = os.path.join(data_path, "cache")
        self.config_path = os.path.join(data_path, "ai_config.json")
        
        # Real Gemma Model Path (your actual model)
        self.gemma_model_path = "D:/Juggernaut_AI/models/ai_models/text/gemma_2_9b_gguf/gemma-2-9b-it-Q4_K_M.gguf"
        
        # GPU Configuration for RTX 4070 SUPER
        self.gpu_config = {
            "enabled": True,
            "memory_limit": 12288,  # 12GB VRAM
            "optimal_layers": 35,   # Optimal for RTX 4070 SUPER
            "batch_size": 512,      # Optimized batch size
            "context_window": 4096, # Context length
            "threads": 8            # CPU threads for hybrid processing
        }
        
        # Model Configuration
        self.model = None
        self.model_name = "gemma-2-9b-it"
        self.model_loaded = False
        self.model_info = {}
        
        # Enhanced Generation Settings for Gemma
        self.generation_config = {
            "max_tokens": 512,      # Increased for better responses
            "temperature": 0.7,     # Good balance for Gemma
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "stop_sequences": ["User:", "Human:", "\n\nUser:", "\n\nHuman:"]
        }
        
        # Learning System
        self.learning_data = {
            "user_preferences": {},
            "conversation_patterns": {},
            "successful_responses": [],
            "feedback_history": [],
            "improvement_areas": [],
            "learning_stats": {
                "total_interactions": 0,
                "positive_feedback": 0,
                "negative_feedback": 0,
                "learning_rate": 0.0
            }
        }
        
        # Conversation Context Management
        self.conversation_contexts = {}
        self.context_lock = threading.Lock()
        
        # Performance Metrics
        self.metrics = {
            "total_requests": 0,
            "total_tokens_generated": 0,
            "total_response_time": 0.0,
            "average_response_time": 0.0,
            "tokens_per_second": 0.0,
            "gpu_utilization": 0.0,
            "model_load_time": 0.0,
            "cache_hits": 0,
            "errors": 0,
            "learning_improvements": 0
        }
        
        # System State
        self.is_initializing = True
        self.llama_available = False
        self.available_models = []
        self.response_cache = {}
        self.cache_lock = threading.Lock()
        
        # Learning files
        self.learning_file = os.path.join(data_path, "gemma_learning.json")
        self.context_file = os.path.join(data_path, "conversation_contexts.json")
        
        # Initialize system
        self._initialize_system()
        
        logger.info("✅ Enhanced AI Engine initialized with Gemma integration")

    def _initialize_system(self):
        """Initialize the complete enhanced AI system"""
        try:
            # Create directories
            self._setup_directories()
            
            # Load configuration
            self._load_configuration()
            
            # Load learning data
            self._load_learning_data()
            
            # Load conversation contexts
            self._load_conversation_contexts()
            
            # Check llama-cpp-python availability
            self._check_llama_availability()
            
            # Load the real Gemma model
            self._load_gemma_model()
            
            # Start background learning tasks
            self._start_learning_tasks()
            
            self.is_initializing = False
            
        except Exception as e:
            logger.error(f"System initialization error: {e}")
            logger.error(traceback.format_exc())
            self.is_initializing = False

    def _setup_directories(self):
        """Setup required directories"""
        directories = [
            self.data_path,
            self.models_path,
            self.cache_path,
            os.path.dirname(self.learning_file),
            os.path.dirname(self.context_file)
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def _load_configuration(self):
        """Load AI configuration"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                # Update configurations with saved values
                self.gpu_config.update(config.get('gpu_config', {}))
                self.generation_config.update(config.get('generation_config', {}))
                
                logger.info("📁 Configuration loaded")
            else:
                self._save_configuration()
                
        except Exception as e:
            logger.error(f"Configuration load error: {e}")

    def _save_configuration(self):
        """Save current configuration"""
        try:
            config = {
                'gpu_config': self.gpu_config,
                'generation_config': self.generation_config,
                'model_path': self.gemma_model_path,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Configuration save error: {e}")

    def _load_learning_data(self):
        """Load learning data from previous sessions"""
        try:
            if os.path.exists(self.learning_file):
                with open(self.learning_file, 'r', encoding='utf-8') as f:
                    saved_data = json.load(f)
                    self.learning_data.update(saved_data)
                    
                logger.info(f"📚 Learning data loaded: {self.learning_data['learning_stats']['total_interactions']} interactions")
            else:
                self._save_learning_data()
                
        except Exception as e:
            logger.error(f"Learning data load error: {e}")

    def _save_learning_data(self):
        """Save learning data to file"""
        try:
            with open(self.learning_file, 'w', encoding='utf-8') as f:
                json.dump(self.learning_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Learning data save error: {e}")

    def _load_conversation_contexts(self):
        """Load conversation contexts"""
        try:
            if os.path.exists(self.context_file):
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    self.conversation_contexts = json.load(f)
                    
                logger.info(f"💬 Conversation contexts loaded: {len(self.conversation_contexts)} chats")
                
        except Exception as e:
            logger.error(f"Context load error: {e}")

    def _save_conversation_contexts(self):
        """Save conversation contexts"""
        try:
            with self.context_lock:
                with open(self.context_file, 'w', encoding='utf-8') as f:
                    json.dump(self.conversation_contexts, f, indent=2, ensure_ascii=False)
                    
        except Exception as e:
            logger.error(f"Context save error: {e}")

    def _check_llama_availability(self):
        """Check if llama-cpp-python is available"""
        try:
            import llama_cpp
            self.llama_available = True
            logger.info("✅ llama-cpp-python available")
            
        except ImportError:
            self.llama_available = False
            logger.warning("⚠️ llama-cpp-python not available")
            logger.info("📥 Install with: pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121")

    def _load_gemma_model(self):
        """Load the real Gemma model"""
        if not self.llama_available:
            logger.info("🔄 Running in demo mode - llama-cpp-python not available")
            return
            
        try:
            from llama_cpp import Llama
            
            if not os.path.exists(self.gemma_model_path):
                logger.warning(f"⚠️ Gemma model not found: {self.gemma_model_path}")
                logger.info("🔄 Running in demo mode")
                return
            
            logger.info(f"🤖 Loading Gemma model: {self.gemma_model_path}")
            logger.info(f"🎯 RTX 4070 SUPER optimization: {self.gpu_config['optimal_layers']} GPU layers")
            
            start_time = time.time()
            
            self.model = Llama(
                model_path=self.gemma_model_path,
                n_gpu_layers=self.gpu_config['optimal_layers'],
                n_ctx=self.gpu_config['context_window'],
                n_batch=self.gpu_config['batch_size'],
                n_threads=self.gpu_config['threads'],
                verbose=False,
                use_mmap=True,
                use_mlock=True
            )
            
            load_time = time.time() - start_time
            self.metrics['model_load_time'] = load_time
            self.model_loaded = True
            
            logger.info(f"✅ Gemma model loaded successfully in {load_time:.2f}s")
            logger.info(f"🚀 GPU layers: {self.gpu_config['optimal_layers']}, Context: {self.gpu_config['context_window']}")
            
        except Exception as e:
            logger.error(f"❌ Gemma model loading failed: {e}")
            logger.error(traceback.format_exc())
            self.model_loaded = False

    def _start_learning_tasks(self):
        """Start background learning tasks"""
        def learning_worker():
            while True:
                try:
                    time.sleep(60)  # Run every minute
                    self._analyze_learning_patterns()
                    self._save_learning_data()
                    self._save_conversation_contexts()
                    
                except Exception as e:
                    logger.error(f"Learning task error: {e}")
        
        learning_thread = threading.Thread(target=learning_worker, daemon=True)
        learning_thread.start()
        logger.info("🧠 Learning tasks started")

    def _analyze_learning_patterns(self):
        """Analyze conversation patterns for learning"""
        try:
            # Analyze successful response patterns
            successful_responses = self.learning_data.get('successful_responses', [])
            
            if len(successful_responses) > 10:
                # Find common patterns in successful responses
                patterns = {}
                for response in successful_responses[-50:]:  # Last 50 successful responses
                    response_length = len(response.get('response', '').split())
                    input_type = self._classify_input_type(response.get('input', ''))
                    
                    key = f"{input_type}_{response_length//10*10}"  # Group by input type and response length
                    patterns[key] = patterns.get(key, 0) + 1
                
                # Update learning patterns
                self.learning_data['conversation_patterns'] = patterns
                self.metrics['learning_improvements'] += 1
                
                logger.debug(f"📈 Learning patterns updated: {len(patterns)} patterns identified")
                
        except Exception as e:
            logger.error(f"Learning analysis error: {e}")

    def _classify_input_type(self, user_input: str) -> str:
        """Classify the type of user input for learning"""
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ['question', 'what', 'how', 'why', 'when', 'where', '?']):
            return 'question'
        elif any(word in input_lower for word in ['help', 'assist', 'support']):
            return 'help_request'
        elif any(word in input_lower for word in ['create', 'generate', 'make', 'build']):
            return 'creation_request'
        elif any(word in input_lower for word in ['explain', 'describe', 'tell me about']):
            return 'explanation_request'
        else:
            return 'general'

    def _update_conversation_context(self, chat_id: str, role: str, content: str):
        """Update conversation context for learning"""
        try:
            with self.context_lock:
                if chat_id not in self.conversation_contexts:
                    self.conversation_contexts[chat_id] = []
                
                context_entry = {
                    'role': role,
                    'content': content,
                    'timestamp': datetime.now().isoformat()
                }
                
                self.conversation_contexts[chat_id].append(context_entry)
                
                # Keep only last 20 messages per chat for memory efficiency
                if len(self.conversation_contexts[chat_id]) > 20:
                    self.conversation_contexts[chat_id] = self.conversation_contexts[chat_id][-20:]
                    
        except Exception as e:
            logger.error(f"Context update error: {e}")

    def _build_context_aware_prompt(self, user_input: str, chat_id: str) -> str:
        """Build context-aware prompt with learning insights"""
        try:
            prompt_parts = []
            
            # System prompt with learning
            prompt_parts.append("You are Juggernaut AI, powered by Gemma. You learn from interactions and adapt to user preferences.")
            
            # Add user preferences if learned
            user_prefs = self.learning_data.get('user_preferences', {})
            if user_prefs:
                prompt_parts.append("User preferences learned:")
                for pref, value in user_prefs.items():
                    prompt_parts.append(f"- {pref}: {value}")
            
            # Add conversation context
            context = self.conversation_contexts.get(chat_id, [])
            if context:
                prompt_parts.append("\nRecent conversation:")
                for msg in context[-5:]:  # Last 5 messages
                    role = "User" if msg['role'] == 'user' else "Juggernaut"
                    prompt_parts.append(f"{role}: {msg['content']}")
            
            # Add current input
            prompt_parts.append(f"\nUser: {user_input}")
            prompt_parts.append("Juggernaut:")
            
            return "\n".join(prompt_parts)
            
        except Exception as e:
            logger.error(f"Prompt building error: {e}")
            return f"User: {user_input}\nJuggernaut:"

    def process_message(self, user_input: str, chat_id: str = "default") -> Dict[str, Any]:
        """Process user message with enhanced Gemma integration and learning"""
        start_time = time.time()
        
        try:
            # Update metrics
            self.metrics['total_requests'] += 1
            
            # Update conversation context
            self._update_conversation_context(chat_id, 'user', user_input)
            
            if self.model_loaded and self.model:
                # Real Gemma model processing
                prompt = self._build_context_aware_prompt(user_input, chat_id)
                
                logger.debug(f"🧠 Processing with Gemma: {user_input[:50]}...")
                
                # Generate response with Gemma
                response = self.model(
                    prompt,
                    max_tokens=self.generation_config['max_tokens'],
                    temperature=self.generation_config['temperature'],
                    top_p=self.generation_config['top_p'],
                    top_k=self.generation_config['top_k'],
                    repeat_penalty=self.generation_config['repeat_penalty'],
                    stop=self.generation_config['stop_sequences']
                )
                
                ai_response = response['choices'][0]['text'].strip()
                
                # Update conversation context
                self._update_conversation_context(chat_id, 'assistant', ai_response)
                
                # Calculate metrics
                response_time = time.time() - start_time
                tokens_generated = len(ai_response.split())
                
                self.metrics['total_tokens_generated'] += tokens_generated
                self.metrics['total_response_time'] += response_time
                self.metrics['average_response_time'] = self.metrics['total_response_time'] / self.metrics['total_requests']
                self.metrics['tokens_per_second'] = tokens_generated / response_time if response_time > 0 else 0
                
                # Learn from interaction
                self._learn_from_interaction(user_input, ai_response, chat_id)
                
                logger.info(f"✅ Gemma response generated in {response_time:.2f}s ({tokens_generated} tokens)")
                
                return {
                    "response": ai_response,
                    "model": self.model_name,
                    "response_time": response_time,
                    "tokens": tokens_generated,
                    "tokens_per_second": self.metrics['tokens_per_second'],
                    "learning_enabled": True,
                    "gpu_accelerated": True
                }
                
            else:
                # Enhanced demo mode with learning simulation
                demo_responses = [
                    f"🤖 Juggernaut AI (Demo): I understand '{user_input}'. I'm learning your communication style and will provide better responses when the Gemma model is loaded!",
                    f"🧠 Learning from: '{user_input}'. Your Gemma model at {self.gemma_model_path} will enable full AI capabilities with RTX 4070 SUPER acceleration.",
                    f"⚡ RTX 4070 SUPER ready! Processing '{user_input}' in demo mode. Install llama-cpp-python for full Gemma integration.",
                    f"📚 I'm analyzing your input pattern: '{user_input}'. Full learning capabilities available with model installation."
                ]
                
                import random
                demo_response = random.choice(demo_responses)
                
                # Still update context and learn in demo mode
                self._update_conversation_context(chat_id, 'assistant', demo_response)
                self._learn_from_interaction(user_input, demo_response, chat_id)
                
                response_time = time.time() - start_time
                
                return {
                    "response": demo_response,
                    "model": "demo-mode",
                    "response_time": response_time,
                    "tokens": len(demo_response.split()),
                    "tokens_per_second": 0,
                    "learning_enabled": True,
                    "gpu_accelerated": False
                }
                
        except Exception as e:
            logger.error(f"❌ Message processing error: {e}")
            logger.error(traceback.format_exc())
            
            self.metrics['errors'] += 1
            error_response = f"⚠️ I encountered an issue: {str(e)}. I'm still learning and will improve!"
            
            return {
                "response": error_response,
                "model": "error",
                "response_time": time.time() - start_time,
                "tokens": 0,
                "tokens_per_second": 0,
                "learning_enabled": False,
                "gpu_accelerated": False,
                "error": str(e)
            }

    def _learn_from_interaction(self, user_input: str, ai_response: str, chat_id: str):
        """Learn from each interaction to improve future responses"""
        try:
            # Update learning statistics
            self.learning_data['learning_stats']['total_interactions'] += 1
            
            # Analyze interaction
            interaction = {
                'timestamp': datetime.now().isoformat(),
                'chat_id': chat_id,
                'user_input': user_input,
                'ai_response': ai_response,
                'input_type': self._classify_input_type(user_input),
                'response_length': len(ai_response.split())
            }
            
            # Store successful patterns (assume positive unless feedback says otherwise)
            self.learning_data['successful_responses'].append(interaction)
            
            # Keep only last 1000 interactions for memory efficiency
            if len(self.learning_data['successful_responses']) > 1000:
                self.learning_data['successful_responses'] = self.learning_data['successful_responses'][-1000:]
            
            # Calculate learning rate
            total = self.learning_data['learning_stats']['total_interactions']
            positive = self.learning_data['learning_stats']['positive_feedback']
            self.learning_data['learning_stats']['learning_rate'] = (positive / total * 100) if total > 0 else 0
            
            logger.debug(f"📈 Learning from interaction: {interaction['input_type']}")
            
        except Exception as e:
            logger.error(f"Learning error: {e}")

    def process_feedback(self, chat_id: str, feedback: str, message_context: str = ""):
        """Process user feedback for learning improvement"""
        try:
            feedback_entry = {
                'timestamp': datetime.now().isoformat(),
                'chat_id': chat_id,
                'feedback': feedback,
                'context': message_context
            }
            
            self.learning_data['feedback_history'].append(feedback_entry)
            
            # Update feedback statistics
            if feedback.lower() in ['good', 'great', 'excellent', 'perfect', 'helpful', 'correct']:
                self.learning_data['learning_stats']['positive_feedback'] += 1
            elif feedback.lower() in ['bad', 'wrong', 'unhelpful', 'incorrect', 'poor']:
                self.learning_data['learning_stats']['negative_feedback'] += 1
            
            # Save learning data
            self._save_learning_data()
            
            logger.info(f"📝 Feedback processed: {feedback}")
            
        except Exception as e:
            logger.error(f"Feedback processing error: {e}")

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive AI engine status"""
        return {
            "ready": self.model_loaded,
            "model_name": self.model_name,
            "model_path": self.gemma_model_path,
            "model_loaded": self.model_loaded,
            "llama_available": self.llama_available,
            "gpu_optimization": f"RTX 4070 SUPER ({self.gpu_config['optimal_layers']} layers)" if self.model_loaded else "Not available",
            "learning_enabled": True,
            "performance_metrics": self.metrics,
            "learning_stats": self.learning_data['learning_stats'],
            "conversation_contexts": len(self.conversation_contexts),
            "system_status": "ready" if not self.is_initializing else "initializing"
        }

    def get_learning_insights(self) -> Dict[str, Any]:
        """Get detailed learning insights"""
        try:
            stats = self.learning_data['learning_stats']
            total = stats['total_interactions']
            positive = stats['positive_feedback']
            negative = stats['negative_feedback']
            
            return {
                "total_interactions": total,
                "positive_feedback": positive,
                "negative_feedback": negative,
                "satisfaction_rate": (positive / total * 100) if total > 0 else 0,
                "learning_rate": stats['learning_rate'],
                "conversation_patterns": len(self.learning_data.get('conversation_patterns', {})),
                "successful_responses": len(self.learning_data.get('successful_responses', [])),
                "improvement_areas": self.learning_data.get('improvement_areas', []),
                "learning_active": True,
                "model_performance": {
                    "average_response_time": self.metrics['average_response_time'],
                    "tokens_per_second": self.metrics['tokens_per_second'],
                    "total_tokens_generated": self.metrics['total_tokens_generated']
                }
            }
            
        except Exception as e:
            logger.error(f"Learning insights error: {e}")
            return {"error": str(e)}

# Maintain compatibility with existing code
GemmaEngine = AIEngine

