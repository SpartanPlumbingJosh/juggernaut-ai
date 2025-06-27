#!/usr/bin/env python3
"""
Juggernaut AI - Desktop Launcher
Professional desktop application launcher with GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import os
import sys
import time
import webbrowser
from pathlib import Path
import json

class JuggernautLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Juggernaut AI - Desktop Launcher")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Set icon (if available)
        try:
            self.root.iconbitmap("juggernaut.ico")
        except:
            pass
        
        # Configure style
        self.setup_style()
        
        # Variables
        self.process = None
        self.is_running = False
        self.server_url = "http://localhost:5000"
        
        # Create GUI
        self.create_widgets()
        
        # Check if system is already running
        self.check_system_status()
    
    def setup_style(self):
        """Setup the GUI style"""
        style = ttk.Style()
        
        # Configure colors
        self.root.configure(bg='#1a1a1a')
        
        # Configure ttk styles
        style.theme_use('clam')
        style.configure('Title.TLabel', 
                       background='#1a1a1a', 
                       foreground='#dc2626',
                       font=('Segoe UI', 16, 'bold'))
        style.configure('Subtitle.TLabel', 
                       background='#1a1a1a', 
                       foreground='#d1d5db',
                       font=('Segoe UI', 10))
        style.configure('Status.TLabel', 
                       background='#1a1a1a', 
                       foreground='#10b981',
                       font=('Segoe UI', 9, 'bold'))
        style.configure('Red.TButton',
                       background='#dc2626',
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
    
    def create_widgets(self):
        """Create the GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="🤖 JUGGERNAUT AI", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ttk.Label(main_frame, 
                                  text="RTX 4070 SUPER Powered AI Assistant", 
                                  style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="System Status", padding=10)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_label = ttk.Label(status_frame, 
                                     text="🔴 Stopped", 
                                     style='Status.TLabel')
        self.status_label.pack()
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Start button
        self.start_button = ttk.Button(control_frame, 
                                      text="🚀 Start Juggernaut AI",
                                      command=self.start_system,
                                      style='Red.TButton')
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Stop button
        self.stop_button = ttk.Button(control_frame, 
                                     text="⏹️ Stop System",
                                     command=self.stop_system,
                                     state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Open browser button
        self.browser_button = ttk.Button(control_frame, 
                                        text="🌐 Open Interface",
                                        command=self.open_browser,
                                        state=tk.DISABLED)
        self.browser_button.pack(side=tk.LEFT)
        
        # Configuration frame
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding=10)
        config_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Model path
        ttk.Label(config_frame, text="Model Path:").pack(anchor=tk.W)
        self.model_path_var = tk.StringVar(value="D:/Juggernaut_AI/models/ai_models/text/gemma_2_9b_gguf/gemma-2-9b-it-Q4_K_M.gguf")
        model_entry = ttk.Entry(config_frame, textvariable=self.model_path_var, width=80)
        model_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Data directory
        ttk.Label(config_frame, text="Data Directory:").pack(anchor=tk.W)
        self.data_dir_var = tk.StringVar(value="D:/JUGGERNAUT_DATA")
        data_entry = ttk.Entry(config_frame, textvariable=self.data_dir_var, width=80)
        data_entry.pack(fill=tk.X, pady=(0, 10))
        
        # GPU layers
        gpu_frame = ttk.Frame(config_frame)
        gpu_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(gpu_frame, text="GPU Layers:").pack(side=tk.LEFT)
        self.gpu_layers_var = tk.StringVar(value="35")
        gpu_spinbox = ttk.Spinbox(gpu_frame, from_=0, to=50, textvariable=self.gpu_layers_var, width=10)
        gpu_spinbox.pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Label(gpu_frame, text="(RTX 4070 SUPER optimized)").pack(side=tk.LEFT, padx=(10, 0))
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="System Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, 
                                                 height=8, 
                                                 bg='#0f0f0f', 
                                                 fg='#d1d5db',
                                                 font=('Consolas', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Add initial log message
        self.log("🎯 Juggernaut AI Desktop Launcher Ready")
        self.log("📍 Interface will be available at: http://localhost:5000")
        self.log("🔧 Configure paths above and click 'Start Juggernaut AI'")
    
    def log(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def check_system_status(self):
        """Check if the system is already running"""
        try:
            import requests
            response = requests.get(self.server_url, timeout=2)
            if response.status_code == 200:
                self.is_running = True
                self.update_status("🟢 Running", "green")
                self.start_button.configure(state=tk.DISABLED)
                self.stop_button.configure(state=tk.NORMAL)
                self.browser_button.configure(state=tk.NORMAL)
                self.log("✅ Detected running Juggernaut AI system")
        except:
            pass
    
    def start_system(self):
        """Start the Juggernaut AI system"""
        if self.is_running:
            messagebox.showwarning("Warning", "System is already running!")
            return
        
        self.log("🚀 Starting Juggernaut AI System...")
        
        # Disable start button
        self.start_button.configure(state=tk.DISABLED)
        
        # Update status
        self.update_status("🟡 Starting...", "orange")
        
        # Start in separate thread
        threading.Thread(target=self._start_system_thread, daemon=True).start()
    
    def _start_system_thread(self):
        """Start system in separate thread"""
        try:
            # Get current directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Look for the integrated system file
            system_files = [
                "juggernaut_integrated.py",
                "app_final_working.py",
                "app.py"
            ]
            
            system_file = None
            for file in system_files:
                file_path = os.path.join(current_dir, file)
                if os.path.exists(file_path):
                    system_file = file_path
                    break
            
            if not system_file:
                self.log("❌ ERROR: No Juggernaut AI system file found!")
                self.log("📁 Please ensure juggernaut_integrated.py is in the same directory")
                self.start_button.configure(state=tk.NORMAL)
                self.update_status("🔴 Error", "red")
                return
            
            self.log(f"📂 Using system file: {os.path.basename(system_file)}")
            
            # Set environment variables
            env = os.environ.copy()
            env['JUGGERNAUT_MODEL_PATH'] = self.model_path_var.get()
            env['JUGGERNAUT_DATA_DIR'] = self.data_dir_var.get()
            env['JUGGERNAUT_GPU_LAYERS'] = self.gpu_layers_var.get()
            
            # Start the process
            self.process = subprocess.Popen(
                [sys.executable, system_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                env=env,
                cwd=current_dir
            )
            
            self.log("⚡ System process started")
            
            # Wait for system to be ready
            self.wait_for_system_ready()
            
        except Exception as e:
            self.log(f"❌ ERROR: Failed to start system: {e}")
            self.start_button.configure(state=tk.NORMAL)
            self.update_status("🔴 Error", "red")
    
    def wait_for_system_ready(self):
        """Wait for system to be ready"""
        max_attempts = 30
        attempt = 0
        
        while attempt < max_attempts:
            try:
                import requests
                response = requests.get(self.server_url, timeout=2)
                if response.status_code == 200:
                    self.is_running = True
                    self.update_status("🟢 Running", "green")
                    self.stop_button.configure(state=tk.NORMAL)
                    self.browser_button.configure(state=tk.NORMAL)
                    self.log("✅ Juggernaut AI System Ready!")
                    self.log(f"🌐 Interface available at: {self.server_url}")
                    
                    # Auto-open browser
                    self.root.after(2000, self.open_browser)
                    return
                    
            except:
                pass
            
            attempt += 1
            time.sleep(1)
            self.log(f"⏳ Waiting for system... ({attempt}/{max_attempts})")
        
        self.log("❌ ERROR: System failed to start within timeout")
        self.start_button.configure(state=tk.NORMAL)
        self.update_status("🔴 Timeout", "red")
    
    def stop_system(self):
        """Stop the Juggernaut AI system"""
        if not self.is_running:
            messagebox.showwarning("Warning", "System is not running!")
            return
        
        self.log("⏹️ Stopping Juggernaut AI System...")
        
        try:
            if self.process:
                self.process.terminate()
                self.process.wait(timeout=10)
                self.log("✅ System stopped successfully")
            else:
                self.log("⚠️ No process handle, system may have been started externally")
                
        except subprocess.TimeoutExpired:
            self.log("⚠️ Force killing system process...")
            self.process.kill()
            self.log("✅ System force stopped")
        except Exception as e:
            self.log(f"❌ ERROR: Failed to stop system: {e}")
        
        # Reset state
        self.is_running = False
        self.process = None
        self.update_status("🔴 Stopped", "red")
        self.start_button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)
        self.browser_button.configure(state=tk.DISABLED)
    
    def open_browser(self):
        """Open the web interface in browser"""
        if not self.is_running:
            messagebox.showwarning("Warning", "System is not running!")
            return
        
        self.log(f"🌐 Opening browser: {self.server_url}")
        webbrowser.open(self.server_url)
    
    def update_status(self, text, color):
        """Update status label"""
        self.status_label.configure(text=text)
        if color == "green":
            self.status_label.configure(foreground='#10b981')
        elif color == "orange":
            self.status_label.configure(foreground='#f59e0b')
        elif color == "red":
            self.status_label.configure(foreground='#ef4444')
    
    def on_closing(self):
        """Handle window closing"""
        if self.is_running:
            if messagebox.askokcancel("Quit", "Juggernaut AI is running. Stop the system and quit?"):
                self.stop_system()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Run the launcher"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    # Create and run launcher
    launcher = JuggernautLauncher()
    launcher.run()

