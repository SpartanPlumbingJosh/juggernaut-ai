#!/usr/bin/env python3
"""
JUGGERNAUT AI - AUTO UPDATER
Automatically updates from GitHub without PowerShell
One-click solution with background updates
"""

import os
import sys
import json
import time
import threading
import subprocess
import requests
import shutil
import zipfile
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_updater.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class JuggernautAutoUpdater:
    def __init__(self):
        self.github_repo = "SpartanPlumbingJosh/juggernaut-ai"
        self.github_api_url = f"https://api.github.com/repos/{self.github_repo}"
        self.github_zip_url = f"https://github.com/{self.github_repo}/archive/refs/heads/main.zip"
        
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.temp_dir = os.path.join(self.current_dir, "temp_update")
        self.backup_dir = os.path.join(self.current_dir, "backup")
        
        self.update_interval = 300  # Check every 5 minutes
        self.current_commit = None
        self.is_running = False
        self.juggernaut_process = None
        
        # Load current commit info
        self.load_current_commit()
    
    def load_current_commit(self):
        """Load current commit hash from local file"""
        try:
            commit_file = os.path.join(self.current_dir, ".current_commit")
            if os.path.exists(commit_file):
                with open(commit_file, 'r') as f:
                    self.current_commit = f.read().strip()
                logger.info(f"Current commit: {self.current_commit}")
            else:
                logger.info("No current commit file found - first run")
        except Exception as e:
            logger.error(f"Error loading current commit: {e}")
    
    def save_current_commit(self, commit_hash):
        """Save current commit hash to local file"""
        try:
            commit_file = os.path.join(self.current_dir, ".current_commit")
            with open(commit_file, 'w') as f:
                f.write(commit_hash)
            self.current_commit = commit_hash
            logger.info(f"Saved current commit: {commit_hash}")
        except Exception as e:
            logger.error(f"Error saving current commit: {e}")
    
    def check_for_updates(self):
        """Check GitHub for new commits"""
        try:
            logger.info("Checking for updates from GitHub...")
            
            # Get latest commit info from GitHub API
            response = requests.get(f"{self.github_api_url}/commits/main", timeout=10)
            response.raise_for_status()
            
            commit_data = response.json()
            latest_commit = commit_data['sha']
            commit_message = commit_data['commit']['message']
            
            logger.info(f"Latest commit: {latest_commit}")
            logger.info(f"Commit message: {commit_message[:100]}...")
            
            # Check if update is needed
            if self.current_commit != latest_commit:
                logger.info("NEW UPDATE AVAILABLE!")
                logger.info(f"Current: {self.current_commit}")
                logger.info(f"Latest:  {latest_commit}")
                return True, latest_commit, commit_message
            else:
                logger.info("No updates available")
                return False, latest_commit, commit_message
                
        except Exception as e:
            logger.error(f"Error checking for updates: {e}")
            return False, None, None
    
    def download_update(self):
        """Download latest code from GitHub"""
        try:
            logger.info("Downloading update from GitHub...")
            
            # Create temp directory
            os.makedirs(self.temp_dir, exist_ok=True)
            
            # Download ZIP file
            response = requests.get(self.github_zip_url, timeout=30)
            response.raise_for_status()
            
            zip_path = os.path.join(self.temp_dir, "update.zip")
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            logger.info("Download complete, extracting...")
            
            # Extract ZIP file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
            
            # Find extracted directory
            extracted_dirs = [d for d in os.listdir(self.temp_dir) 
                            if os.path.isdir(os.path.join(self.temp_dir, d)) and d.startswith('juggernaut-ai-')]
            
            if not extracted_dirs:
                raise Exception("Could not find extracted directory")
            
            self.extracted_dir = os.path.join(self.temp_dir, extracted_dirs[0])
            logger.info(f"Extracted to: {self.extracted_dir}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error downloading update: {e}")
            return False
    
    def backup_current_version(self):
        """Backup current version before update"""
        try:
            logger.info("Creating backup of current version...")
            
            # Create backup directory
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}")
            os.makedirs(backup_path, exist_ok=True)
            
            # Files to backup
            important_files = [
                "juggernaut_real.py",
                "real_gemma_engine.py",
                "templates",
                "static",
                "requirements_real.txt",
                ".current_commit"
            ]
            
            for item in important_files:
                src_path = os.path.join(self.current_dir, item)
                if os.path.exists(src_path):
                    dst_path = os.path.join(backup_path, item)
                    if os.path.isdir(src_path):
                        shutil.copytree(src_path, dst_path)
                    else:
                        shutil.copy2(src_path, dst_path)
            
            logger.info(f"Backup created: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return False
    
    def apply_update(self):
        """Apply the downloaded update"""
        try:
            logger.info("Applying update...")
            
            # Files to update
            update_files = [
                "juggernaut_real.py",
                "real_gemma_engine.py",
                "templates",
                "static",
                "requirements_real.txt",
                "install_real_gemma.py",
                "auto_updater.py"
            ]
            
            for item in update_files:
                src_path = os.path.join(self.extracted_dir, item)
                dst_path = os.path.join(self.current_dir, item)
                
                if os.path.exists(src_path):
                    # Remove existing file/directory
                    if os.path.exists(dst_path):
                        if os.path.isdir(dst_path):
                            shutil.rmtree(dst_path)
                        else:
                            os.remove(dst_path)
                    
                    # Copy new file/directory
                    if os.path.isdir(src_path):
                        shutil.copytree(src_path, dst_path)
                    else:
                        shutil.copy2(src_path, dst_path)
                    
                    logger.info(f"Updated: {item}")
            
            logger.info("Update applied successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error applying update: {e}")
            return False
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
            logger.info("Temporary files cleaned up")
        except Exception as e:
            logger.error(f"Error cleaning up temp files: {e}")
    
    def install_dependencies(self):
        """Install/update dependencies"""
        try:
            logger.info("Installing/updating dependencies...")
            
            # Check if requirements file exists
            req_file = os.path.join(self.current_dir, "requirements_real.txt")
            if os.path.exists(req_file):
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", req_file, "--upgrade"
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info("Dependencies updated successfully")
                else:
                    logger.warning(f"Dependency update warning: {result.stderr}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error installing dependencies: {e}")
            return False
    
    def restart_juggernaut(self):
        """Restart the Juggernaut system"""
        try:
            logger.info("Restarting Juggernaut system...")
            
            # Stop current process if running
            if self.juggernaut_process:
                self.juggernaut_process.terminate()
                self.juggernaut_process.wait(timeout=10)
                logger.info("Stopped current Juggernaut process")
            
            # Start new process
            juggernaut_file = os.path.join(self.current_dir, "juggernaut_real.py")
            if os.path.exists(juggernaut_file):
                self.juggernaut_process = subprocess.Popen([
                    sys.executable, juggernaut_file
                ])
                logger.info("Started new Juggernaut process")
                return True
            else:
                logger.error("juggernaut_real.py not found")
                return False
                
        except Exception as e:
            logger.error(f"Error restarting Juggernaut: {e}")
            return False
    
    def perform_update(self, latest_commit, commit_message):
        """Perform complete update process"""
        try:
            logger.info("STARTING AUTO-UPDATE PROCESS")
            logger.info(f"Updating to commit: {latest_commit}")
            logger.info(f"Commit message: {commit_message}")
            
            # Step 1: Download update
            if not self.download_update():
                return False
            
            # Step 2: Backup current version
            if not self.backup_current_version():
                return False
            
            # Step 3: Apply update
            if not self.apply_update():
                return False
            
            # Step 4: Install dependencies
            self.install_dependencies()
            
            # Step 5: Save new commit hash
            self.save_current_commit(latest_commit)
            
            # Step 6: Clean up
            self.cleanup_temp_files()
            
            # Step 7: Restart system
            self.restart_juggernaut()
            
            logger.info("AUTO-UPDATE COMPLETED SUCCESSFULLY!")
            return True
            
        except Exception as e:
            logger.error(f"Update process failed: {e}")
            self.cleanup_temp_files()
            return False
    
    def start_auto_updater(self):
        """Start the auto-updater in background"""
        def update_loop():
            logger.info("Auto-updater started - checking for updates every 5 minutes")
            
            while self.is_running:
                try:
                    # Check for updates
                    has_update, latest_commit, commit_message = self.check_for_updates()
                    
                    if has_update:
                        logger.info("NEW UPDATE DETECTED - Starting auto-update...")
                        if self.perform_update(latest_commit, commit_message):
                            logger.info("Auto-update successful!")
                        else:
                            logger.error("Auto-update failed!")
                    
                    # Wait before next check
                    for _ in range(self.update_interval):
                        if not self.is_running:
                            break
                        time.sleep(1)
                        
                except Exception as e:
                    logger.error(f"Error in update loop: {e}")
                    time.sleep(60)  # Wait 1 minute before retrying
            
            logger.info("Auto-updater stopped")
        
        self.is_running = True
        self.update_thread = threading.Thread(target=update_loop, daemon=True)
        self.update_thread.start()
    
    def stop_auto_updater(self):
        """Stop the auto-updater"""
        self.is_running = False
        if hasattr(self, 'update_thread'):
            self.update_thread.join(timeout=5)
    
    def run_with_auto_update(self):
        """Run Juggernaut with auto-updater"""
        try:
            logger.info("JUGGERNAUT AI - AUTO-UPDATING SYSTEM")
            logger.info("No PowerShell required - automatic GitHub updates")
            
            # Start auto-updater
            self.start_auto_updater()
            
            # Start Juggernaut system
            juggernaut_file = os.path.join(self.current_dir, "juggernaut_real.py")
            if os.path.exists(juggernaut_file):
                logger.info("Starting Juggernaut AI system...")
                self.juggernaut_process = subprocess.Popen([
                    sys.executable, juggernaut_file
                ])
                
                # Wait for process to complete
                self.juggernaut_process.wait()
            else:
                logger.error("juggernaut_real.py not found - downloading from GitHub...")
                has_update, latest_commit, commit_message = self.check_for_updates()
                if has_update or not self.current_commit:
                    self.perform_update(latest_commit, commit_message)
                    self.run_with_auto_update()  # Retry after download
            
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        finally:
            self.stop_auto_updater()
            if self.juggernaut_process:
                self.juggernaut_process.terminate()

if __name__ == "__main__":
    updater = JuggernautAutoUpdater()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--check-only":
        # Just check for updates
        has_update, latest_commit, commit_message = updater.check_for_updates()
        if has_update:
            print(f"Update available: {latest_commit}")
            print(f"Message: {commit_message}")
        else:
            print("No updates available")
    else:
        # Run with auto-updater
        updater.run_with_auto_update()

