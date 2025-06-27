#!/usr/bin/env python3
"""
JUGGERNAUT AI - ONE-CLICK LAUNCHER
Double-click to run - no PowerShell needed
Auto-updates from GitHub automatically
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import requests
import json

class JuggernautOneLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Juggernaut AI - One-Click Launcher")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Configure style
        self.root.configure(bg='#1a1a1a')
        
        # Variables
        self.auto_updater_process = None
        self.is_running = False
        
        # Create GUI
        self.create_widgets()
        
        # Auto-check for updates on startup
        threading.Thread(target=self.startup_check, daemon=True).start()
    
    def create_widgets(self):
        """Create the GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, 
                              text="JUGGERNAUT AI", 
                              bg='#1a1a1a',
                              fg='#dc2626',
                              font=('Segoe UI', 20, 'bold'))
        title_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(main_frame, 
                                 text="One-Click Auto-Updating AI System", 
                                 bg='#1a1a1a',
                                 fg='#d1d5db',
                                 font=('Segoe UI', 12))
        subtitle_label.pack(pady=(0, 20))
        
        # Features frame
        features_frame = ttk.LabelFrame(main_frame, text="Features", padding=10)
        features_frame.pack(fill=tk.X, pady=(0, 20))
        
        features_text = """✓ No PowerShell commands required
✓ Automatic updates from GitHub
✓ Real Gemma AI integration
✓ RTX 4070 SUPER optimized
✓ Professional Monster UI
✓ Background auto-updater
✓ One-click operation"""
        
        features_label = tk.Label(features_frame, 
                                 text=features_text,
                                 bg='white',
                                 fg='#374151',
                                 font=('Segoe UI', 10),
                                 justify=tk.LEFT)
        features_label.pack(anchor=tk.W)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="System Status", padding=10)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_label = tk.Label(status_frame, 
                                    text="Ready to launch", 
                                    bg='white',
                                    fg='#10b981',
                                    font=('Segoe UI', 11, 'bold'))
        self.status_label.pack()
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Launch button
        self.launch_button = tk.Button(button_frame, 
                                      text="🚀 LAUNCH JUGGERNAUT AI",
                                      command=self.launch_system,
                                      bg='#dc2626',
                                      fg='white',
                                      font=('Segoe UI', 12, 'bold'),
                                      height=2,
                                      relief=tk.FLAT)
        self.launch_button.pack(fill=tk.X, pady=(0, 10))
        
        # Update button
        self.update_button = tk.Button(button_frame, 
                                      text="🔄 CHECK FOR UPDATES",
                                      command=self.check_updates,
                                      bg='#374151',
                                      fg='white',
                                      font=('Segoe UI', 10),
                                      relief=tk.FLAT)
        self.update_button.pack(fill=tk.X, pady=(0, 10))
        
        # Stop button
        self.stop_button = tk.Button(button_frame, 
                                    text="⏹️ STOP SYSTEM",
                                    command=self.stop_system,
                                    bg='#ef4444',
                                    fg='white',
                                    font=('Segoe UI', 10),
                                    state=tk.DISABLED,
                                    relief=tk.FLAT)
        self.stop_button.pack(fill=tk.X)
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="System Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, 
                                                 height=12, 
                                                 bg='#0f0f0f', 
                                                 fg='#d1d5db',
                                                 font=('Consolas', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Initial log messages
        self.log("Juggernaut AI One-Click Launcher Ready")
        self.log("No PowerShell required - automatic GitHub updates")
        self.log("Click 'LAUNCH JUGGERNAUT AI' to start the system")
    
    def log(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_status(self, text, color="black"):
        """Update status label"""
        self.status_label.configure(text=text, fg=color)
    
    def startup_check(self):
        """Check for updates on startup"""
        try:
            self.log("Checking for updates from GitHub...")
            self.update_status("Checking for updates...", "#f59e0b")
            
            # Check GitHub for latest version
            response = requests.get("https://api.github.com/repos/SpartanPlumbingJosh/juggernaut-ai/commits/main", timeout=10)
            if response.status_code == 200:
                commit_data = response.json()
                latest_commit = commit_data['sha'][:8]
                commit_message = commit_data['commit']['message']
                
                self.log(f"Latest version: {latest_commit}")
                self.log(f"Latest update: {commit_message[:60]}...")
                self.update_status("Ready to launch - latest version available", "#10b981")
            else:
                self.log("Could not check for updates - will use local version")
                self.update_status("Ready to launch - offline mode", "#f59e0b")
                
        except Exception as e:
            self.log(f"Update check failed: {e}")
            self.update_status("Ready to launch - offline mode", "#f59e0b")
    
    def check_updates(self):
        """Check for updates manually"""
        threading.Thread(target=self._check_updates_thread, daemon=True).start()
    
    def _check_updates_thread(self):
        """Check for updates in separate thread"""
        try:
            self.log("Checking for updates...")
            self.update_status("Checking for updates...", "#f59e0b")
            
            # Run auto-updater check
            result = subprocess.run([
                sys.executable, "auto_updater.py", "--check-only"
            ], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
            
            if "Update available" in result.stdout:
                self.log("UPDATE AVAILABLE!")
                self.log("Downloading and installing update...")
                self.update_status("Installing update...", "#f59e0b")
                
                # Run full update
                update_result = subprocess.run([
                    sys.executable, "auto_updater.py"
                ], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
                
                if update_result.returncode == 0:
                    self.log("Update installed successfully!")
                    self.update_status("Updated - ready to launch", "#10b981")
                else:
                    self.log("Update failed - using current version")
                    self.update_status("Update failed - ready to launch", "#ef4444")
            else:
                self.log("No updates available")
                self.update_status("Up to date - ready to launch", "#10b981")
                
        except Exception as e:
            self.log(f"Update check error: {e}")
            self.update_status("Update check failed", "#ef4444")
    
    def launch_system(self):
        """Launch the Juggernaut AI system"""
        if self.is_running:
            messagebox.showwarning("Warning", "System is already running!")
            return
        
        self.log("LAUNCHING JUGGERNAUT AI SYSTEM...")
        self.update_status("Starting system...", "#f59e0b")
        
        # Disable launch button
        self.launch_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)
        
        # Start in separate thread
        threading.Thread(target=self._launch_system_thread, daemon=True).start()
    
    def _launch_system_thread(self):
        """Launch system in separate thread"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Start auto-updater (which will start Juggernaut)
            self.auto_updater_process = subprocess.Popen([
                sys.executable, "auto_updater.py"
            ], cwd=current_dir)
            
            self.is_running = True
            self.log("System started with auto-updater")
            self.log("Auto-updater will check for GitHub updates every 5 minutes")
            self.log("Web interface will be available at: http://localhost:5000")
            self.update_status("Running with auto-updates", "#10b981")
            
            # Wait for process
            self.auto_updater_process.wait()
            
            # Process ended
            self.is_running = False
            self.log("System stopped")
            self.update_status("Stopped", "#ef4444")
            self.launch_button.configure(state=tk.NORMAL)
            self.stop_button.configure(state=tk.DISABLED)
            
        except Exception as e:
            self.log(f"Launch error: {e}")
            self.update_status("Launch failed", "#ef4444")
            self.launch_button.configure(state=tk.NORMAL)
            self.stop_button.configure(state=tk.DISABLED)
            self.is_running = False
    
    def stop_system(self):
        """Stop the system"""
        if not self.is_running:
            messagebox.showwarning("Warning", "System is not running!")
            return
        
        self.log("Stopping Juggernaut AI system...")
        
        try:
            if self.auto_updater_process:
                self.auto_updater_process.terminate()
                self.auto_updater_process.wait(timeout=10)
                self.log("System stopped successfully")
            
        except subprocess.TimeoutExpired:
            self.log("Force stopping system...")
            self.auto_updater_process.kill()
            self.log("System force stopped")
        except Exception as e:
            self.log(f"Stop error: {e}")
        
        self.is_running = False
        self.auto_updater_process = None
        self.update_status("Stopped", "#ef4444")
        self.launch_button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)
    
    def on_closing(self):
        """Handle window closing"""
        if self.is_running:
            if messagebox.askokcancel("Quit", "Juggernaut AI is running. Stop and quit?"):
                self.stop_system()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Run the launcher"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    # Create and run one-click launcher
    launcher = JuggernautOneLauncher()
    launcher.run()

