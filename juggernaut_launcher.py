#!/usr/bin/env python3
"""
Juggernaut AI - Desktop Launcher
Simple one-click launcher for Juggernaut AI system
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import time
import webbrowser
import os
import sys
import json
from pathlib import Path
import requests
from datetime import datetime

class JuggernautLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 Juggernaut AI Launcher")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        # Set icon and styling
        self.setup_styling()
        
        # Process tracking
        self.flask_process = None
        self.is_running = False
        self.status_thread = None
        
        # Create GUI
        self.create_gui()
        
        # Start status monitoring
        self.start_status_monitoring()
    
    def setup_styling(self):
        """Setup dark theme styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', 
                       background='#1a1a1a', 
                       foreground='#ff3333',
                       font=('Arial', 16, 'bold'))
        
        style.configure('Status.TLabel',
                       background='#1a1a1a',
                       foreground='#ffffff',
                       font=('Arial', 10))
        
        style.configure('Start.TButton',
                       background='#ff3333',
                       foreground='#ffffff',
                       font=('Arial', 12, 'bold'))
        
        style.configure('Stop.TButton',
                       background='#666666',
                       foreground='#ffffff',
                       font=('Arial', 12, 'bold'))
    
    def create_gui(self):
        """Create the main GUI interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="🤖 JUGGERNAUT AI LAUNCHER", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        # System status
        self.status_label = ttk.Label(status_frame, 
                                     text="🔴 System: Stopped", 
                                     style='Status.TLabel')
        self.status_label.pack(pady=10)
        
        self.gpu_label = ttk.Label(status_frame, 
                                  text="🎮 GPU: RTX 4070 SUPER (12GB)", 
                                  style='Status.TLabel')
        self.gpu_label.pack()
        
        self.model_label = ttk.Label(status_frame, 
                                    text="🧠 Model: Gemma 3 (Ready)", 
                                    style='Status.TLabel')
        self.model_label.pack()
        
        self.url_label = ttk.Label(status_frame, 
                                  text="🌐 URL: http://localhost:5000", 
                                  style='Status.TLabel')
        self.url_label.pack(pady=(0, 10))
        
        # Control buttons frame
        button_frame = tk.Frame(main_frame, bg='#1a1a1a')
        button_frame.pack(pady=20)
        
        # Start button
        self.start_button = tk.Button(button_frame,
                                     text="🚀 START JUGGERNAUT AI",
                                     command=self.start_system,
                                     bg='#ff3333',
                                     fg='#ffffff',
                                     font=('Arial', 14, 'bold'),
                                     width=20,
                                     height=2)
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        # Stop button
        self.stop_button = tk.Button(button_frame,
                                    text="⏹️ STOP SYSTEM",
                                    command=self.stop_system,
                                    bg='#666666',
                                    fg='#ffffff',
                                    font=('Arial', 14, 'bold'),
                                    width=20,
                                    height=2,
                                    state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        # Open browser button
        self.browser_button = tk.Button(button_frame,
                                       text="🌐 OPEN INTERFACE",
                                       command=self.open_browser,
                                       bg='#0066cc',
                                       fg='#ffffff',
                                       font=('Arial', 14, 'bold'),
                                       width=20,
                                       height=2,
                                       state=tk.DISABLED)
        self.browser_button.pack(side=tk.LEFT, padx=10)
        
        # Log frame
        log_frame = tk.Frame(main_frame, bg='#1a1a1a')
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        log_title = ttk.Label(log_frame, 
                             text="📋 System Logs", 
                             style='Status.TLabel')
        log_title.pack(anchor=tk.W)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                 bg='#0a0a0a',
                                                 fg='#00ff00',
                                                 font=('Consolas', 9),
                                                 height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Add initial log
        self.add_log("🤖 Juggernaut AI Launcher initialized")
        self.add_log("💡 Click 'START JUGGERNAUT AI' to begin")
    
    def add_log(self, message):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_system(self):
        """Start Juggernaut AI system"""
        try:
            self.add_log("🚀 Starting Juggernaut AI system...")
            
            # Check if Python and app.py exist
            if not os.path.exists("app.py"):
                self.add_log("❌ Error: app.py not found in current directory")
                messagebox.showerror("Error", "app.py not found!\nMake sure you're running this from the Juggernaut AI directory.")
                return
            
            # Start Flask process
            self.flask_process = subprocess.Popen(
                [sys.executable, "app.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            self.is_running = True
            
            # Update UI
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="🟡 System: Starting...")
            
            # Start log monitoring
            self.start_log_monitoring()
            
            # Wait a moment then check if system is ready
            self.root.after(3000, self.check_system_ready)
            
        except Exception as e:
            self.add_log(f"❌ Error starting system: {str(e)}")
            messagebox.showerror("Error", f"Failed to start system:\n{str(e)}")
    
    def start_log_monitoring(self):
        """Monitor Flask process logs"""
        def monitor_logs():
            if self.flask_process:
                for line in iter(self.flask_process.stdout.readline, ''):
                    if line and self.is_running:
                        # Clean up log line
                        clean_line = line.strip()
                        if clean_line:
                            self.root.after(0, lambda: self.add_log(f"📡 {clean_line}"))
                    
                    if not self.is_running:
                        break
        
        log_thread = threading.Thread(target=monitor_logs, daemon=True)
        log_thread.start()
    
    def check_system_ready(self):
        """Check if system is ready and update status"""
        try:
            response = requests.get("http://localhost:5000", timeout=2)
            if response.status_code == 200:
                self.add_log("✅ System ready! Juggernaut AI is running")
                self.status_label.config(text="🟢 System: Running")
                self.browser_button.config(state=tk.NORMAL)
                
                # Auto-open browser
                self.root.after(1000, self.open_browser)
            else:
                self.root.after(2000, self.check_system_ready)
        except:
            self.root.after(2000, self.check_system_ready)
    
    def stop_system(self):
        """Stop Juggernaut AI system"""
        try:
            self.add_log("⏹️ Stopping Juggernaut AI system...")
            
            self.is_running = False
            
            if self.flask_process:
                self.flask_process.terminate()
                self.flask_process.wait(timeout=5)
                self.flask_process = None
            
            # Update UI
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.browser_button.config(state=tk.DISABLED)
            self.status_label.config(text="🔴 System: Stopped")
            
            self.add_log("✅ System stopped successfully")
            
        except Exception as e:
            self.add_log(f"❌ Error stopping system: {str(e)}")
    
    def open_browser(self):
        """Open Juggernaut AI interface in browser"""
        try:
            webbrowser.open("http://localhost:5000")
            self.add_log("🌐 Opened Juggernaut AI interface in browser")
        except Exception as e:
            self.add_log(f"❌ Error opening browser: {str(e)}")
    
    def start_status_monitoring(self):
        """Start background status monitoring"""
        def monitor_status():
            while True:
                if self.is_running:
                    try:
                        response = requests.get("http://localhost:5000/api/system/metrics", timeout=1)
                        if response.status_code == 200:
                            # System is responding
                            pass
                    except:
                        if self.is_running:
                            self.root.after(0, lambda: self.add_log("⚠️ System connection lost"))
                
                time.sleep(10)
        
        self.status_thread = threading.Thread(target=monitor_status, daemon=True)
        self.status_thread.start()
    
    def on_closing(self):
        """Handle window closing"""
        if self.is_running:
            if messagebox.askokcancel("Quit", "Juggernaut AI is still running. Stop it before closing?"):
                self.stop_system()
                time.sleep(1)
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Run the launcher"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

def main():
    """Main entry point"""
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Create and run launcher
    launcher = JuggernautLauncher()
    launcher.run()

if __name__ == "__main__":
    main()

