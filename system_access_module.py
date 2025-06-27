#!/usr/bin/env python3
"""
JUGGERNAUT AI - System Access Module
Provides comprehensive system access capabilities for the AI assistant
Author: Manus AI
Date: June 27, 2025

This module enables the AI to perform file operations, system analysis,
command execution, and other system tasks safely and efficiently.
"""

import os
import sys
import json
import logging
import subprocess
import shutil
import psutil
import platform
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import mimetypes
import hashlib
# Windows-specific imports (only available on Windows)
try:
    import winreg
    WINREG_AVAILABLE = True
except ImportError:
    WINREG_AVAILABLE = False

try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False

logger = logging.getLogger(__name__)

class SystemAccessModule:
    """Comprehensive system access capabilities for Juggernaut AI"""
    
    def __init__(self):
        self.allowed_drives = ['C:', 'D:', 'E:', 'F:', 'G:', 'H:']
        self.restricted_paths = [
            'Windows/System32',
            'Program Files/Windows NT',
            'Users/*/AppData/Local/Microsoft/Windows/UsrClass.dat',
            'pagefile.sys',
            'hiberfil.sys'
        ]
        self.max_file_size = 100 * 1024 * 1024  # 100MB limit for file operations
        self.wmi_connection = None
        self.initialize_wmi()
    
    def initialize_wmi(self):
        """Initialize WMI connection for system information"""
        try:
            if WMI_AVAILABLE:
                self.wmi_connection = wmi.WMI()
                logger.info("WMI connection initialized successfully")
            else:
                logger.info("WMI not available (Windows only)")
                self.wmi_connection = None
        except Exception as e:
            logger.warning(f"Failed to initialize WMI: {e}")
            self.wmi_connection = None
    
    def is_path_allowed(self, path: str) -> bool:
        """Check if path access is allowed"""
        try:
            path = os.path.abspath(path)
            
            # Check if path is in allowed drives
            drive = os.path.splitdrive(path)[0]
            if drive not in self.allowed_drives:
                return False
            
            # Check restricted paths
            for restricted in self.restricted_paths:
                if restricted.lower() in path.lower():
                    return False
            
            return True
        except:
            return False
    
    def get_system_overview(self) -> Dict[str, Any]:
        """Get comprehensive system overview"""
        try:
            overview = {
                'timestamp': datetime.now().isoformat(),
                'system_info': self.get_system_info(),
                'hardware_info': self.get_hardware_info(),
                'drive_info': self.get_drive_info(),
                'process_info': self.get_process_summary(),
                'network_info': self.get_network_info(),
                'performance_metrics': self.get_performance_metrics()
            }
            return overview
        except Exception as e:
            logger.error(f"Error getting system overview: {e}")
            return {'error': str(e)}
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get basic system information"""
        try:
            info = {
                'platform': platform.platform(),
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'hostname': platform.node(),
                'python_version': platform.python_version(),
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat()
            }
            
            # Add Windows-specific info
            if platform.system() == 'Windows':
                try:
                    info['windows_edition'] = platform.win32_edition()
                    info['windows_version'] = platform.win32_ver()
                except:
                    pass
            
            return info
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {'error': str(e)}
    
    def get_hardware_info(self) -> Dict[str, Any]:
        """Get hardware information"""
        try:
            hardware = {
                'cpu': {
                    'physical_cores': psutil.cpu_count(logical=False),
                    'logical_cores': psutil.cpu_count(logical=True),
                    'max_frequency': psutil.cpu_freq().max if psutil.cpu_freq() else 'Unknown',
                    'current_frequency': psutil.cpu_freq().current if psutil.cpu_freq() else 'Unknown'
                },
                'memory': {
                    'total': psutil.virtual_memory().total,
                    'available': psutil.virtual_memory().available,
                    'used': psutil.virtual_memory().used,
                    'percentage': psutil.virtual_memory().percent
                },
                'swap': {
                    'total': psutil.swap_memory().total,
                    'used': psutil.swap_memory().used,
                    'free': psutil.swap_memory().free,
                    'percentage': psutil.swap_memory().percent
                }
            }
            
            # Add GPU information using WMI
            if self.wmi_connection:
                try:
                    gpus = []
                    for gpu in self.wmi_connection.Win32_VideoController():
                        if gpu.Name:
                            gpus.append({
                                'name': gpu.Name,
                                'driver_version': gpu.DriverVersion,
                                'video_memory': gpu.AdapterRAM if gpu.AdapterRAM else 'Unknown'
                            })
                    hardware['gpu'] = gpus
                except Exception as e:
                    logger.warning(f"Failed to get GPU info: {e}")
            
            return hardware
        except Exception as e:
            logger.error(f"Error getting hardware info: {e}")
            return {'error': str(e)}
    
    def get_drive_info(self) -> Dict[str, Any]:
        """Get information about all drives"""
        try:
            drives = {}
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    drives[partition.device] = {
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free,
                        'percentage': (usage.used / usage.total) * 100
                    }
                except PermissionError:
                    drives[partition.device] = {'error': 'Permission denied'}
                except Exception as e:
                    drives[partition.device] = {'error': str(e)}
            
            return drives
        except Exception as e:
            logger.error(f"Error getting drive info: {e}")
            return {'error': str(e)}
    
    def get_process_summary(self) -> Dict[str, Any]:
        """Get summary of running processes"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            
            return {
                'total_processes': len(processes),
                'top_cpu_processes': processes[:10],
                'total_cpu_usage': psutil.cpu_percent(interval=1)
            }
        except Exception as e:
            logger.error(f"Error getting process info: {e}")
            return {'error': str(e)}
    
    def get_network_info(self) -> Dict[str, Any]:
        """Get network information"""
        try:
            network = {
                'interfaces': {},
                'connections': len(psutil.net_connections()),
                'io_stats': psutil.net_io_counters()._asdict() if psutil.net_io_counters() else {}
            }
            
            # Get interface information
            for interface, addrs in psutil.net_if_addrs().items():
                network['interfaces'][interface] = []
                for addr in addrs:
                    network['interfaces'][interface].append({
                        'family': str(addr.family),
                        'address': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast
                    })
            
            return network
        except Exception as e:
            logger.error(f"Error getting network info: {e}")
            return {'error': str(e)}
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        try:
            return {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_io': psutil.disk_io_counters()._asdict() if psutil.disk_io_counters() else {},
                'network_io': psutil.net_io_counters()._asdict() if psutil.net_io_counters() else {},
                'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else 'Not available'
            }
        except Exception as e:
            logger.error(f"Error getting performance metrics: {e}")
            return {'error': str(e)}
    
    def analyze_directory(self, path: str, max_depth: int = 3, include_hidden: bool = False) -> Dict[str, Any]:
        """Analyze directory structure and contents"""
        if not self.is_path_allowed(path):
            return {'error': 'Path access not allowed'}
        
        try:
            path = Path(path)
            if not path.exists():
                return {'error': 'Path does not exist'}
            
            if not path.is_dir():
                return {'error': 'Path is not a directory'}
            
            analysis = {
                'path': str(path),
                'total_size': 0,
                'file_count': 0,
                'directory_count': 0,
                'file_types': {},
                'largest_files': [],
                'structure': {},
                'permissions': oct(path.stat().st_mode)[-3:] if hasattr(path.stat(), 'st_mode') else 'Unknown'
            }
            
            # Analyze directory contents
            for item in self._scan_directory(path, max_depth, include_hidden):
                if item['type'] == 'file':
                    analysis['file_count'] += 1
                    analysis['total_size'] += item['size']
                    
                    # Track file types
                    ext = item['extension'].lower()
                    if ext not in analysis['file_types']:
                        analysis['file_types'][ext] = {'count': 0, 'total_size': 0}
                    analysis['file_types'][ext]['count'] += 1
                    analysis['file_types'][ext]['total_size'] += item['size']
                    
                    # Track largest files
                    analysis['largest_files'].append({
                        'path': item['path'],
                        'size': item['size'],
                        'modified': item['modified']
                    })
                
                elif item['type'] == 'directory':
                    analysis['directory_count'] += 1
            
            # Sort largest files
            analysis['largest_files'].sort(key=lambda x: x['size'], reverse=True)
            analysis['largest_files'] = analysis['largest_files'][:20]  # Top 20
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing directory {path}: {e}")
            return {'error': str(e)}
    
    def _scan_directory(self, path: Path, max_depth: int, include_hidden: bool, current_depth: int = 0):
        """Recursively scan directory contents"""
        if current_depth >= max_depth:
            return
        
        try:
            for item in path.iterdir():
                if not include_hidden and item.name.startswith('.'):
                    continue
                
                try:
                    stat = item.stat()
                    item_info = {
                        'path': str(item),
                        'name': item.name,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'created': datetime.fromtimestamp(stat.st_ctime).isoformat() if hasattr(stat, 'st_ctime') else None
                    }
                    
                    if item.is_file():
                        item_info.update({
                            'type': 'file',
                            'size': stat.st_size,
                            'extension': item.suffix
                        })
                        yield item_info
                    
                    elif item.is_dir():
                        item_info.update({
                            'type': 'directory',
                            'size': 0
                        })
                        yield item_info
                        
                        # Recurse into subdirectory
                        yield from self._scan_directory(item, max_depth, include_hidden, current_depth + 1)
                
                except (PermissionError, OSError):
                    continue
                    
        except (PermissionError, OSError):
            pass
    
    def read_file_content(self, file_path: str, max_lines: int = 1000) -> Dict[str, Any]:
        """Read and analyze file content"""
        if not self.is_path_allowed(file_path):
            return {'error': 'File access not allowed'}
        
        try:
            path = Path(file_path)
            if not path.exists():
                return {'error': 'File does not exist'}
            
            if not path.is_file():
                return {'error': 'Path is not a file'}
            
            stat = path.stat()
            if stat.st_size > self.max_file_size:
                return {'error': f'File too large (max {self.max_file_size} bytes)'}
            
            # Determine file type
            mime_type, _ = mimetypes.guess_type(str(path))
            
            result = {
                'path': str(path),
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'mime_type': mime_type,
                'extension': path.suffix,
                'encoding': None,
                'content': None,
                'lines': 0,
                'is_binary': False
            }
            
            # Try to read as text
            encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
            content = None
            
            for encoding in encodings:
                try:
                    with open(path, 'r', encoding=encoding) as f:
                        lines = f.readlines()
                        if len(lines) > max_lines:
                            content = ''.join(lines[:max_lines]) + f'\n... (truncated, showing first {max_lines} lines)'
                        else:
                            content = ''.join(lines)
                        
                        result['encoding'] = encoding
                        result['content'] = content
                        result['lines'] = len(lines)
                        break
                        
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                # File is likely binary
                result['is_binary'] = True
                result['content'] = f'Binary file ({stat.st_size} bytes)'
                
                # Calculate file hash for binary files
                with open(path, 'rb') as f:
                    result['md5_hash'] = hashlib.md5(f.read()).hexdigest()
            
            return result
            
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return {'error': str(e)}
    
    def execute_command(self, command: str, working_directory: str = None, timeout: int = 30) -> Dict[str, Any]:
        """Execute system command safely"""
        try:
            # Basic command validation
            dangerous_commands = ['format', 'del', 'rm', 'rmdir', 'rd', 'shutdown', 'restart']
            command_lower = command.lower()
            
            for dangerous in dangerous_commands:
                if dangerous in command_lower:
                    return {'error': f'Command contains dangerous operation: {dangerous}'}
            
            # Set working directory
            if working_directory and not self.is_path_allowed(working_directory):
                return {'error': 'Working directory access not allowed'}
            
            # Execute command
            start_time = time.time()
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=working_directory
            )
            
            execution_time = time.time() - start_time
            
            return {
                'command': command,
                'return_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'execution_time': execution_time,
                'working_directory': working_directory or os.getcwd()
            }
            
        except subprocess.TimeoutExpired:
            return {'error': f'Command timed out after {timeout} seconds'}
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return {'error': str(e)}
    
    def search_files(self, search_path: str, pattern: str, file_type: str = None, max_results: int = 100) -> Dict[str, Any]:
        """Search for files matching pattern"""
        if not self.is_path_allowed(search_path):
            return {'error': 'Search path access not allowed'}
        
        try:
            path = Path(search_path)
            if not path.exists():
                return {'error': 'Search path does not exist'}
            
            results = []
            pattern_lower = pattern.lower()
            
            for item in path.rglob('*'):
                if len(results) >= max_results:
                    break
                
                try:
                    if item.is_file():
                        # Check file type filter
                        if file_type and not item.suffix.lower().endswith(file_type.lower()):
                            continue
                        
                        # Check pattern match
                        if pattern_lower in item.name.lower():
                            stat = item.stat()
                            results.append({
                                'path': str(item),
                                'name': item.name,
                                'size': stat.st_size,
                                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                                'extension': item.suffix
                            })
                
                except (PermissionError, OSError):
                    continue
            
            return {
                'search_path': search_path,
                'pattern': pattern,
                'file_type': file_type,
                'results_count': len(results),
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Error searching files: {e}")
            return {'error': str(e)}
    
    def get_installed_software(self) -> Dict[str, Any]:
        """Get list of installed software (Windows)"""
        try:
            software = []
            
            if platform.system() == 'Windows' and WINREG_AVAILABLE:
                # Check both 32-bit and 64-bit registry locations
                registry_paths = [
                    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall")
                ]
                
                for hkey, path in registry_paths:
                    try:
                        with winreg.OpenKey(hkey, path) as key:
                            for i in range(winreg.QueryInfoKey(key)[0]):
                                try:
                                    subkey_name = winreg.EnumKey(key, i)
                                    with winreg.OpenKey(key, subkey_name) as subkey:
                                        try:
                                            name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                            version = winreg.QueryValueEx(subkey, "DisplayVersion")[0] if "DisplayVersion" in [winreg.EnumValue(subkey, j)[0] for j in range(winreg.QueryInfoKey(subkey)[1])] else "Unknown"
                                            publisher = winreg.QueryValueEx(subkey, "Publisher")[0] if "Publisher" in [winreg.EnumValue(subkey, j)[0] for j in range(winreg.QueryInfoKey(subkey)[1])] else "Unknown"
                                            
                                            software.append({
                                                'name': name,
                                                'version': version,
                                                'publisher': publisher
                                            })
                                        except FileNotFoundError:
                                            pass
                                except OSError:
                                    pass
                    except OSError:
                        pass
            else:
                # For non-Windows systems or when winreg is not available
                software.append({
                    'name': 'Software detection not available',
                    'version': 'N/A',
                    'publisher': 'Windows registry access required'
                })
            
            # Remove duplicates
            unique_software = []
            seen = set()
            for item in software:
                key = (item['name'], item['version'])
                if key not in seen:
                    seen.add(key)
                    unique_software.append(item)
            
            return {
                'total_count': len(unique_software),
                'software': sorted(unique_software, key=lambda x: x['name'].lower())
            }
            
        except Exception as e:
            logger.error(f"Error getting installed software: {e}")
            return {'error': str(e)}
    
    def create_system_report(self) -> Dict[str, Any]:
        """Create comprehensive system report"""
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'report_type': 'comprehensive_system_analysis',
                'system_overview': self.get_system_overview(),
                'installed_software': self.get_installed_software(),
                'drive_analysis': {}
            }
            
            # Analyze each drive
            for drive in ['C:', 'D:', 'E:', 'F:']:
                if os.path.exists(drive + '\\'):
                    report['drive_analysis'][drive] = self.analyze_directory(
                        drive + '\\', 
                        max_depth=2, 
                        include_hidden=False
                    )
            
            return report
            
        except Exception as e:
            logger.error(f"Error creating system report: {e}")
            return {'error': str(e)}

# Global instance
system_access = SystemAccessModule()

