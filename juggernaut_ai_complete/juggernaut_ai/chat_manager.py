# chat_manager.py
import os
import json
from datetime import datetime

CHAT_DATA_PATH = os.path.join("data", "chats")
os.makedirs(CHAT_DATA_PATH, exist_ok=True)

class ChatManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.current_tab = "chat_1"
        self.chats = self.load_chats()

    def load_chats(self):
        chats = {}
        for file in os.listdir(CHAT_DATA_PATH):
            if file.endswith(".json"):
                with open(os.path.join(CHAT_DATA_PATH, file), "r", encoding="utf-8") as f:
                    chat_id = file.replace(".json", "")
                    chats[chat_id] = json.load(f)
        if not chats:
            chats["chat_1"] = []
        return chats

    def save_chat(self, chat_id, messages):
        with open(os.path.join(CHAT_DATA_PATH, f"{chat_id}.json"), "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)

    def add_message(self, chat_id, role, content):
        if chat_id not in self.chats:
            self.chats[chat_id] = []
        msg = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.chats[chat_id].append(msg)
        self.save_chat(chat_id, self.chats[chat_id])
        return msg

    def get_messages(self, chat_id):
        return self.chats.get(chat_id, [])

    def edit_message(self, chat_id, msg_index, new_content):
        if chat_id in self.chats and 0 <= msg_index < len(self.chats[chat_id]):
            self.chats[chat_id][msg_index]["content"] = new_content
            self.save_chat(chat_id, self.chats[chat_id])
            return True
        return False

    def get_chat(self, chat_id):
        return self.chats.get(chat_id, [])

    def get_all_chats(self):
        return {chat_id: messages for chat_id, messages in self.chats.items()}

