"""
Juggernaut AI - Core Module
RTX 4070 SUPER Optimized AI System
"""

from .ai_engine import AIEngine
from .chat_manager import ChatManager
from .file_manager import FileManager
from .browser_controller import BrowserController
from .plugin_manager import PluginManager

__version__ = "1.0.0"
__author__ = "Juggernaut AI Team"

__all__ = [
    'AIEngine',
    'ChatManager', 
    'FileManager',
    'BrowserController',
    'PluginManager'
]

