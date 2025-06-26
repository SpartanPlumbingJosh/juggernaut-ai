"""
AI Engine Module - Handles all AI interactions
Modular component for the Juggernaut Unified Interface
"""

import os
import json
from datetime import datetime
from llama_cpp import Llama

class AIEngine:
    def __init__(self, data_path):
        self.data_path = data_path
        self.llm = None
        self.model_path = self.find_gemma_model()
        self.ready = False
        self.learning_data = {}
        
        # Load learning data
        self.load_learning_data()
        
        # Initialize in background
        import threading
        threading.Thread(target=self.initialize_model, daemon=True).start()
    
    def find_gemma_model(self):
        """Automatically find Gemma model in common locations"""
        possible_paths = [
            "models/ai_models/text/gemma_2_9b_gguf/gemma-2-9b-it-Q4_K_M.gguf",
            "D:/Juggernaut_AI/models/ai_models/text/gemma_2_9b_gguf/gemma-2-9b-it-Q4_K_M.gguf",
            "models/gemma-2-9b-it-Q4_K_M.gguf",
            "gemma-2-9b-it-Q4_K_M.gguf",
            "models/gemma/gemma-2-9b-it-Q4_K_M.gguf"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"✅ Found Gemma model: {path}")
                return path
        
        print("⚠️ Gemma model not found in common locations")
        print("📁 Searched paths:")
        for path in possible_paths:
            print(f"   - {path}")
        
        return possible_paths[0]  # Return default path
    
    def initialize_model(self):
        """Initialize the AI model"""
        try:
            if not os.path.exists(self.model_path):
                print(f"❌ Model not found: {self.model_path}")
                return
            
            print("🧠 Loading AI model...")
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=4096,
                n_gpu_layers=35,
                verbose=False
            )
            
            self.ready = True
            print("✅ AI model ready!")
            
        except Exception as e:
            print(f"❌ AI model error: {e}")
            self.ready = False
    
    def is_ready(self):
        """Check if AI is ready"""
        return self.ready
    
    def process_message(self, message, chat_id):
        """Process user message and return AI response"""
        if not self.ready:
            return "AI is still initializing, please wait..."
        
        try:
            # Learn from user input
            self.learn_from_interaction(message, chat_id)
            
            # Generate response
            response = self.llm(
                message,
                max_tokens=512,
                temperature=0.7,
                stop=["Human:", "User:"]
            )
            
            ai_response = response['choices'][0]['text'].strip()
            
            # Learn from AI response
            self.learn_from_response(ai_response, chat_id)
            
            return ai_response
            
        except Exception as e:
            return f"Error processing message: {str(e)}"
    
    def analyze_file(self, file_path):
        """Analyze uploaded file for research"""
        if not self.ready:
            return {"success": False, "error": "AI not ready"}
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Analyze with AI
            prompt = f"Analyze this file content and provide insights:\\n\\n{content[:2000]}"
            
            response = self.llm(
                prompt,
                max_tokens=1024,
                temperature=0.5
            )
            
            analysis = response['choices'][0]['text'].strip()
            
            return {
                "success": True,
                "analysis": analysis,
                "file_path": file_path
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def learn_from_interaction(self, message, chat_id):
        """Learn from user interactions"""
        try:
            timestamp = datetime.now().isoformat()
            
            if "interactions" not in self.learning_data:
                self.learning_data["interactions"] = []
            
            self.learning_data["interactions"].append({
                "timestamp": timestamp,
                "chat_id": chat_id,
                "message": message,
                "type": "user_input"
            })
            
            # Keep only recent interactions
            if len(self.learning_data["interactions"]) > 1000:
                self.learning_data["interactions"] = self.learning_data["interactions"][-1000:]
            
            self.save_learning_data()
            
        except Exception as e:
            print(f"Learning error: {e}")
    
    def learn_from_response(self, response, chat_id):
        """Learn from AI responses"""
        try:
            timestamp = datetime.now().isoformat()
            
            if "responses" not in self.learning_data:
                self.learning_data["responses"] = []
            
            self.learning_data["responses"].append({
                "timestamp": timestamp,
                "chat_id": chat_id,
                "response": response,
                "type": "ai_response"
            })
            
            # Keep only recent responses
            if len(self.learning_data["responses"]) > 1000:
                self.learning_data["responses"] = self.learning_data["responses"][-1000:]
            
            self.save_learning_data()
            
        except Exception as e:
            print(f"Learning error: {e}")
    
    def load_learning_data(self):
        """Load learning data from file"""
        try:
            learning_file = os.path.join(self.data_path, "ai_learning.json")
            if os.path.exists(learning_file):
                with open(learning_file, 'r', encoding='utf-8') as f:
                    self.learning_data = json.load(f)
                print(f"✅ Loaded AI learning data")
            else:
                self.learning_data = {}
                
        except Exception as e:
            print(f"Error loading learning data: {e}")
            self.learning_data = {}
    
    def save_learning_data(self):
        """Save learning data to file"""
        try:
            learning_file = os.path.join(self.data_path, "ai_learning.json")
            with open(learning_file, 'w', encoding='utf-8') as f:
                json.dump(self.learning_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Error saving learning data: {e}")
    
    def get_learning_stats(self):
        """Get learning statistics"""
        return {
            "interactions": len(self.learning_data.get("interactions", [])),
            "responses": len(self.learning_data.get("responses", [])),
            "ready": self.ready
        }

