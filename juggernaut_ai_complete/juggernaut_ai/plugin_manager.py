# plugin_manager.py
import os
import json
import uuid
from datetime import datetime
from PIL import Image

PLUGIN_DATA_PATH = os.path.join("data", "plugins")
IMAGE_OUTPUT_PATH = os.path.join("data", "images")
os.makedirs(PLUGIN_DATA_PATH, exist_ok=True)
os.makedirs(IMAGE_OUTPUT_PATH, exist_ok=True)

class PluginManager:
    def __init__(self):
        self.plugins = self.load_plugins()

    def load_plugins(self):
        plugins = {}
        for file in os.listdir(PLUGIN_DATA_PATH):
            if file.endswith(".json"):
                with open(os.path.join(PLUGIN_DATA_PATH, file), "r", encoding="utf-8") as f:
                    plugin_id = file.replace(".json", "")
                    plugins[plugin_id] = json.load(f)
        return plugins

    def save_plugin(self, plugin_id, plugin_data):
        with open(os.path.join(PLUGIN_DATA_PATH, f"{plugin_id}.json"), "w", encoding="utf-8") as f:
            json.dump(plugin_data, f, indent=2, ensure_ascii=False)

    def list_plugins(self):
        return list(self.plugins.keys())

    def add_plugin(self, name, description):
        plugin_id = str(uuid.uuid4())
        data = {
            "id": plugin_id,
            "name": name,
            "description": description,
            "created_at": datetime.now().isoformat()
        }
        self.plugins[plugin_id] = data
        self.save_plugin(plugin_id, data)
        return plugin_id

    def get_plugin(self, plugin_id):
        return self.plugins.get(plugin_id, {})

    # Example image generation handler (stub - replace with your actual AI integration)
    def generate_image(self, prompt, filename=None):
        if not filename:
            filename = f"img_{uuid.uuid4().hex[:8]}.png"
        path = os.path.join(IMAGE_OUTPUT_PATH, filename)
        # For now, just create a blank image as a stub
        img = Image.new("RGB", (512, 512), (255, 0, 0))
        img.save(path)
        return path

    def list_images(self):
        return [f for f in os.listdir(IMAGE_OUTPUT_PATH) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
