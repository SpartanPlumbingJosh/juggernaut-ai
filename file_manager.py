# file_manager.py
import os
import shutil
import uuid

DATA_PATH = os.path.join("data", "files")
os.makedirs(DATA_PATH, exist_ok=True)

class FileManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data_path = DATA_PATH

    def save_file(self, file_storage):
        filename = file_storage.filename
        unique_id = str(uuid.uuid4())[:8]
        save_path = os.path.join(self.data_path, f"{unique_id}_{filename}")
        file_storage.save(save_path)
        return save_path

    def list_files(self):
        return [f for f in os.listdir(self.data_path) if os.path.isfile(os.path.join(self.data_path, f))]

    def get_file_path(self, filename):
        path = os.path.join(self.data_path, filename)
        if os.path.exists(path):
            return path
        return None

    def delete_file(self, filename):
        path = self.get_file_path(filename)
        if path:
            os.remove(path)
            return True
        return False

    def clear_all_files(self):
        for f in self.list_files():
            os.remove(os.path.join(self.data_path, f))

    def move_file(self, filename, new_dir):
        src = self.get_file_path(filename)
        if src and os.path.exists(new_dir):
            dst = os.path.join(new_dir, filename)
            shutil.move(src, dst)
            return dst
        return None
