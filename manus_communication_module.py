#!/usr/bin/env python3
"""
MANUS COMMUNICATION MODULE
Enables Juggernaut AI to communicate with Manus for enhanced capabilities
"""

import json
import time
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class ManusCommBridge:
    """
    Communication bridge between Juggernaut AI and Manus
    Enables AI-to-AI consultation for complex tasks
    """
    
    def __init__(self, communication_dir: str = "D:/JuggernautAI/manus_comm"):
        self.comm_dir = Path(communication_dir)
        self.comm_dir.mkdir(parents=True, exist_ok=True)
        
        # Communication files
        self.outbox = self.comm_dir / "outbox.json"
        self.inbox = self.comm_dir / "inbox.json"
        self.conversation_log = self.comm_dir / "conversation_log.json"
        
        # Initialize communication files
        self.initialize_communication()
        
        logger.info(f"Manus Communication Bridge initialized at {self.comm_dir}")
    
    def initialize_communication(self):
        """Initialize communication files"""
        try:
            # Initialize outbox
            if not self.outbox.exists():
                self.outbox.write_text(json.dumps({
                    "messages": [],
                    "status": "ready",
                    "last_updated": datetime.now().isoformat()
                }, indent=2))
            
            # Initialize inbox
            if not self.inbox.exists():
                self.inbox.write_text(json.dumps({
                    "messages": [],
                    "status": "ready",
                    "last_updated": datetime.now().isoformat()
                }, indent=2))
            
            # Initialize conversation log
            if not self.conversation_log.exists():
                self.conversation_log.write_text(json.dumps({
                    "conversations": [],
                    "total_messages": 0,
                    "created": datetime.now().isoformat()
                }, indent=2))
                
        except Exception as e:
            logger.error(f"Failed to initialize communication files: {e}")
    
    def send_to_manus(self, message: str, context: Dict = None, priority: str = "normal") -> str:
        """
        Send a message to Manus for consultation
        
        Args:
            message: The question or request to send to Manus
            context: Additional context information
            priority: Message priority (low, normal, high, urgent)
            
        Returns:
            Message ID for tracking
        """
        try:
            message_id = f"msg_{int(time.time() * 1000)}"
            
            # Create message object
            message_obj = {
                "id": message_id,
                "timestamp": datetime.now().isoformat(),
                "message": message,
                "context": context or {},
                "priority": priority,
                "status": "pending",
                "sender": "juggernaut_ai"
            }
            
            # Load current outbox
            outbox_data = json.loads(self.outbox.read_text())
            
            # Add message to outbox
            outbox_data["messages"].append(message_obj)
            outbox_data["last_updated"] = datetime.now().isoformat()
            outbox_data["status"] = "has_messages"
            
            # Save updated outbox
            self.outbox.write_text(json.dumps(outbox_data, indent=2))
            
            # Log the conversation
            self.log_conversation("sent", message_obj)
            
            logger.info(f"Message sent to Manus: {message_id}")
            return message_id
            
        except Exception as e:
            logger.error(f"Failed to send message to Manus: {e}")
            return None
    
    def check_manus_response(self, message_id: str = None) -> Optional[Dict]:
        """
        Check for responses from Manus
        
        Args:
            message_id: Specific message ID to check for, or None for any response
            
        Returns:
            Response message object or None
        """
        try:
            if not self.inbox.exists():
                return None
            
            inbox_data = json.loads(self.inbox.read_text())
            
            if not inbox_data.get("messages"):
                return None
            
            # Find response
            for message in inbox_data["messages"]:
                if message_id is None or message.get("response_to") == message_id:
                    # Mark as read
                    message["status"] = "read"
                    message["read_timestamp"] = datetime.now().isoformat()
                    
                    # Update inbox
                    self.inbox.write_text(json.dumps(inbox_data, indent=2))
                    
                    # Log the conversation
                    self.log_conversation("received", message)
                    
                    logger.info(f"Response received from Manus: {message.get('id')}")
                    return message
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to check Manus response: {e}")
            return None
    
    def wait_for_manus_response(self, message_id: str, timeout: int = 300) -> Optional[Dict]:
        """
        Wait for a specific response from Manus
        
        Args:
            message_id: Message ID to wait for response to
            timeout: Maximum time to wait in seconds
            
        Returns:
            Response message object or None if timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            response = self.check_manus_response(message_id)
            if response:
                return response
            
            time.sleep(2)  # Check every 2 seconds
        
        logger.warning(f"Timeout waiting for Manus response to {message_id}")
        return None
    
    def ask_manus(self, question: str, context: Dict = None, wait_for_response: bool = True, timeout: int = 300) -> Optional[str]:
        """
        Ask Manus a question and optionally wait for response
        
        Args:
            question: The question to ask Manus
            context: Additional context
            wait_for_response: Whether to wait for response
            timeout: Maximum time to wait for response
            
        Returns:
            Manus response text or None
        """
        try:
            # Send question to Manus
            message_id = self.send_to_manus(question, context)
            
            if not message_id:
                return None
            
            if not wait_for_response:
                return message_id
            
            # Wait for response
            response = self.wait_for_manus_response(message_id, timeout)
            
            if response:
                return response.get("message", "")
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to ask Manus: {e}")
            return None
    
    def log_conversation(self, direction: str, message: Dict):
        """Log conversation for history tracking"""
        try:
            log_data = json.loads(self.conversation_log.read_text())
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "direction": direction,  # "sent" or "received"
                "message_id": message.get("id"),
                "message": message.get("message", ""),
                "context": message.get("context", {}),
                "priority": message.get("priority", "normal")
            }
            
            log_data["conversations"].append(log_entry)
            log_data["total_messages"] += 1
            
            # Keep only last 1000 conversations
            if len(log_data["conversations"]) > 1000:
                log_data["conversations"] = log_data["conversations"][-1000:]
            
            self.conversation_log.write_text(json.dumps(log_data, indent=2))
            
        except Exception as e:
            logger.error(f"Failed to log conversation: {e}")
    
    def get_conversation_history(self, limit: int = 50) -> List[Dict]:
        """Get recent conversation history"""
        try:
            log_data = json.loads(self.conversation_log.read_text())
            conversations = log_data.get("conversations", [])
            
            return conversations[-limit:] if conversations else []
            
        except Exception as e:
            logger.error(f"Failed to get conversation history: {e}")
            return []
    
    def clear_communication(self):
        """Clear all communication files"""
        try:
            self.initialize_communication()
            logger.info("Communication files cleared")
        except Exception as e:
            logger.error(f"Failed to clear communication: {e}")

# Global instance
manus_bridge = ManusCommBridge()

# Convenience functions for easy integration
def ask_manus(question: str, context: Dict = None, wait: bool = True, timeout: int = 300) -> Optional[str]:
    """
    Convenience function to ask Manus a question
    
    Usage:
        response = ask_manus("How do I optimize this code?", {"code": "..."})
        print(response)
    """
    return manus_bridge.ask_manus(question, context, wait, timeout)

def send_to_manus(message: str, context: Dict = None, priority: str = "normal") -> str:
    """
    Convenience function to send a message to Manus
    
    Usage:
        msg_id = send_to_manus("Please help me with this task", {"task_details": "..."})
    """
    return manus_bridge.send_to_manus(message, context, priority)

def check_manus_responses() -> List[Dict]:
    """
    Convenience function to check for any Manus responses
    
    Usage:
        responses = check_manus_responses()
        for response in responses:
            print(response["message"])
    """
    responses = []
    while True:
        response = manus_bridge.check_manus_response()
        if response:
            responses.append(response)
        else:
            break
    return responses

if __name__ == "__main__":
    # Test the communication bridge
    print("Testing Manus Communication Bridge...")
    
    # Send a test message
    msg_id = ask_manus("Hello Manus! This is a test message from Juggernaut AI. Can you confirm you received this?", 
                       {"test": True}, wait=False)
    
    print(f"Test message sent with ID: {msg_id}")
    print("Communication bridge is ready!")

