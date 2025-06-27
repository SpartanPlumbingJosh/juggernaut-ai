"""
Juggernaut AI - Hot Reload System
Automatically updates from GitHub without restart
"""

import os
import sys
import time
import json
import subprocess
import threading
import importlib
import logging
from pathlib import Path
from typing import Dict, List, Callable, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

class GitHubHotReloader:
    """
    Hot reload system that automatically pulls GitHub changes
    and updates the running system without restart
    """
    
    def __init__(self, repo_path: str, github_repo: str, branch: str = "main"):
        self.repo_path = Path(repo_path)
        self.github_repo = github_repo
        self.branch = branch
        self.last_commit_hash = None
        self.update_callbacks = []
        self.file_watchers = {}
        self.observer = None
        self.running = False
        
        # Track loaded modules for hot reload
        self.tracked_modules = set()
        self.original_modules = {}
        
        # Update settings
        self.check_interval = 30  # seconds
        self.auto_pull = True
        self.notify_updates = True
        
        logger.info(f"🔥 Hot Reload System initialized for {github_repo}")
    
    def start(self):
        """Start the hot reload system"""
        self.running = True
        
        # Start GitHub monitoring
        self.github_monitor_thread = threading.Thread(target=self._monitor_github, daemon=True)
        self.github_monitor_thread.start()
        
        # Start file system monitoring
        self.start_file_watcher()
        
        # Get initial commit hash
        self.last_commit_hash = self.get_current_commit_hash()
        
        logger.info("🚀 Hot Reload System started")
        logger.info(f"📁 Monitoring: {self.repo_path}")
        logger.info(f"🔗 GitHub: {self.github_repo}")
        logger.info(f"🌿 Branch: {self.branch}")
        logger.info(f"⏱️ Check interval: {self.check_interval}s")
    
    def stop(self):
        """Stop the hot reload system"""
        self.running = False
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
        
        logger.info("🛑 Hot Reload System stopped")
    
    def add_update_callback(self, callback: Callable):
        """Add callback to be called when updates occur"""
        self.update_callbacks.append(callback)
    
    def start_file_watcher(self):
        """Start watching local files for changes"""
        if self.observer:
            self.observer.stop()
        
        self.observer = Observer()
        handler = HotReloadHandler(self)
        
        # Watch main directories
        watch_dirs = [
            self.repo_path,
            self.repo_path / "static",
            self.repo_path / "templates",
            self.repo_path / "core",
            self.repo_path / "modules"
        ]
        
        for watch_dir in watch_dirs:
            if watch_dir.exists():
                self.observer.schedule(handler, str(watch_dir), recursive=True)
                logger.info(f"👀 Watching: {watch_dir}")
        
        self.observer.start()
    
    def _monitor_github(self):
        """Monitor GitHub for new commits"""
        while self.running:
            try:
                if self.auto_pull:
                    self.check_for_updates()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"GitHub monitoring error: {e}")
                time.sleep(self.check_interval)
    
    def check_for_updates(self) -> bool:
        """Check GitHub for new commits and pull if available"""
        try:
            # Get latest commit hash from GitHub API
            api_url = f"https://api.github.com/repos/{self.github_repo}/commits/{self.branch}"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                latest_commit = response.json()
                latest_hash = latest_commit['sha']
                
                if self.last_commit_hash and latest_hash != self.last_commit_hash:
                    logger.info(f"🔄 New commit detected: {latest_hash[:8]}")
                    logger.info(f"📝 Message: {latest_commit['commit']['message']}")
                    
                    # Pull the changes
                    if self.pull_changes():
                        self.last_commit_hash = latest_hash
                        self.trigger_hot_reload()
                        return True
                
                elif not self.last_commit_hash:
                    self.last_commit_hash = latest_hash
                    logger.info(f"📌 Initial commit hash: {latest_hash[:8]}")
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking for updates: {e}")
            return False
    
    def pull_changes(self) -> bool:
        """Pull changes from GitHub"""
        try:
            logger.info("⬇️ Pulling changes from GitHub...")
            
            # Change to repo directory
            original_dir = os.getcwd()
            os.chdir(self.repo_path)
            
            try:
                # Pull changes
                result = subprocess.run(
                    ["git", "pull", "origin", self.branch],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    logger.info("✅ Successfully pulled changes")
                    logger.info(f"📄 Output: {result.stdout.strip()}")
                    return True
                else:
                    logger.error(f"❌ Git pull failed: {result.stderr}")
                    return False
                    
            finally:
                os.chdir(original_dir)
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Git pull timed out")
            return False
        except Exception as e:
            logger.error(f"❌ Error pulling changes: {e}")
            return False
    
    def trigger_hot_reload(self):
        """Trigger hot reload of the system"""
        logger.info("🔥 Triggering hot reload...")
        
        try:
            # Reload Python modules
            self.reload_python_modules()
            
            # Notify callbacks
            for callback in self.update_callbacks:
                try:
                    callback()
                except Exception as e:
                    logger.error(f"Callback error: {e}")
            
            # Send WebSocket notification
            self.notify_clients_of_update()
            
            logger.info("✅ Hot reload completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Hot reload failed: {e}")
    
    def reload_python_modules(self):
        """Reload Python modules that have changed"""
        try:
            # Get list of modules to reload
            modules_to_reload = [
                'gemma3_engine',
                'free_communication_manager',
                'hot_reload_system'
            ]
            
            for module_name in modules_to_reload:
                if module_name in sys.modules:
                    try:
                        importlib.reload(sys.modules[module_name])
                        logger.info(f"🔄 Reloaded module: {module_name}")
                    except Exception as e:
                        logger.error(f"Failed to reload {module_name}: {e}")
            
            # Reload core modules
            core_path = self.repo_path / "core"
            if core_path.exists():
                for py_file in core_path.glob("*.py"):
                    module_name = f"core.{py_file.stem}"
                    if module_name in sys.modules:
                        try:
                            importlib.reload(sys.modules[module_name])
                            logger.info(f"🔄 Reloaded core module: {module_name}")
                        except Exception as e:
                            logger.error(f"Failed to reload {module_name}: {e}")
            
        except Exception as e:
            logger.error(f"Error reloading modules: {e}")
    
    def notify_clients_of_update(self):
        """Notify connected clients of the update"""
        try:
            # This would integrate with your WebSocket system
            update_message = {
                'type': 'system_update',
                'message': 'System updated from GitHub',
                'timestamp': datetime.now().isoformat(),
                'reload_required': False  # Hot reload means no page refresh needed
            }
            
            # Save update notification for WebSocket clients
            notification_file = self.repo_path / "temp" / "update_notification.json"
            notification_file.parent.mkdir(exist_ok=True)
            
            with open(notification_file, 'w') as f:
                json.dump(update_message, f)
            
            logger.info("📢 Client notification sent")
            
        except Exception as e:
            logger.error(f"Error notifying clients: {e}")
    
    def get_current_commit_hash(self) -> str:
        """Get current local commit hash"""
        try:
            original_dir = os.getcwd()
            os.chdir(self.repo_path)
            
            try:
                result = subprocess.run(
                    ["git", "rev-parse", "HEAD"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    return result.stdout.strip()
                
            finally:
                os.chdir(original_dir)
                
        except Exception as e:
            logger.error(f"Error getting commit hash: {e}")
        
        return None
    
    def force_update(self) -> bool:
        """Force update from GitHub"""
        logger.info("🔄 Force updating from GitHub...")
        
        if self.pull_changes():
            self.last_commit_hash = self.get_current_commit_hash()
            self.trigger_hot_reload()
            return True
        
        return False
    
    def get_status(self) -> Dict:
        """Get hot reload system status"""
        return {
            'running': self.running,
            'repo_path': str(self.repo_path),
            'github_repo': self.github_repo,
            'branch': self.branch,
            'last_commit_hash': self.last_commit_hash[:8] if self.last_commit_hash else None,
            'auto_pull': self.auto_pull,
            'check_interval': self.check_interval,
            'tracked_modules': len(self.tracked_modules),
            'update_callbacks': len(self.update_callbacks),
            'file_watcher_active': self.observer is not None and self.observer.is_alive()
        }


class HotReloadHandler(FileSystemEventHandler):
    """File system event handler for hot reload"""
    
    def __init__(self, reloader: GitHubHotReloader):
        self.reloader = reloader
        self.last_reload_time = 0
        self.reload_delay = 2  # seconds
    
    def on_modified(self, event):
        """Handle file modification events"""
        if event.is_directory:
            return
        
        # Avoid rapid successive reloads
        current_time = time.time()
        if current_time - self.last_reload_time < self.reload_delay:
            return
        
        file_path = Path(event.src_path)
        
        # Only reload for specific file types
        if file_path.suffix in ['.py', '.js', '.css', '.html']:
            logger.info(f"📝 File changed: {file_path.name}")
            
            # Handle different file types
            if file_path.suffix == '.py':
                self.handle_python_change(file_path)
            elif file_path.suffix in ['.js', '.css', '.html']:
                self.handle_static_change(file_path)
            
            self.last_reload_time = current_time
    
    def handle_python_change(self, file_path: Path):
        """Handle Python file changes"""
        try:
            # Reload specific module
            module_name = file_path.stem
            
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
                logger.info(f"🔄 Hot reloaded: {module_name}")
            
            # Notify callbacks
            for callback in self.reloader.update_callbacks:
                try:
                    callback()
                except Exception as e:
                    logger.error(f"Callback error: {e}")
                    
        except Exception as e:
            logger.error(f"Error handling Python change: {e}")
    
    def handle_static_change(self, file_path: Path):
        """Handle static file changes"""
        try:
            logger.info(f"🎨 Static file updated: {file_path.name}")
            
            # Notify clients to refresh static resources
            self.reloader.notify_clients_of_update()
            
        except Exception as e:
            logger.error(f"Error handling static change: {e}")


class HotReloadManager:
    """Manager for hot reload functionality"""
    
    def __init__(self, app, repo_path: str, github_repo: str):
        self.app = app
        self.reloader = GitHubHotReloader(repo_path, github_repo)
        self.setup_routes()
    
    def setup_routes(self):
        """Setup Flask routes for hot reload management"""
        
        @self.app.route('/api/hot-reload/status')
        def hot_reload_status():
            """Get hot reload status"""
            return {
                'success': True,
                'data': self.reloader.get_status()
            }
        
        @self.app.route('/api/hot-reload/force-update', methods=['POST'])
        def force_update():
            """Force update from GitHub"""
            success = self.reloader.force_update()
            return {
                'success': success,
                'message': 'Update completed' if success else 'Update failed'
            }
        
        @self.app.route('/api/hot-reload/toggle', methods=['POST'])
        def toggle_auto_pull():
            """Toggle auto-pull functionality"""
            self.reloader.auto_pull = not self.reloader.auto_pull
            return {
                'success': True,
                'auto_pull': self.reloader.auto_pull,
                'message': f"Auto-pull {'enabled' if self.reloader.auto_pull else 'disabled'}"
            }
        
        @self.app.route('/api/hot-reload/settings', methods=['POST'])
        def update_settings():
            """Update hot reload settings"""
            data = request.get_json()
            
            if 'check_interval' in data:
                self.reloader.check_interval = max(10, int(data['check_interval']))
            
            if 'auto_pull' in data:
                self.reloader.auto_pull = bool(data['auto_pull'])
            
            return {
                'success': True,
                'settings': {
                    'check_interval': self.reloader.check_interval,
                    'auto_pull': self.reloader.auto_pull
                }
            }
    
    def start(self):
        """Start hot reload system"""
        self.reloader.start()
    
    def stop(self):
        """Stop hot reload system"""
        self.reloader.stop()


# PowerShell script for manual updates
POWERSHELL_UPDATE_SCRIPT = '''
# Juggernaut AI - Manual Update Script
# Run this to manually pull GitHub changes

Write-Host "🔄 Juggernaut AI - Manual Update" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path ".git")) {
    Write-Host "❌ Error: Not in a git repository" -ForegroundColor Red
    Write-Host "Please run this script from your juggernaut-ai directory" -ForegroundColor Yellow
    pause
    exit 1
}

# Pull latest changes
Write-Host "⬇️ Pulling latest changes from GitHub..." -ForegroundColor Yellow
git pull origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Successfully updated from GitHub!" -ForegroundColor Green
    
    # Check if requirements changed
    if (git diff HEAD~1 HEAD --name-only | Select-String "requirements") {
        Write-Host "📦 Requirements file changed - updating dependencies..." -ForegroundColor Yellow
        pip install -r requirements.txt
    }
    
    Write-Host "🚀 Update complete! Restart the application to apply changes." -ForegroundColor Green
} else {
    Write-Host "❌ Failed to pull changes from GitHub" -ForegroundColor Red
    Write-Host "Please check your internet connection and try again" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
pause
'''

