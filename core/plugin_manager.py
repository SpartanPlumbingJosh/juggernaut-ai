"""
Plugin Manager Module - Handles image generation and other plugins
"""

import os
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import uuid

class PluginManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.plugins_dir = os.path.join(data_path, "plugins")
        self.images_dir = os.path.join(data_path, "images")
        self.loaded_plugins = {}
        
        # Ensure directories exist
        os.makedirs(self.plugins_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        
        # Initialize built-in plugins
        self.initialize_builtin_plugins()
    
    def initialize_builtin_plugins(self):
        """Initialize built-in plugins"""
        self.loaded_plugins["image_generator"] = {
            "name": "Image Generator",
            "version": "1.0",
            "status": "active"
        }
        
        self.loaded_plugins["file_analyzer"] = {
            "name": "File Analyzer", 
            "version": "1.0",
            "status": "active"
        }
        
        print("✅ Built-in plugins loaded")
    
    def get_plugin_count(self):
        """Get number of loaded plugins"""
        return len(self.loaded_plugins)
    
    def generate_image(self, prompt, chat_id=None):
        """Generate image from text prompt"""
        try:
            # Create image
            width, height = 512, 512
            img = Image.new('RGB', (width, height), color='black')
            draw = ImageDraw.Draw(img)
            
            # Get colors based on prompt
            colors = self.get_colors_from_prompt(prompt)
            
            # Create gradient background
            for y in range(height):
                ratio = y / height
                r = int(colors[0][0] * (1-ratio) + colors[1][0] * ratio)
                g = int(colors[0][1] * (1-ratio) + colors[1][1] * ratio)
                b = int(colors[0][2] * (1-ratio) + colors[1][2] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Add geometric shapes based on prompt
            self.add_shapes_to_image(draw, prompt, width, height)
            
            # Add text
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Add prompt as title
            title = prompt[:30] + "..." if len(prompt) > 30 else prompt
            bbox = draw.textbbox((0, 0), title, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = height - 50
            
            # Text background
            draw.rectangle([x-10, y-5, x+text_width+10, y+30], fill='black', outline='white')
            draw.text((x, y), title, fill='white', font=font)
            
            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_id = str(uuid.uuid4())[:8]
            filename = f"generated_{timestamp}_{image_id}.png"
            filepath = os.path.join(self.images_dir, filename)
            
            img.save(filepath, quality=95)
            
            # Save metadata
            metadata = {
                "id": image_id,
                "prompt": prompt,
                "filename": filename,
                "filepath": filepath,
                "chat_id": chat_id,
                "created": datetime.now().isoformat(),
                "size": f"{width}x{height}"
            }
            
            metadata_file = os.path.join(self.images_dir, f"{image_id}_metadata.json")
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            return {
                "success": True,
                "image_id": image_id,
                "filename": filename,
                "filepath": filepath,
                "prompt": prompt,
                "url": f"/api/image/{image_id}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_colors_from_prompt(self, prompt):
        """Get color palette based on prompt keywords"""
        prompt_lower = prompt.lower()
        
        # Color mappings
        if any(word in prompt_lower for word in ["sunset", "warm", "orange", "fire"]):
            return [(255, 120, 0), (255, 200, 100)]
        elif any(word in prompt_lower for word in ["ocean", "blue", "water", "sea"]):
            return [(0, 100, 200), (100, 200, 255)]
        elif any(word in prompt_lower for word in ["forest", "green", "nature", "tree"]):
            return [(0, 120, 0), (100, 200, 100)]
        elif any(word in prompt_lower for word in ["space", "galaxy", "purple", "cosmic"]):
            return [(20, 20, 50), (100, 50, 150)]
        elif any(word in prompt_lower for word in ["tech", "cyber", "neon", "digital"]):
            return [(0, 255, 255), (255, 0, 255)]
        else:
            return [(50, 50, 150), (150, 150, 255)]  # Default blue gradient
    
    def add_shapes_to_image(self, draw, prompt, width, height):
        """Add shapes based on prompt content"""
        prompt_lower = prompt.lower()
        
        if "circle" in prompt_lower or "round" in prompt_lower:
            # Add circles
            for i in range(3):
                x = width // 4 + i * width // 4
                y = height // 4 + i * height // 6
                radius = 30 + i * 20
                draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                           outline='white', width=2)
        
        elif "square" in prompt_lower or "geometric" in prompt_lower:
            # Add squares
            for i in range(3):
                x = width // 4 + i * width // 4
                y = height // 4 + i * height // 6
                size = 40 + i * 20
                draw.rectangle([x-size//2, y-size//2, x+size//2, y+size//2], 
                             outline='white', width=2)
        
        elif "line" in prompt_lower or "abstract" in prompt_lower:
            # Add abstract lines
            for i in range(5):
                x1 = i * width // 5
                y1 = height // 4
                x2 = width - i * width // 5
                y2 = 3 * height // 4
                draw.line([(x1, y1), (x2, y2)], fill='white', width=2)
    
    def get_image(self, image_id):
        """Get image by ID"""
        try:
            metadata_file = os.path.join(self.images_dir, f"{image_id}_metadata.json")
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                return metadata
            return None
            
        except Exception as e:
            print(f"Error getting image {image_id}: {e}")
            return None
    
    def list_images(self, chat_id=None):
        """List all generated images"""
        images = []
        
        try:
            for filename in os.listdir(self.images_dir):
                if filename.endswith('_metadata.json'):
                    with open(os.path.join(self.images_dir, filename), 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                        
                        if chat_id is None or metadata.get("chat_id") == chat_id:
                            images.append(metadata)
            
            # Sort by creation date
            images.sort(key=lambda x: x["created"], reverse=True)
            return images
            
        except Exception as e:
            print(f"Error listing images: {e}")
            return []
    
    def delete_image(self, image_id):
        """Delete an image"""
        try:
            metadata_file = os.path.join(self.images_dir, f"{image_id}_metadata.json")
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                # Delete image file
                if os.path.exists(metadata["filepath"]):
                    os.remove(metadata["filepath"])
                
                # Delete metadata
                os.remove(metadata_file)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Error deleting image {image_id}: {e}")
            return False

