#!/usr/bin/env python3
"""
Juggernaut AI Desktop Launcher
Professional GUI launcher for Juggernaut AI system
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import time
import os
import sys
import webbrowser
from pathlib import Path
import json
import requests

class JuggernautLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Juggernaut AI Launcher")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        # Set icon if available
        try:
            icon_path = Path(__file__).parent / "static" / "juggernaut_icon.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except:
            pass
        
        self.process = None
        self.is_running = False
        self.setup_ui()
        self.check_dependencies()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#1a1a1a')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="JUGGERNAUT AI",
            font=("Arial", 24, "bold"),
            fg='#dc2626',
            bg='#1a1a1a'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="RTX 4070 SUPER Powered AI Assistant",
            font=("Arial", 12),
            fg='#9ca3af',
            bg='#1a1a1a'
        )
        subtitle_label.pack()
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.RAISED, bd=1)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            status_frame,
            text="System Status",
            font=("Arial", 14, "bold"),
            fg='#ffffff',
            bg='#2d2d2d'
        ).pack(pady=10)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to start",
            font=("Arial", 12),
            fg='#10b981',
            bg='#2d2d2d'
        )
        self.status_label.pack(pady=(0, 10))
        
        # Control buttons frame
        control_frame = tk.Frame(main_frame, bg='#1a1a1a')
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.start_button = tk.Button(
            control_frame,
            text="START JUGGERNAUT AI",
            font=("Arial", 14, "bold"),
            fg='#ffffff',
            bg='#dc2626',
            activebackground='#b91c1c',
            activeforeground='#ffffff',
            command=self.start_system,
            height=2,
            width=20
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = tk.Button(
            control_frame,
            text="STOP",
            font=("Arial", 14, "bold"),
            fg='#ffffff',
            bg='#6b7280',
            activebackground='#4b5563',
            activeforeground='#ffffff',
            command=self.stop_system,
            height=2,
            width=10,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.open_button = tk.Button(
            control_frame,
            text="OPEN INTERFACE",
            font=("Arial", 14, "bold"),
            fg='#ffffff',
            bg='#059669',
            activebackground='#047857',
            activeforeground='#ffffff',
            command=self.open_interface,
            height=2,
            width=15,
            state=tk.DISABLED
        )
        self.open_button.pack(side=tk.LEFT)
        
        # Log frame
        log_frame = tk.Frame(main_frame, bg='#1a1a1a')
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            log_frame,
            text="System Log",
            font=("Arial", 12, "bold"),
            fg='#ffffff',
            bg='#1a1a1a'
        ).pack(anchor=tk.W)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            bg='#0f0f0f',
            fg='#ffffff',
            font=("Consolas", 10),
            height=15,
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Footer
        footer_frame = tk.Frame(main_frame, bg='#1a1a1a')
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(
            footer_frame,
            text="Access the web interface at: http://localhost:5000",
            font=("Arial", 10),
            fg='#6b7280',
            bg='#1a1a1a'
        ).pack()
        
    def check_dependencies(self):
        """Check if required files exist"""
        app_file = Path("app.py")
        if not app_file.exists():
            self.log("WARNING: app.py not found in current directory")
            self.log("Please run this launcher from the Juggernaut AI directory")
            self.start_button.config(state=tk.DISABLED)
        else:
            self.log("SUCCESS: Juggernaut AI files found")
            
    def log(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.root.update()
        
    def start_system(self):
        """Start the Juggernaut AI system"""
        if self.is_running:
            return
            
        self.log("STARTUP: Starting Juggernaut AI system...")
        self.status_label.config(text="Starting...", fg='#f59e0b')
        
        try:
            # Start the Flask app
            self.process = subprocess.Popen(
                [sys.executable, "app.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            
            # Start monitoring thread
            monitor_thread = threading.Thread(target=self.monitor_process, daemon=True)
            monitor_thread.start()
            
            # Wait a moment then check if server is ready
            self.root.after(3000, self.check_server_ready)
            
        except Exception as e:
            self.log(f"ERROR: Failed to start system: {e}")
            self.status_label.config(text="Failed to start", fg='#dc2626')
            
    def stop_system(self):
        """Stop the Juggernaut AI system"""
        if not self.is_running:
            return
            
        self.log("SHUTDOWN: Stopping Juggernaut AI system...")
        self.status_label.config(text="Stopping...", fg='#f59e0b')
        
        try:
            if self.process:
                self.process.terminate()
                self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.process.kill()
        except Exception as e:
            self.log(f"ERROR: {e}")
            
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.open_button.config(state=tk.DISABLED)
        self.status_label.config(text="Stopped", fg='#6b7280')
        self.log("SHUTDOWN: System stopped")
        
    def monitor_process(self):
        """Monitor the Flask process output"""
        if not self.process:
            return
            
        try:
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    # Clean up the line and log it
                    clean_line = line.strip()
                    if clean_line:
                        self.log(clean_line)
                        
                if self.process.poll() is not None:
                    break
                    
        except Exception as e:
            self.log(f"Monitor error: {e}")
            
        # Process ended
        if self.is_running:
            self.log("SYSTEM: Process ended unexpectedly")
            self.is_running = False
            self.root.after(0, lambda: [
                self.start_button.config(state=tk.NORMAL),
                self.stop_button.config(state=tk.DISABLED),
                self.open_button.config(state=tk.DISABLED),
                self.status_label.config(text="Stopped", fg='#dc2626')
            ])
            
    def check_server_ready(self):
        """Check if the Flask server is ready"""
        try:
            response = requests.get("http://localhost:5000", timeout=5)
            if response.status_code == 200:
                self.log("SUCCESS: Web interface is ready!")
                self.status_label.config(text="Running", fg='#10b981')
                self.open_button.config(state=tk.NORMAL)
                
                # Auto-open browser
                self.root.after(1000, self.open_interface)
            else:
                self.root.after(2000, self.check_server_ready)
        except requests.exceptions.RequestException:
            self.root.after(2000, self.check_server_ready)
        except Exception as e:
            self.log(f"Server check error: {e}")
            
    def open_interface(self):
        """Open the web interface in browser"""
        try:
            webbrowser.open("http://localhost:5000")
            self.log("BROWSER: Opening web interface...")
        except Exception as e:
            self.log(f"Browser error: {e}")
            
    def on_closing(self):
        """Handle window closing"""
        if self.is_running:
            if messagebox.askokcancel("Quit", "Juggernaut AI is still running. Stop it before closing?"):
                self.stop_system()
                self.root.after(2000, self.root.destroy)
        else:
            self.root.destroy()
            
    def run(self):
        """Run the launcher"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.log("LAUNCHER: Juggernaut AI Desktop Launcher ready")
        self.log("SYSTEM: RTX 4070 SUPER optimization enabled")
        self.log("READY: Click START to launch Juggernaut AI")
        self.root.mainloop()

if __name__ == "__main__":
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    launcher = JuggernautLauncher()
    launcher.run()

