"""
Juggernaut AI - Chat Manager
Handles chat session management, persistence, and organization
Production-ready with comprehensive error handling
"""

import os
import json
import logging
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime
import traceback

logger = logging.getLogger(__name__)

class ChatManager:
    """
    Advanced Chat Management System
    Features:
    - Multi-chat session support
    - Persistent storage with JSON
    - Thread-safe operations
    - Chat history management
    - Search and filtering
    - Export capabilities
    - Automatic cleanup
    """
    
    def __init__(self, data_path: str = "data"):
        self.data_path = data_path
        self.chats_path = os.path.join(data_path, "chats")
        self.chat_lock = threading.Lock()
        self.active_chats = {}
        self.chat_index = {}
        
        # Configuration
        self.max_chats_per_session = 100
        self.max_messages_per_chat = 1000
        self.auto_save_interval = 30  # seconds
        
        # Initialize system
        self._initialize_chat_system()
        
        logger.info("✅ Chat Manager initialized")

    def _initialize_chat_system(self):
        """Initialize the chat management system"""
        try:
            # Create directories
            os.makedirs(self.chats_path, exist_ok=True)
            
            # Load existing chats
            self._load_chat_index()
            
            # Start background tasks
            self._start_background_tasks()
            
        except Exception as e:
            logger.error(f"Chat system initialization error: {e}")
            logger.error(traceback.format_exc())

    def _load_chat_index(self):
        """Load chat index for quick access"""
        index_path = os.path.join(self.chats_path, "chat_index.json")
        
        try:
            if os.path.exists(index_path):
                with open(index_path, 'r', encoding='utf-8') as f:
                    self.chat_index = json.load(f)
                logger.info(f"📚 Loaded chat index with {len(self.chat_index)} entries")
            else:
                self.chat_index = {}
                self._save_chat_index()
                
        except Exception as e:
            logger.error(f"Failed to load chat index: {e}")
            self.chat_index = {}

    def _save_chat_index(self):
        """Save chat index to disk"""
        index_path = os.path.join(self.chats_path, "chat_index.json")
        
        try:
            with open(index_path, 'w', encoding='utf-8') as f:
                json.dump(self.chat_index, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save chat index: {e}")

    def save_chat(self, chat_id: str, chat_data: Dict[str, Any]) -> bool:
        """Save a chat session to disk"""
        try:
            with self.chat_lock:
                # Validate chat data
                if not self._validate_chat_data(chat_data):
                    logger.error(f"Invalid chat data for {chat_id}")
                    return False
                
                # Limit message count
                if len(chat_data.get('messages', [])) > self.max_messages_per_chat:
                    chat_data['messages'] = chat_data['messages'][-self.max_messages_per_chat:]
                    logger.warning(f"Truncated chat {chat_id} to {self.max_messages_per_chat} messages")
                
                # Save to file
                chat_file = os.path.join(self.chats_path, f"{chat_id}.json")
                with open(chat_file, 'w', encoding='utf-8') as f:
                    json.dump(chat_data, f, indent=2, ensure_ascii=False)
                
                # Update index
                self.chat_index[chat_id] = {
                    'title': chat_data.get('title', 'New Chat'),
                    'created_at': chat_data.get('created_at'),
                    'updated_at': chat_data.get('updated_at', datetime.now().isoformat()),
                    'message_count': len(chat_data.get('messages', [])),
                    'file_path': chat_file
                }
                
                # Update active chats
                self.active_chats[chat_id] = chat_data
                
                logger.debug(f"💾 Chat saved: {chat_id}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to save chat {chat_id}: {e}")
            logger.error(traceback.format_exc())
            return False

    def load_chat(self, chat_id: str) -> Optional[Dict[str, Any]]:
        """Load a specific chat session"""
        try:
            with self.chat_lock:
                # Check active chats first
                if chat_id in self.active_chats:
                    return self.active_chats[chat_id]
                
                # Load from disk
                chat_file = os.path.join(self.chats_path, f"{chat_id}.json")
                if not os.path.exists(chat_file):
                    logger.warning(f"Chat file not found: {chat_id}")
                    return None
                
                with open(chat_file, 'r', encoding='utf-8') as f:
                    chat_data = json.load(f)
                
                # Validate and cache
                if self._validate_chat_data(chat_data):
                    self.active_chats[chat_id] = chat_data
                    return chat_data
                else:
                    logger.error(f"Invalid chat data in file: {chat_id}")
                    return None
                    
        except Exception as e:
            logger.error(f"Failed to load chat {chat_id}: {e}")
            return None

    def load_all_chats(self) -> Dict[str, Dict[str, Any]]:
        """Load all chat sessions"""
        try:
            with self.chat_lock:
                loaded_chats = {}
                
                # Load from chat index
                for chat_id, chat_info in self.chat_index.items():
                    chat_data = self.load_chat(chat_id)
                    if chat_data:
                        loaded_chats[chat_id] = chat_data
                
                # Scan for any missing chats
                if os.path.exists(self.chats_path):
                    for filename in os.listdir(self.chats_path):
                        if filename.endswith('.json') and filename != 'chat_index.json':
                            chat_id = filename[:-5]  # Remove .json extension
                            if chat_id not in loaded_chats:
                                chat_data = self.load_chat(chat_id)
                                if chat_data:
                                    loaded_chats[chat_id] = chat_data
                
                self.active_chats = loaded_chats
                logger.info(f"📚 Loaded {len(loaded_chats)} chat sessions")
                return loaded_chats
                
        except Exception as e:
            logger.error(f"Failed to load all chats: {e}")
            return {}

    def delete_chat(self, chat_id: str) -> bool:
        """Delete a chat session"""
        try:
            with self.chat_lock:
                # Remove from active chats
                if chat_id in self.active_chats:
                    del self.active_chats[chat_id]
                
                # Remove from index
                if chat_id in self.chat_index:
                    del self.chat_index[chat_id]
                    self._save_chat_index()
                
                # Remove file
                chat_file = os.path.join(self.chats_path, f"{chat_id}.json")
                if os.path.exists(chat_file):
                    os.remove(chat_file)
                
                logger.info(f"🗑️ Chat deleted: {chat_id}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to delete chat {chat_id}: {e}")
            return False

    def search_chats(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search chats by content or title"""
        try:
            results = []
            query_lower = query.lower()
            
            with self.chat_lock:
                for chat_id, chat_data in self.active_chats.items():
                    # Search in title
                    title = chat_data.get('title', '').lower()
                    if query_lower in title:
                        results.append({
                            'chat_id': chat_id,
                            'title': chat_data.get('title'),
                            'match_type': 'title',
                            'created_at': chat_data.get('created_at'),
                            'message_count': len(chat_data.get('messages', []))
                        })
                        continue
                    
                    # Search in messages
                    for message in chat_data.get('messages', []):
                        content = message.get('content', '').lower()
                        if query_lower in content:
                            results.append({
                                'chat_id': chat_id,
                                'title': chat_data.get('title'),
                                'match_type': 'message',
                                'match_content': message.get('content')[:100] + '...',
                                'created_at': chat_data.get('created_at'),
                                'message_count': len(chat_data.get('messages', []))
                            })
                            break
                    
                    if len(results) >= limit:
                        break
            
            # Sort by relevance (title matches first, then by date)
            results.sort(key=lambda x: (
                0 if x['match_type'] == 'title' else 1,
                x.get('created_at', '')
            ), reverse=True)
            
            return results[:limit]
            
        except Exception as e:
            logger.error(f"Chat search error: {e}")
            return []

    def get_chat_statistics(self) -> Dict[str, Any]:
        """Get comprehensive chat statistics"""
        try:
            with self.chat_lock:
                total_chats = len(self.active_chats)
                total_messages = sum(
                    len(chat.get('messages', [])) 
                    for chat in self.active_chats.values()
                )
                
                # Calculate average messages per chat
                avg_messages = total_messages / max(total_chats, 1)
                
                # Find most active chat
                most_active_chat = None
                max_messages = 0
                for chat_id, chat_data in self.active_chats.items():
                    message_count = len(chat_data.get('messages', []))
                    if message_count > max_messages:
                        max_messages = message_count
                        most_active_chat = {
                            'id': chat_id,
                            'title': chat_data.get('title'),
                            'message_count': message_count
                        }
                
                # Calculate storage usage
                storage_size = 0
                if os.path.exists(self.chats_path):
                    for filename in os.listdir(self.chats_path):
                        file_path = os.path.join(self.chats_path, filename)
                        if os.path.isfile(file_path):
                            storage_size += os.path.getsize(file_path)
                
                return {
                    'total_chats': total_chats,
                    'total_messages': total_messages,
                    'average_messages_per_chat': round(avg_messages, 2),
                    'most_active_chat': most_active_chat,
                    'storage_size_bytes': storage_size,
                    'storage_size_mb': round(storage_size / (1024 * 1024), 2)
                }
                
        except Exception as e:
            logger.error(f"Failed to get chat statistics: {e}")
            return {}

    def export_chat(self, chat_id: str, format: str = 'json') -> Optional[str]:
        """Export a chat to various formats"""
        try:
            chat_data = self.load_chat(chat_id)
            if not chat_data:
                return None
            
            export_dir = os.path.join(self.data_path, "exports")
            os.makedirs(export_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if format == 'json':
                export_file = os.path.join(export_dir, f"chat_{chat_id}_{timestamp}.json")
                with open(export_file, 'w', encoding='utf-8') as f:
                    json.dump(chat_data, f, indent=2, ensure_ascii=False)
                    
            elif format == 'txt':
                export_file = os.path.join(export_dir, f"chat_{chat_id}_{timestamp}.txt")
                with open(export_file, 'w', encoding='utf-8') as f:
                    f.write(f"Chat Export: {chat_data.get('title', 'Untitled')}\n")
                    f.write(f"Created: {chat_data.get('created_at', 'Unknown')}\n")
                    f.write(f"Messages: {len(chat_data.get('messages', []))}\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for message in chat_data.get('messages', []):
                        role = message.get('role', 'unknown').title()
                        content = message.get('content', '')
                        timestamp = message.get('timestamp', '')
                        
                        f.write(f"[{timestamp}] {role}:\n")
                        f.write(f"{content}\n\n")
            
            logger.info(f"📤 Chat exported: {export_file}")
            return export_file
            
        except Exception as e:
            logger.error(f"Failed to export chat {chat_id}: {e}")
            return None

    def cleanup_old_chats(self, days_old: int = 30) -> int:
        """Clean up old inactive chats"""
        try:
            cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
            deleted_count = 0
            
            with self.chat_lock:
                chats_to_delete = []
                
                for chat_id, chat_data in self.active_chats.items():
                    updated_at = chat_data.get('updated_at')
                    if updated_at:
                        try:
                            chat_timestamp = datetime.fromisoformat(updated_at).timestamp()
                            if chat_timestamp < cutoff_date:
                                chats_to_delete.append(chat_id)
                        except ValueError:
                            # Invalid timestamp format, skip
                            continue
                
                # Delete old chats
                for chat_id in chats_to_delete:
                    if self.delete_chat(chat_id):
                        deleted_count += 1
            
            if deleted_count > 0:
                logger.info(f"🧹 Cleaned up {deleted_count} old chats")
            
            return deleted_count
            
        except Exception as e:
            logger.error(f"Chat cleanup error: {e}")
            return 0

    def _validate_chat_data(self, chat_data: Dict[str, Any]) -> bool:
        """Validate chat data structure"""
        try:
            required_fields = ['id', 'created_at', 'messages']
            for field in required_fields:
                if field not in chat_data:
                    return False
            
            # Validate messages structure
            messages = chat_data.get('messages', [])
            if not isinstance(messages, list):
                return False
            
            for message in messages:
                if not isinstance(message, dict):
                    return False
                if 'role' not in message or 'content' not in message:
                    return False
            
            return True
            
        except Exception:
            return False

    def _start_background_tasks(self):
        """Start background maintenance tasks"""
        def periodic_save():
            import time
            while True:
                try:
                    time.sleep(self.auto_save_interval)
                    self._save_chat_index()
                except Exception as e:
                    logger.error(f"Periodic save error: {e}")
        
        def periodic_cleanup():
            import time
            while True:
                try:
                    time.sleep(24 * 60 * 60)  # Daily cleanup
                    self.cleanup_old_chats()
                except Exception as e:
                    logger.error(f"Periodic cleanup error: {e}")
        
        # Start background threads
        save_thread = threading.Thread(target=periodic_save, daemon=True)
        cleanup_thread = threading.Thread(target=periodic_cleanup, daemon=True)
        
        save_thread.start()
        cleanup_thread.start()

    def get_recent_chats(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recently updated chats"""
        try:
            with self.chat_lock:
                chats = []
                for chat_id, chat_data in self.active_chats.items():
                    chats.append({
                        'id': chat_id,
                        'title': chat_data.get('title', 'New Chat'),
                        'updated_at': chat_data.get('updated_at'),
                        'message_count': len(chat_data.get('messages', [])),
                        'last_message': chat_data.get('messages', [{}])[-1].get('content', '')[:100] if chat_data.get('messages') else ''
                    })
                
                # Sort by update time
                chats.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
                return chats[:limit]
                
        except Exception as e:
            logger.error(f"Failed to get recent chats: {e}")
            return []

    def __del__(self):
        """Cleanup when manager is destroyed"""
        try:
            self._save_chat_index()
        except:
            pass

