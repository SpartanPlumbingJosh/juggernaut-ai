"""
Chat Manager Module - Handles multiple chats with save/edit functionality
"""

import os
import json
import uuid
from datetime import datetime

class ChatManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.chats_dir = os.path.join(data_path, "chats")
        self.active_chats = {}
        
        # Load existing chats
        self.load_existing_chats()
    
    def load_existing_chats(self):
        """Load all existing chat files"""
        try:
            if not os.path.exists(self.chats_dir):
                os.makedirs(self.chats_dir, exist_ok=True)
                return
            
            for filename in os.listdir(self.chats_dir):
                if filename.endswith('.json'):
                    chat_id = filename[:-5]  # Remove .json
                    chat_path = os.path.join(self.chats_dir, filename)
                    
                    with open(chat_path, 'r', encoding='utf-8') as f:
                        chat_data = json.load(f)
                        self.active_chats[chat_id] = chat_data
            
            print(f"✅ Loaded {len(self.active_chats)} existing chats")
            
        except Exception as e:
            print(f"Error loading chats: {e}")
    
    def create_chat(self, chat_id=None):
        """Create a new chat"""
        if not chat_id:
            chat_id = str(uuid.uuid4())[:8]
        
        chat_data = {
            "id": chat_id,
            "title": f"Chat {chat_id}",
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "messages": [],
            "metadata": {
                "message_count": 0,
                "total_tokens": 0,
                "tags": []
            }
        }
        
        self.active_chats[chat_id] = chat_data
        self.save_chat(chat_id)
        
        return chat_data
    
    def add_message(self, chat_id, role, content, message_type="text"):
        """Add message to chat"""
        if chat_id not in self.active_chats:
            self.create_chat(chat_id)
        
        message_id = str(uuid.uuid4())[:8]
        message = {
            "id": message_id,
            "role": role,
            "content": content,
            "type": message_type,
            "timestamp": datetime.now().isoformat(),
            "edited": False,
            "edit_history": []
        }
        
        self.active_chats[chat_id]["messages"].append(message)
        self.active_chats[chat_id]["last_updated"] = datetime.now().isoformat()
        self.active_chats[chat_id]["metadata"]["message_count"] += 1
        
        # Auto-update title based on first user message
        if role == "user" and len(self.active_chats[chat_id]["messages"]) == 1:
            title = content[:50] + "..." if len(content) > 50 else content
            self.active_chats[chat_id]["title"] = title
        
        self.save_chat(chat_id)
        return message_id
    
    def edit_message(self, chat_id, message_id, new_content):
        """Edit an existing message"""
        if chat_id not in self.active_chats:
            return False
        
        for message in self.active_chats[chat_id]["messages"]:
            if message["id"] == message_id:
                # Save edit history
                if not message["edited"]:
                    message["edit_history"] = []
                
                message["edit_history"].append({
                    "old_content": message["content"],
                    "edited_at": datetime.now().isoformat()
                })
                
                # Update message
                message["content"] = new_content
                message["edited"] = True
                message["last_edited"] = datetime.now().isoformat()
                
                self.active_chats[chat_id]["last_updated"] = datetime.now().isoformat()
                self.save_chat(chat_id)
                return True
        
        return False
    
    def delete_message(self, chat_id, message_id):
        """Delete a message"""
        if chat_id not in self.active_chats:
            return False
        
        messages = self.active_chats[chat_id]["messages"]
        for i, message in enumerate(messages):
            if message["id"] == message_id:
                del messages[i]
                self.active_chats[chat_id]["last_updated"] = datetime.now().isoformat()
                self.active_chats[chat_id]["metadata"]["message_count"] -= 1
                self.save_chat(chat_id)
                return True
        
        return False
    
    def get_chat(self, chat_id):
        """Get chat data"""
        return self.active_chats.get(chat_id, None)
    
    def get_all_chats(self):
        """Get all chat summaries"""
        summaries = []
        for chat_id, chat_data in self.active_chats.items():
            summary = {
                "id": chat_id,
                "title": chat_data["title"],
                "created": chat_data["created"],
                "last_updated": chat_data["last_updated"],
                "message_count": chat_data["metadata"]["message_count"],
                "preview": ""
            }
            
            # Get preview from last message
            if chat_data["messages"]:
                last_msg = chat_data["messages"][-1]
                preview = last_msg["content"][:100]
                summary["preview"] = preview + "..." if len(last_msg["content"]) > 100 else preview
            
            summaries.append(summary)
        
        # Sort by last updated
        summaries.sort(key=lambda x: x["last_updated"], reverse=True)
        return summaries
    
    def save_chat(self, chat_id):
        """Save chat to file"""
        if chat_id not in self.active_chats:
            return False
        
        try:
            chat_file = os.path.join(self.chats_dir, f"{chat_id}.json")
            with open(chat_file, 'w', encoding='utf-8') as f:
                json.dump(self.active_chats[chat_id], f, ensure_ascii=False, indent=2)
            return True
            
        except Exception as e:
            print(f"Error saving chat {chat_id}: {e}")
            return False
    
    def delete_chat(self, chat_id):
        """Delete a chat"""
        if chat_id not in self.active_chats:
            return False
        
        try:
            # Remove from memory
            del self.active_chats[chat_id]
            
            # Remove file
            chat_file = os.path.join(self.chats_dir, f"{chat_id}.json")
            if os.path.exists(chat_file):
                os.remove(chat_file)
            
            return True
            
        except Exception as e:
            print(f"Error deleting chat {chat_id}: {e}")
            return False
    
    def search_chats(self, query):
        """Search through chat messages"""
        results = []
        query_lower = query.lower()
        
        for chat_id, chat_data in self.active_chats.items():
            for message in chat_data["messages"]:
                if query_lower in message["content"].lower():
                    results.append({
                        "chat_id": chat_id,
                        "chat_title": chat_data["title"],
                        "message_id": message["id"],
                        "content": message["content"],
                        "role": message["role"],
                        "timestamp": message["timestamp"]
                    })
        
        return results
    
    def export_chat(self, chat_id, format="json"):
        """Export chat in various formats"""
        if chat_id not in self.active_chats:
            return None
        
        chat_data = self.active_chats[chat_id]
        
        if format == "json":
            return json.dumps(chat_data, ensure_ascii=False, indent=2)
        
        elif format == "txt":
            lines = [f"Chat: {chat_data['title']}", f"Created: {chat_data['created']}", "=" * 50, ""]
            
            for message in chat_data["messages"]:
                role = message["role"].upper()
                timestamp = message["timestamp"]
                content = message["content"]
                
                lines.append(f"[{timestamp}] {role}:")
                lines.append(content)
                lines.append("")
            
            return "\\n".join(lines)
        
        return None
    
    def get_chat_stats(self):
        """Get overall chat statistics"""
        total_chats = len(self.active_chats)
        total_messages = sum(chat["metadata"]["message_count"] for chat in self.active_chats.values())
        
        return {
            "total_chats": total_chats,
            "total_messages": total_messages,
            "active_chats": list(self.active_chats.keys())
        }

