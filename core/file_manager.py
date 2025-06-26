# File Manager for Juggernaut AI
import os
import shutil
from datetime import datetime

class FileManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.files_path = os.path.join(data_path, "files")
        os.makedirs(self.files_path, exist_ok=True)
        print(" File Manager initialized")
    
    def save_file(self, filename, content):
        filepath = os.path.join(self.files_path, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath
    
    def read_file(self, filename):
        filepath = os.path.join(self.files_path, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    def list_files(self):
        if os.path.exists(self.files_path):
            return os.listdir(self.files_path)
        return []
    
    def delete_file(self, filename):
        filepath = os.path.join(self.files_path, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
