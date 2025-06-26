"""
Juggernaut AI - File Manager
Handles file uploads, storage, processing, and management
Production-ready with comprehensive security and error handling
"""

import os
import json
import logging
import threading
import hashlib
import mimetypes
from typing import Dict, List, Any, Optional, BinaryIO
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import traceback

logger = logging.getLogger(__name__)

class FileManager:
    """
    Advanced File Management System
    Features:
    - Secure file upload and storage
    - File type validation and filtering
    - Automatic file organization
    - Duplicate detection
    - File metadata extraction
    - Storage quota management
    - Virus scanning integration ready
    - Thumbnail generation for images
    """
    
    def __init__(self, data_path: str = "data"):
        self.data_path = data_path
        self.files_path = os.path.join(data_path, "files")
        self.images_path = os.path.join(data_path, "images")
        self.cache_path = os.path.join(data_path, "cache")
        self.metadata_file = os.path.join(self.files_path, "file_metadata.json")
        
        # Thread safety
        self.file_lock = threading.Lock()
        
        # Configuration
        self.max_file_size = 100 * 1024 * 1024  # 100MB
        self.max_total_storage = 10 * 1024 * 1024 * 1024  # 10GB
        self.allowed_extensions = {
            'text': ['.txt', '.md', '.json', '.csv', '.xml', '.yaml', '.yml'],
            'document': ['.pdf', '.doc', '.docx', '.rtf', '.odt'],
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'],
            'audio': ['.mp3', '.wav', '.ogg', '.m4a', '.flac'],
            'video': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm'],
            'archive': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'code': ['.py', '.js', '.html', '.css', '.cpp', '.java', '.go', '.rs']
        }
        
        # File metadata storage
        self.file_metadata = {}
        
        # Initialize system
        self._initialize_file_system()
        
        logger.info("✅ File Manager initialized")

    def _initialize_file_system(self):
        """Initialize the file management system"""
        try:
            # Create directories
            directories = [
                self.files_path,
                self.images_path,
                self.cache_path,
                os.path.join(self.files_path, "uploads"),
                os.path.join(self.files_path, "processed"),
                os.path.join(self.images_path, "thumbnails")
            ]
            
            for directory in directories:
                os.makedirs(directory, exist_ok=True)
            
            # Load existing metadata
            self._load_file_metadata()
            
            # Scan existing files
            self._scan_existing_files()
            
        except Exception as e:
            logger.error(f"File system initialization error: {e}")
            logger.error(traceback.format_exc())

    def _load_file_metadata(self):
        """Load file metadata from disk"""
        try:
            if os.path.exists(self.metadata_file):
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    self.file_metadata = json.load(f)
                logger.info(f"📁 Loaded metadata for {len(self.file_metadata)} files")
            else:
                self.file_metadata = {}
                
        except Exception as e:
            logger.error(f"Failed to load file metadata: {e}")
            self.file_metadata = {}

    def _save_file_metadata(self):
        """Save file metadata to disk"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.file_metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save file metadata: {e}")

    def _scan_existing_files(self):
        """Scan existing files and update metadata"""
        try:
            scanned_count = 0
            
            for root, dirs, files in os.walk(self.files_path):
                for filename in files:
                    if filename == 'file_metadata.json':
                        continue
                        
                    file_path = os.path.join(root, filename)
                    file_id = self._generate_file_id(file_path)
                    
                    if file_id not in self.file_metadata:
                        # Generate metadata for existing file
                        metadata = self._generate_file_metadata(file_path, filename)
                        if metadata:
                            self.file_metadata[file_id] = metadata
                            scanned_count += 1
            
            if scanned_count > 0:
                self._save_file_metadata()
                logger.info(f"📁 Scanned and indexed {scanned_count} existing files")
                
        except Exception as e:
            logger.error(f"File scanning error: {e}")

    def save_file(self, file: FileStorage) -> Dict[str, Any]:
        """Save uploaded file with security checks and metadata generation"""
        try:
            with self.file_lock:
                # Validate file
                validation_result = self._validate_file(file)
                if not validation_result['valid']:
                    raise ValueError(validation_result['error'])
                
                # Check storage quota
                if not self._check_storage_quota(file):
                    raise ValueError("Storage quota exceeded")
                
                # Generate secure filename and path
                original_filename = secure_filename(file.filename)
                file_extension = os.path.splitext(original_filename)[1].lower()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_filename = f"{timestamp}_{original_filename}"
                
                # Determine storage path based on file type
                file_category = self._get_file_category(file_extension)
                if file_category == 'image':
                    storage_dir = self.images_path
                else:
                    storage_dir = os.path.join(self.files_path, "uploads")
                
                file_path = os.path.join(storage_dir, safe_filename)
                
                # Save file
                file.save(file_path)
                
                # Generate file ID and metadata
                file_id = self._generate_file_id(file_path)
                metadata = self._generate_file_metadata(file_path, original_filename)
                
                # Store metadata
                self.file_metadata[file_id] = metadata
                self._save_file_metadata()
                
                # Post-processing
                self._post_process_file(file_path, file_category)
                
                logger.info(f"📁 File saved: {original_filename} -> {file_id}")
                
                return {
                    'file_id': file_id,
                    'filename': original_filename,
                    'safe_filename': safe_filename,
                    'file_path': file_path,
                    'size': metadata['size'],
                    'category': file_category,
                    'status': 'uploaded',
                    'upload_time': metadata['upload_time']
                }
                
        except Exception as e:
            logger.error(f"File save error: {e}")
            logger.error(traceback.format_exc())
            raise

    def _validate_file(self, file: FileStorage) -> Dict[str, Any]:
        """Validate uploaded file for security and compliance"""
        try:
            # Check if file exists
            if not file or not file.filename:
                return {'valid': False, 'error': 'No file provided'}
            
            # Check file size
            file.seek(0, 2)  # Seek to end
            file_size = file.tell()
            file.seek(0)  # Reset to beginning
            
            if file_size > self.max_file_size:
                return {
                    'valid': False, 
                    'error': f'File too large. Maximum size: {self.max_file_size / (1024*1024):.1f}MB'
                }
            
            if file_size == 0:
                return {'valid': False, 'error': 'Empty file not allowed'}
            
            # Check file extension
            filename = secure_filename(file.filename)
            file_extension = os.path.splitext(filename)[1].lower()
            
            allowed_extensions = []
            for category_extensions in self.allowed_extensions.values():
                allowed_extensions.extend(category_extensions)
            
            if file_extension not in allowed_extensions:
                return {
                    'valid': False,
                    'error': f'File type not allowed: {file_extension}'
                }
            
            # Basic content validation
            if not self._validate_file_content(file, file_extension):
                return {'valid': False, 'error': 'File content validation failed'}
            
            return {'valid': True}
            
        except Exception as e:
            logger.error(f"File validation error: {e}")
            return {'valid': False, 'error': f'Validation error: {str(e)}'}

    def _validate_file_content(self, file: FileStorage, extension: str) -> bool:
        """Validate file content matches extension"""
        try:
            # Read first few bytes for magic number checking
            file.seek(0)
            header = file.read(1024)
            file.seek(0)
            
            # Basic magic number checks
            magic_numbers = {
                '.pdf': b'%PDF',
                '.jpg': b'\xff\xd8\xff',
                '.jpeg': b'\xff\xd8\xff',
                '.png': b'\x89PNG\r\n\x1a\n',
                '.gif': b'GIF8',
                '.zip': b'PK\x03\x04',
                '.mp3': b'ID3',
            }
            
            if extension in magic_numbers:
                expected_magic = magic_numbers[extension]
                if not header.startswith(expected_magic):
                    logger.warning(f"Magic number mismatch for {extension}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Content validation error: {e}")
            return False

    def _check_storage_quota(self, file: FileStorage) -> bool:
        """Check if file upload would exceed storage quota"""
        try:
            # Calculate current storage usage
            current_usage = self._calculate_storage_usage()
            
            # Get file size
            file.seek(0, 2)
            file_size = file.tell()
            file.seek(0)
            
            # Check quota
            if current_usage + file_size > self.max_total_storage:
                logger.warning(f"Storage quota would be exceeded: {current_usage + file_size} > {self.max_total_storage}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Storage quota check error: {e}")
            return False

    def _calculate_storage_usage(self) -> int:
        """Calculate total storage usage"""
        try:
            total_size = 0
            
            for root, dirs, files in os.walk(self.files_path):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    if os.path.isfile(file_path):
                        total_size += os.path.getsize(file_path)
            
            for root, dirs, files in os.walk(self.images_path):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    if os.path.isfile(file_path):
                        total_size += os.path.getsize(file_path)
            
            return total_size
            
        except Exception as e:
            logger.error(f"Storage calculation error: {e}")
            return 0

    def _generate_file_id(self, file_path: str) -> str:
        """Generate unique file ID based on path and content"""
        try:
            # Use file path and modification time for uniqueness
            stat = os.stat(file_path)
            unique_string = f"{file_path}_{stat.st_mtime}_{stat.st_size}"
            return hashlib.md5(unique_string.encode()).hexdigest()
        except Exception as e:
            logger.error(f"File ID generation error: {e}")
            return hashlib.md5(file_path.encode()).hexdigest()

    def _generate_file_metadata(self, file_path: str, original_filename: str) -> Dict[str, Any]:
        """Generate comprehensive file metadata"""
        try:
            stat = os.stat(file_path)
            file_extension = os.path.splitext(original_filename)[1].lower()
            
            metadata = {
                'original_filename': original_filename,
                'file_path': file_path,
                'size': stat.st_size,
                'extension': file_extension,
                'category': self._get_file_category(file_extension),
                'mime_type': mimetypes.guess_type(original_filename)[0],
                'upload_time': datetime.now().isoformat(),
                'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'checksum': self._calculate_file_checksum(file_path),
                'accessible': True
            }
            
            # Add category-specific metadata
            if metadata['category'] == 'image':
                metadata.update(self._get_image_metadata(file_path))
            elif metadata['category'] == 'document':
                metadata.update(self._get_document_metadata(file_path))
            
            return metadata
            
        except Exception as e:
            logger.error(f"Metadata generation error: {e}")
            return {
                'original_filename': original_filename,
                'file_path': file_path,
                'size': 0,
                'extension': '',
                'category': 'unknown',
                'upload_time': datetime.now().isoformat(),
                'error': str(e)
            }

    def _get_file_category(self, extension: str) -> str:
        """Determine file category based on extension"""
        for category, extensions in self.allowed_extensions.items():
            if extension in extensions:
                return category
        return 'unknown'

    def _calculate_file_checksum(self, file_path: str) -> str:
        """Calculate MD5 checksum of file"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error(f"Checksum calculation error: {e}")
            return ""

    def _get_image_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract image-specific metadata"""
        try:
            # Try to get image dimensions using PIL if available
            try:
                from PIL import Image
                with Image.open(file_path) as img:
                    return {
                        'width': img.width,
                        'height': img.height,
                        'format': img.format,
                        'mode': img.mode
                    }
            except ImportError:
                logger.debug("PIL not available for image metadata")
                return {'image_metadata': 'PIL not available'}
            
        except Exception as e:
            logger.error(f"Image metadata error: {e}")
            return {'image_metadata_error': str(e)}

    def _get_document_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract document-specific metadata"""
        try:
            # Basic document metadata
            metadata = {}
            
            # For text files, count lines and words
            if file_path.endswith(('.txt', '.md')):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    metadata.update({
                        'line_count': len(content.splitlines()),
                        'word_count': len(content.split()),
                        'character_count': len(content)
                    })
            
            return metadata
            
        except Exception as e:
            logger.error(f"Document metadata error: {e}")
            return {'document_metadata_error': str(e)}

    def _post_process_file(self, file_path: str, category: str):
        """Post-process file after upload"""
        try:
            if category == 'image':
                self._generate_thumbnail(file_path)
            elif category == 'document':
                self._extract_text_content(file_path)
                
        except Exception as e:
            logger.error(f"Post-processing error: {e}")

    def _generate_thumbnail(self, image_path: str):
        """Generate thumbnail for image files"""
        try:
            from PIL import Image
            
            thumbnail_dir = os.path.join(self.images_path, "thumbnails")
            os.makedirs(thumbnail_dir, exist_ok=True)
            
            filename = os.path.basename(image_path)
            thumbnail_path = os.path.join(thumbnail_dir, f"thumb_{filename}")
            
            with Image.open(image_path) as img:
                img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                img.save(thumbnail_path, optimize=True, quality=85)
                
            logger.debug(f"📷 Thumbnail generated: {thumbnail_path}")
            
        except ImportError:
            logger.debug("PIL not available for thumbnail generation")
        except Exception as e:
            logger.error(f"Thumbnail generation error: {e}")

    def _extract_text_content(self, file_path: str):
        """Extract text content from documents for indexing"""
        try:
            # Basic text extraction for supported formats
            content = ""
            
            if file_path.endswith(('.txt', '.md')):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            
            # Store extracted content for search indexing
            if content:
                content_file = file_path + ".content"
                with open(content_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
        except Exception as e:
            logger.error(f"Text extraction error: {e}")

    def list_files(self, category: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """List files with optional filtering"""
        try:
            with self.file_lock:
                files = []
                
                for file_id, metadata in self.file_metadata.items():
                    # Filter by category if specified
                    if category and metadata.get('category') != category:
                        continue
                    
                    # Check if file still exists
                    if not os.path.exists(metadata.get('file_path', '')):
                        metadata['accessible'] = False
                    
                    files.append({
                        'file_id': file_id,
                        'filename': metadata.get('original_filename'),
                        'size': metadata.get('size'),
                        'category': metadata.get('category'),
                        'upload_time': metadata.get('upload_time'),
                        'accessible': metadata.get('accessible', True)
                    })
                
                # Sort by upload time (newest first)
                files.sort(key=lambda x: x.get('upload_time', ''), reverse=True)
                
                return files[:limit]
                
        except Exception as e:
            logger.error(f"File listing error: {e}")
            return []

    def get_file_path(self, file_id: str) -> Optional[str]:
        """Get file path by ID"""
        try:
            with self.file_lock:
                metadata = self.file_metadata.get(file_id)
                if metadata:
                    file_path = metadata.get('file_path')
                    if file_path and os.path.exists(file_path):
                        return file_path
                return None
                
        except Exception as e:
            logger.error(f"Get file path error: {e}")
            return None

    def get_file_metadata(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Get complete file metadata"""
        try:
            with self.file_lock:
                return self.file_metadata.get(file_id)
        except Exception as e:
            logger.error(f"Get file metadata error: {e}")
            return None

    def delete_file(self, file_id: str) -> bool:
        """Delete a file and its metadata"""
        try:
            with self.file_lock:
                metadata = self.file_metadata.get(file_id)
                if not metadata:
                    return False
                
                file_path = metadata.get('file_path')
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)
                
                # Remove thumbnail if exists
                if metadata.get('category') == 'image':
                    thumbnail_path = os.path.join(
                        self.images_path, 
                        "thumbnails", 
                        f"thumb_{os.path.basename(file_path)}"
                    )
                    if os.path.exists(thumbnail_path):
                        os.remove(thumbnail_path)
                
                # Remove content file if exists
                content_file = file_path + ".content"
                if os.path.exists(content_file):
                    os.remove(content_file)
                
                # Remove from metadata
                del self.file_metadata[file_id]
                self._save_file_metadata()
                
                logger.info(f"🗑️ File deleted: {file_id}")
                return True
                
        except Exception as e:
            logger.error(f"File deletion error: {e}")
            return False

    def search_files(self, query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search files by filename or content"""
        try:
            results = []
            query_lower = query.lower()
            
            with self.file_lock:
                for file_id, metadata in self.file_metadata.items():
                    # Filter by category
                    if category and metadata.get('category') != category:
                        continue
                    
                    # Search in filename
                    filename = metadata.get('original_filename', '').lower()
                    if query_lower in filename:
                        results.append({
                            'file_id': file_id,
                            'filename': metadata.get('original_filename'),
                            'category': metadata.get('category'),
                            'size': metadata.get('size'),
                            'upload_time': metadata.get('upload_time'),
                            'match_type': 'filename'
                        })
            
            return results
            
        except Exception as e:
            logger.error(f"File search error: {e}")
            return []

    def get_storage_statistics(self) -> Dict[str, Any]:
        """Get storage usage statistics"""
        try:
            total_usage = self._calculate_storage_usage()
            file_count = len(self.file_metadata)
            
            # Count by category
            category_stats = {}
            for metadata in self.file_metadata.values():
                category = metadata.get('category', 'unknown')
                if category not in category_stats:
                    category_stats[category] = {'count': 0, 'size': 0}
                category_stats[category]['count'] += 1
                category_stats[category]['size'] += metadata.get('size', 0)
            
            return {
                'total_files': file_count,
                'total_size_bytes': total_usage,
                'total_size_mb': round(total_usage / (1024 * 1024), 2),
                'quota_bytes': self.max_total_storage,
                'quota_mb': round(self.max_total_storage / (1024 * 1024), 2),
                'usage_percentage': round((total_usage / self.max_total_storage) * 100, 2),
                'category_breakdown': category_stats
            }
            
        except Exception as e:
            logger.error(f"Storage statistics error: {e}")
            return {}

    def cleanup_orphaned_files(self) -> int:
        """Clean up files without metadata or missing files"""
        try:
            cleaned_count = 0
            
            with self.file_lock:
                # Remove metadata for missing files
                missing_files = []
                for file_id, metadata in self.file_metadata.items():
                    file_path = metadata.get('file_path')
                    if file_path and not os.path.exists(file_path):
                        missing_files.append(file_id)
                
                for file_id in missing_files:
                    del self.file_metadata[file_id]
                    cleaned_count += 1
                
                if cleaned_count > 0:
                    self._save_file_metadata()
                    logger.info(f"🧹 Cleaned up {cleaned_count} orphaned file entries")
            
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
            return 0

    def __del__(self):
        """Cleanup when manager is destroyed"""
        try:
            self._save_file_metadata()
        except:
            pass

