"""
Enhanced Juggernaut AI Engine with Real Gemma Integration
RTX 4070 SUPER Optimized with Learning Capabilities
"""

import os
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class EnhancedGemmaEngine:
    """
    Enhanced Gemma AI Engine with learning capabilities and RTX 4070 SUPER optimization
    """
    
    def __init__(self, data_path: str = "D:\\JUGGERNAUT_DATA"):
        self.data_path = data_path
        self.model_path = "D:/Juggernaut_AI/models/ai_models/text/gemma_2_9b_gguf/gemma-2-9b-it-Q4_K_M.gguf"
        self.model = None
        self.ready = False
        self.learning_data = {}
        self.conversation_context = {}
        self.performance_stats = {
            "total_requests": 0,
            "successful_responses": 0,
            "average_response_time": 0,
            "gpu_utilization": 0
        }
        
        # Initialize learning system
        self.learning_file = os.path.join(data_path, "gemma_learning.json")
        self.load_learning_data()
        
        # Initialize model
        self.initialize_model()
    
    def initialize_model(self):
        """Initialize Gemma model with RTX 4070 SUPER optimization"""
        try:
            logger.info("🤖 Initializing Enhanced Gemma AI Engine...")
            
            # Try to import llama-cpp-python for GGUF model support
            try:
                from llama_cpp import Llama
                
                # RTX 4070 SUPER optimized settings
                # 12GB VRAM - allocate 10GB for model, 2GB for system
                gpu_layers = 35  # Most layers on GPU for RTX 4070 SUPER
                context_length = 4096  # Good balance for 12GB VRAM
                
                logger.info(f"📁 Loading model: {self.model_path}")
                logger.info(f"🎯 RTX 4070 SUPER optimization: {gpu_layers} GPU layers")
                
                if os.path.exists(self.model_path):
                    self.model = Llama(
                        model_path=self.model_path,
                        n_gpu_layers=gpu_layers,  # RTX 4070 SUPER optimization
                        n_ctx=context_length,
                        n_batch=512,
                        verbose=False,
                        use_mmap=True,
                        use_mlock=True,
                        n_threads=8  # Optimize for modern CPUs
                    )
                    
                    self.ready = True
                    logger.info("✅ Gemma model loaded successfully with RTX 4070 SUPER acceleration")
                    logger.info(f"🚀 GPU layers: {gpu_layers}, Context: {context_length}")
                    
                else:
                    logger.warning(f"⚠️ Model file not found: {self.model_path}")
                    logger.info("🔄 Running in demo mode - install model for full functionality")
                    self.ready = False
                    
            except ImportError:
                logger.warning("⚠️ llama-cpp-python not available")
                logger.info("📥 Install with: pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121")
                logger.info("🔄 Running in demo mode")
                self.ready = False
                
        except Exception as e:
            logger.error(f"❌ Model initialization failed: {e}")
            self.ready = False
    
    def load_learning_data(self):
        """Load previous learning data"""
        try:
            if os.path.exists(self.learning_file):
                with open(self.learning_file, 'r', encoding='utf-8') as f:
                    self.learning_data = json.load(f)
                logger.info(f"📚 Loaded learning data: {len(self.learning_data)} entries")
            else:
                self.learning_data = {
                    "user_preferences": {},
                    "conversation_patterns": {},
                    "successful_responses": [],
                    "feedback_history": [],
                    "learning_stats": {
                        "total_interactions": 0,
                        "positive_feedback": 0,
                        "improvement_areas": []
                    }
                }
                logger.info("📝 Initialized new learning data")
        except Exception as e:
            logger.error(f"❌ Failed to load learning data: {e}")
            self.learning_data = {}
    
    def save_learning_data(self):
        """Save learning data to file"""
        try:
            os.makedirs(os.path.dirname(self.learning_file), exist_ok=True)
            with open(self.learning_file, 'w', encoding='utf-8') as f:
                json.dump(self.learning_data, f, indent=2, ensure_ascii=False)
            logger.debug("💾 Learning data saved")
        except Exception as e:
            logger.error(f"❌ Failed to save learning data: {e}")
    
    def learn_from_interaction(self, user_input: str, response: str, feedback: str = None):
        """Learn from user interactions to improve responses"""
        try:
            interaction = {
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input,
                "response": response,
                "feedback": feedback
            }
            
            # Update learning statistics
            self.learning_data["learning_stats"]["total_interactions"] += 1
            
            if feedback and feedback.lower() in ["good", "great", "excellent", "perfect"]:
                self.learning_data["learning_stats"]["positive_feedback"] += 1
                self.learning_data["successful_responses"].append(interaction)
            
            # Analyze conversation patterns
            input_length = len(user_input.split())
            if input_length not in self.learning_data["conversation_patterns"]:
                self.learning_data["conversation_patterns"][str(input_length)] = []
            
            self.learning_data["conversation_patterns"][str(input_length)].append({
                "input": user_input[:100],  # Store first 100 chars
                "response_quality": feedback or "neutral"
            })
            
            # Save learning data
            self.save_learning_data()
            
            logger.debug(f"📈 Learning from interaction: {feedback or 'no feedback'}")
            
        except Exception as e:
            logger.error(f"❌ Learning failed: {e}")
    
    def get_context_aware_prompt(self, user_input: str, chat_id: str = "default") -> str:
        """Create context-aware prompt based on learning data"""
        try:
            # Get conversation context
            context = self.conversation_context.get(chat_id, [])
            
            # Build enhanced prompt with context and learning
            prompt_parts = []
            
            # System prompt with learning insights
            prompt_parts.append("You are Juggernaut AI, an advanced AI assistant powered by Gemma.")
            prompt_parts.append("You learn from interactions and adapt to user preferences.")
            
            # Add learning insights if available
            if self.learning_data.get("user_preferences"):
                prompt_parts.append("User preferences learned:")
                for pref, value in self.learning_data["user_preferences"].items():
                    prompt_parts.append(f"- {pref}: {value}")
            
            # Add recent context
            if context:
                prompt_parts.append("\nRecent conversation:")
                for msg in context[-3:]:  # Last 3 messages for context
                    prompt_parts.append(f"{msg['role']}: {msg['content']}")
            
            # Add current user input
            prompt_parts.append(f"\nUser: {user_input}")
            prompt_parts.append("Juggernaut:")
            
            return "\n".join(prompt_parts)
            
        except Exception as e:
            logger.error(f"❌ Context prompt creation failed: {e}")
            return f"User: {user_input}\nJuggernaut:"
    
    def update_conversation_context(self, chat_id: str, role: str, content: str):
        """Update conversation context for learning"""
        try:
            if chat_id not in self.conversation_context:
                self.conversation_context[chat_id] = []
            
            self.conversation_context[chat_id].append({
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })
            
            # Keep only last 10 messages for memory efficiency
            if len(self.conversation_context[chat_id]) > 10:
                self.conversation_context[chat_id] = self.conversation_context[chat_id][-10:]
                
        except Exception as e:
            logger.error(f"❌ Context update failed: {e}")
    
    def generate_response(self, user_input: str, chat_id: str = "default") -> Dict[str, Any]:
        """Generate AI response with learning and context awareness"""
        start_time = time.time()
        
        try:
            # Update performance stats
            self.performance_stats["total_requests"] += 1
            
            # Update conversation context
            self.update_conversation_context(chat_id, "user", user_input)
            
            if self.ready and self.model:
                # Real Gemma model inference
                prompt = self.get_context_aware_prompt(user_input, chat_id)
                
                logger.debug(f"🧠 Generating response for: {user_input[:50]}...")
                
                response = self.model(
                    prompt,
                    max_tokens=512,
                    temperature=0.7,
                    top_p=0.9,
                    repeat_penalty=1.1,
                    stop=["User:", "Human:", "\n\n"]
                )
                
                ai_response = response['choices'][0]['text'].strip()
                
                # Update conversation context
                self.update_conversation_context(chat_id, "assistant", ai_response)
                
                # Performance tracking
                response_time = time.time() - start_time
                self.performance_stats["successful_responses"] += 1
                self.performance_stats["average_response_time"] = (
                    (self.performance_stats["average_response_time"] * (self.performance_stats["successful_responses"] - 1) + response_time) /
                    self.performance_stats["successful_responses"]
                )
                
                logger.info(f"✅ Generated response in {response_time:.2f}s")
                
                return {
                    "response": ai_response,
                    "model": "gemma-2-9b-it",
                    "response_time": response_time,
                    "tokens": len(ai_response.split()),
                    "learning_enabled": True
                }
                
            else:
                # Demo mode with learning simulation
                demo_responses = [
                    f"🤖 Juggernaut AI (Demo): I understand you said '{user_input}'. I'm ready to help when the Gemma model is loaded!",
                    f"🧠 Learning from your input: '{user_input}'. The full Gemma model will provide much more detailed responses.",
                    f"⚡ RTX 4070 SUPER ready! Your message '{user_input}' is noted. Install the Gemma model for full AI power.",
                    f"📚 I'm learning your communication style from '{user_input}'. Full functionality available with model installation."
                ]
                
                import random
                demo_response = random.choice(demo_responses)
                
                # Still learn from demo interactions
                self.update_conversation_context(chat_id, "assistant", demo_response)
                
                response_time = time.time() - start_time
                
                return {
                    "response": demo_response,
                    "model": "demo-mode",
                    "response_time": response_time,
                    "tokens": len(demo_response.split()),
                    "learning_enabled": True
                }
                
        except Exception as e:
            logger.error(f"❌ Response generation failed: {e}")
            error_response = f"⚠️ I encountered an issue processing your request: {str(e)}"
            
            return {
                "response": error_response,
                "model": "error",
                "response_time": time.time() - start_time,
                "tokens": 0,
                "learning_enabled": False,
                "error": str(e)
            }
    
    def process_feedback(self, chat_id: str, message_id: str, feedback: str):
        """Process user feedback for learning"""
        try:
            # Find the interaction in context
            context = self.conversation_context.get(chat_id, [])
            
            # Store feedback for learning
            feedback_entry = {
                "timestamp": datetime.now().isoformat(),
                "chat_id": chat_id,
                "message_id": message_id,
                "feedback": feedback
            }
            
            self.learning_data["feedback_history"].append(feedback_entry)
            
            # Update learning statistics
            if feedback.lower() in ["good", "great", "excellent", "perfect", "helpful"]:
                self.learning_data["learning_stats"]["positive_feedback"] += 1
            
            self.save_learning_data()
            logger.info(f"📈 Processed feedback: {feedback}")
            
        except Exception as e:
            logger.error(f"❌ Feedback processing failed: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get AI engine status and statistics"""
        return {
            "ready": self.ready,
            "model_path": self.model_path,
            "model_loaded": self.model is not None,
            "learning_enabled": True,
            "performance_stats": self.performance_stats,
            "learning_stats": self.learning_data.get("learning_stats", {}),
            "conversation_contexts": len(self.conversation_context),
            "gpu_optimization": "RTX 4070 SUPER (35 layers)" if self.ready else "Not available"
        }
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Get insights from learning data"""
        try:
            stats = self.learning_data.get("learning_stats", {})
            total = stats.get("total_interactions", 0)
            positive = stats.get("positive_feedback", 0)
            
            return {
                "total_interactions": total,
                "positive_feedback": positive,
                "satisfaction_rate": (positive / total * 100) if total > 0 else 0,
                "conversation_patterns": len(self.learning_data.get("conversation_patterns", {})),
                "successful_responses": len(self.learning_data.get("successful_responses", [])),
                "learning_active": True
            }
            
        except Exception as e:
            logger.error(f"❌ Learning insights failed: {e}")
            return {"error": str(e)}

# Compatibility alias for existing code
AIEngine = EnhancedGemmaEngine
GemmaEngine = EnhancedGemmaEngine

