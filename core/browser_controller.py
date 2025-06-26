"""
Browser Controller Module - Handles dual browser modes
AI browsing + User Chrome with real credentials
"""

import os
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class BrowserController:
    def __init__(self, data_path):
        self.data_path = data_path
        self.ai_browser = None
        self.user_browser = None
        self.current_mode = "ai"
        self.current_url = ""
        self.current_title = ""
        self.current_screenshot = None
        self.ready = False
        
        # Initialize browsers
        self.initialize_browsers()
    
    def initialize_browsers(self):
        """Initialize both AI and user browsers"""
        try:
            print("🌐 Initializing browsers...")
            
            # AI Browser (detected as automation)
            self.setup_ai_browser()
            
            # User Browser (uses real Chrome profile)
            self.setup_user_browser()
            
            self.ready = True
            print("✅ Browsers ready!")
            
        except Exception as e:
            print(f"❌ Browser initialization error: {e}")
            self.ready = False
    
    def setup_ai_browser(self):
        """Setup AI browser for automated tasks"""
        try:
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            
            service = Service(ChromeDriverManager().install())
            self.ai_browser = webdriver.Chrome(service=service, options=options)
            
            print("✅ AI browser ready")
            
        except Exception as e:
            print(f"❌ AI browser error: {e}")
    
    def setup_user_browser(self):
        """Setup user browser with real Chrome profile"""
        try:
            options = Options()
            
            # Use user's actual Chrome profile
            user_data_dir = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data")
            options.add_argument(f"--user-data-dir={user_data_dir}")
            options.add_argument("--profile-directory=Default")
            
            # Advanced anti-detection measures
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-features=VizDisplayCompositor")
            
            # Remove automation detection
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # User agent and window settings
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--start-maximized")
            
            # Enable remote debugging for monitoring
            options.add_argument("--remote-debugging-port=9222")
            
            # Disable notifications and popups
            prefs = {
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_settings.popups": 0,
                "profile.managed_default_content_settings.images": 1
            }
            options.add_experimental_option("prefs", prefs)
            
            service = Service(ChromeDriverManager().install())
            self.user_browser = webdriver.Chrome(service=service, options=options)
            
            # Execute scripts to hide automation indicators
            self.user_browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.user_browser.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            self.user_browser.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
            self.user_browser.execute_script("window.chrome = { runtime: {} }")
            
            print("✅ User browser ready with real profile and anti-detection")
            
        except Exception as e:
            print(f"❌ User browser error: {e}")
            print("💡 Tip: Make sure Chrome is closed before starting the interface")
    
    def is_ready(self):
        """Check if browsers are ready"""
        return self.ready
    
    def navigate(self, url, mode="ai"):
        """Navigate to URL in specified mode"""
        try:
            self.current_mode = mode
            browser = self.ai_browser if mode == "ai" else self.user_browser
            
            if not browser:
                return {"success": False, "error": f"{mode} browser not available"}
            
            browser.get(url)
            self.current_url = url
            self.current_title = browser.title
            
            # Take screenshot
            self.take_screenshot(mode)
            
            return {
                "success": True,
                "url": url,
                "title": self.current_title,
                "mode": mode,
                "screenshot": self.current_screenshot
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def take_screenshot(self, mode):
        """Take screenshot of current page"""
        try:
            browser = self.ai_browser if mode == "ai" else self.user_browser
            
            if browser:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = os.path.join(self.data_path, "screenshots", f"{mode}_{timestamp}.png")
                
                browser.save_screenshot(screenshot_path)
                self.current_screenshot = screenshot_path
                
                return screenshot_path
                
        except Exception as e:
            print(f"Screenshot error: {e}")
            return None
    
    def get_current_view(self):
        """Get current browser view data"""
        try:
            browser = self.ai_browser if self.current_mode == "ai" else self.user_browser
            
            if not browser:
                return {"error": "No browser available"}
            
            # Get page info
            page_data = {
                "url": self.current_url,
                "title": self.current_title,
                "mode": self.current_mode,
                "screenshot": self.current_screenshot,
                "page_source": browser.page_source[:1000] + "..." if len(browser.page_source) > 1000 else browser.page_source
            }
            
            return page_data
            
        except Exception as e:
            return {"error": str(e)}
    
    def execute_task(self, task_data):
        """Execute browser task (clicking, typing, etc.)"""
        try:
            mode = task_data.get("mode", "ai")
            browser = self.ai_browser if mode == "ai" else self.user_browser
            
            if not browser:
                return {"success": False, "error": f"{mode} browser not available"}
            
            task_type = task_data.get("type")
            
            if task_type == "click":
                element = browser.find_element("xpath", task_data.get("xpath"))
                element.click()
                
            elif task_type == "type":
                element = browser.find_element("xpath", task_data.get("xpath"))
                element.clear()
                element.send_keys(task_data.get("text"))
                
            elif task_type == "scroll":
                browser.execute_script("window.scrollBy(0, arguments[0]);", task_data.get("amount", 500))
            
            # Take screenshot after action
            self.take_screenshot(mode)
            
            return {
                "success": True,
                "task": task_type,
                "mode": mode,
                "screenshot": self.current_screenshot
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def read_manus_chats(self):
        """Read Manus chats automatically"""
        try:
            # Navigate to Manus
            result = self.navigate("https://manus.im/app", "user")
            
            if not result["success"]:
                return {"success": False, "error": "Failed to navigate to Manus"}
            
            # Wait for page load
            time.sleep(5)
            
            # Extract chat data with proper Manus selectors
            browser = self.user_browser
            
            chats = []
            try:
                # Wait for chat interface to load
                from selenium.webdriver.common.by import By
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                
                # Wait for chat container
                wait = WebDriverWait(browser, 10)
                
                # Try multiple possible selectors for Manus chat messages
                possible_selectors = [
                    "[data-testid='message']",
                    ".message",
                    ".chat-message", 
                    "[class*='message']",
                    "[class*='chat']",
                    ".conversation-item",
                    "[role='listitem']",
                    ".text-content"
                ]
                
                chat_elements = []
                for selector in possible_selectors:
                    try:
                        elements = browser.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            chat_elements = elements
                            print(f"✅ Found {len(elements)} messages using selector: {selector}")
                            break
                    except:
                        continue
                
                # Extract text from found elements
                for element in chat_elements:
                    try:
                        text = element.text.strip()
                        if text and len(text) > 5:  # Filter out empty or very short messages
                            chats.append({
                                "text": text,
                                "timestamp": datetime.now().isoformat(),
                                "source": "manus"
                            })
                    except:
                        continue
                
                # If no messages found, try to get page source and extract text
                if not chats:
                    page_source = browser.page_source
                    # Look for common patterns in chat applications
                    import re
                    
                    # Extract text that looks like chat messages
                    text_patterns = [
                        r'<div[^>]*class="[^"]*message[^"]*"[^>]*>(.*?)</div>',
                        r'<span[^>]*class="[^"]*text[^"]*"[^>]*>(.*?)</span>',
                        r'<p[^>]*>(.*?)</p>'
                    ]
                    
                    for pattern in text_patterns:
                        matches = re.findall(pattern, page_source, re.DOTALL | re.IGNORECASE)
                        for match in matches:
                            # Clean HTML tags
                            clean_text = re.sub(r'<[^>]+>', '', match).strip()
                            if clean_text and len(clean_text) > 10:
                                chats.append({
                                    "text": clean_text,
                                    "timestamp": datetime.now().isoformat(),
                                    "source": "manus_extracted"
                                })
                
            except Exception as e:
                print(f"Error extracting Manus chats: {e}")
            
            # Save chat data
            chat_file = os.path.join(self.data_path, "manus_chats.json")
            with open(chat_file, 'w', encoding='utf-8') as f:
                json.dump(chats, f, ensure_ascii=False, indent=2)
            
            return {
                "success": True,
                "chats_found": len(chats),
                "file_saved": chat_file,
                "message": f"Successfully extracted {len(chats)} chat messages from Manus"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def close_browsers(self):
        """Close all browsers"""
        try:
            if self.ai_browser:
                self.ai_browser.quit()
            if self.user_browser:
                self.user_browser.quit()
            print("🔒 Browsers closed")
        except Exception as e:
            print(f"Error closing browsers: {e}")

