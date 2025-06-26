# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from ai_engine import GemmaEngine
from browser_controller import BrowserController
from chat_manager import ChatManager
from plugin_manager import PluginManager
from file_manager import FileManager

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DATA_DIR = os.path.join(os.getcwd(), "data")
LOGS_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Core modules
gemma = GemmaEngine(model_path="D:/Juggernaut_AI/models/ai_models/text/gemma_2_9b_gguf/gemma-2-9b-it-Q4_K_M.gguf")
browser = BrowserController()
chats = ChatManager(DATA_DIR)
plugins = PluginManager()
files = FileManager(DATA_DIR)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)

@app.route("/api/chat/send", methods=["POST"])
def send_message():
    data = request.get_json()
    message = data.get("message")
    chat_id = data.get("chat_id", "default")
    user = data.get("user", "Josh")
    chats.add_message(chat_id, user, message)
    response = gemma.generate(message)
    chats.add_message(chat_id, "Juggernaut", response)
    return jsonify({"success": True, "response": response})

@app.route("/api/chats", methods=["GET"])
def get_chats():
    return jsonify(chats.get_all_chats())

@app.route("/api/chat/<chat_id>", methods=["GET"])
def get_chat(chat_id):
    return jsonify(chats.get_chat(chat_id))

@app.route("/api/chat/<chat_id>/edit", methods=["POST"])
def edit_message(chat_id):
    data = request.get_json()
    msg_idx = data.get("msg_idx")
    new_content = data.get("content")
    chats.edit_message(chat_id, msg_idx, new_content)
    return jsonify({"success": True})

@app.route("/api/files/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file provided"})
    f = request.files["file"]
    filename = files.save_file(f)
    return jsonify({"success": True, "filename": filename})

@app.route("/api/files/list", methods=["GET"])
def list_files():
    return jsonify({"files": files.list_files()})

@app.route("/api/files/analyze", methods=["POST"])
def analyze_file():
    data = request.get_json()
    filename = data.get("filename")
    result = files.analyze_file(filename)
    return jsonify({"result": result})

@app.route("/api/plugins/generate_image", methods=["POST"])
def generate_image():
    data = request.get_json()
    prompt = data.get("prompt", "Generate an image")
    image_url = plugins.generate_image(prompt)
    return jsonify({"image_url": image_url})

@app.route("/api/browser/command", methods=["POST"])
def browser_command():
    data = request.get_json()
    command = data.get("command")
    url = data.get("url")
    result = browser.execute(command, url)
    return jsonify({"result": result})

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "ai_ready": gemma.is_ready(),
        "browser_ready": browser.is_ready(),
        "system_ready": True
    })

if __name__ == "__main__":
    print("🚀 Juggernaut AI Monster UI running at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)

