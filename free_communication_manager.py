"""
Juggernaut AI - FREE Communication Manager
100% Free and Open Source Communication Solutions
- Email monitoring and responses (Gmail)
- SMS via Email-to-SMS gateways (FREE)
- Discord bot integration (FREE)
- Telegram bot integration (FREE)
- Webhook endpoints for custom integrations
"""

import smtplib
import imaplib
import email
import json
import logging
import threading
import time
import requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
import os

logger = logging.getLogger(__name__)

class FreeCommunicationManager:
    """
    100% FREE Communication Manager for Juggernaut AI
    Features:
    - Gmail email monitoring and responses
    - FREE SMS via email-to-SMS gateways
    - Discord bot integration
    - Telegram bot integration
    - Custom webhook endpoints
    - No paid services required!
    """
    
    def __init__(self, data_path="D:\\JUGGERNAUT_DATA"):
        self.data_path = data_path
        self.config_file = os.path.join(data_path, "free_communication_config.json")
        self.message_log = os.path.join(data_path, "communication_log.json")
        
        # FREE SMS Gateways (Email-to-SMS)
        self.sms_gateways = {
            "verizon": "@vtext.com",
            "att": "@txt.att.net", 
            "tmobile": "@tmomail.net",
            "sprint": "@messaging.sprintpcs.com",
            "boost": "@smsmyboostmobile.com",
            "cricket": "@sms.cricketwireless.net",
            "uscellular": "@email.uscc.net",
            "metro": "@mymetropcs.com",
            "virgin": "@vmobl.com",
            "tracfone": "@mmst5.tracfone.com"
        }
        
        # Configuration
        self.config = {
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "imap_server": "imap.gmail.com", 
                "imap_port": 993,
                "email": "",
                "password": "",
                "check_interval": 60
            },
            "sms": {
                "enabled": False,
                "phone_number": "",
                "carrier": "verizon",  # Default carrier
                "use_email_gateway": True
            },
            "discord": {
                "enabled": False,
                "bot_token": "",
                "channel_id": "",
                "webhook_url": ""
            },
            "telegram": {
                "enabled": False,
                "bot_token": "",
                "chat_id": ""
            },
            "security": {
                "authorized_emails": [],
                "authorized_discord_users": [],
                "authorized_telegram_users": [],
                "require_authorization": True,
                "max_daily_messages": 100
            }
        }
        
        # State
        self.is_monitoring = False
        self.message_count = {"email": 0, "sms": 0, "discord": 0, "telegram": 0}
        self.daily_reset_time = datetime.now().date()
        
        # Load configuration
        self.load_config()
        
        # Initialize services
        self.email_monitor_thread = None
        self.ai_engine = None
        
        logger.info("📧 FREE Communication Manager initialized")
    
    def load_config(self):
        """Load communication configuration"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
                logger.info("📁 Communication config loaded")
            else:
                self.save_config()
        except Exception as e:
            logger.error(f"Config load error: {e}")
    
    def save_config(self):
        """Save communication configuration"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Config save error: {e}")
    
    def setup_email(self, email_address, password, authorized_emails=None):
        """Setup email configuration"""
        try:
            self.config["email"]["email"] = email_address
            self.config["email"]["password"] = password
            self.config["email"]["enabled"] = True
            
            if authorized_emails:
                self.config["security"]["authorized_emails"] = authorized_emails
            
            self.save_config()
            logger.info(f"📧 Email configured: {email_address}")
            
            return {"success": True, "message": "Email configured successfully"}
            
        except Exception as e:
            logger.error(f"Email setup error: {e}")
            return {"success": False, "error": str(e)}
    
    def setup_free_sms(self, phone_number, carrier):
        """Setup FREE SMS via email-to-SMS gateway"""
        try:
            if carrier not in self.sms_gateways:
                return {"success": False, "error": f"Carrier '{carrier}' not supported"}
            
            # Clean phone number (remove formatting)
            clean_number = ''.join(filter(str.isdigit, phone_number))
            if len(clean_number) == 11 and clean_number.startswith('1'):
                clean_number = clean_number[1:]  # Remove country code
            
            self.config["sms"]["phone_number"] = clean_number
            self.config["sms"]["carrier"] = carrier
            self.config["sms"]["enabled"] = True
            
            self.save_config()
            logger.info(f"📱 FREE SMS configured: {clean_number}@{self.sms_gateways[carrier]}")
            
            return {
                "success": True, 
                "message": f"FREE SMS configured for {carrier}",
                "sms_email": f"{clean_number}{self.sms_gateways[carrier]}"
            }
            
        except Exception as e:
            logger.error(f"SMS setup error: {e}")
            return {"success": False, "error": str(e)}
    
    def setup_discord(self, bot_token=None, webhook_url=None, channel_id=None):
        """Setup Discord integration (FREE)"""
        try:
            if webhook_url:
                # Webhook method (easier setup)
                self.config["discord"]["webhook_url"] = webhook_url
                self.config["discord"]["enabled"] = True
                method = "webhook"
            elif bot_token and channel_id:
                # Bot method (more features)
                self.config["discord"]["bot_token"] = bot_token
                self.config["discord"]["channel_id"] = channel_id
                self.config["discord"]["enabled"] = True
                method = "bot"
            else:
                return {"success": False, "error": "Provide either webhook_url or (bot_token + channel_id)"}
            
            self.save_config()
            logger.info(f"🎮 Discord configured using {method}")
            
            return {"success": True, "message": f"Discord configured using {method}"}
            
        except Exception as e:
            logger.error(f"Discord setup error: {e}")
            return {"success": False, "error": str(e)}
    
    def setup_telegram(self, bot_token, chat_id):
        """Setup Telegram bot integration (FREE)"""
        try:
            # Test the bot token
            test_url = f"https://api.telegram.org/bot{bot_token}/getMe"
            response = requests.get(test_url, timeout=10)
            
            if response.status_code != 200:
                return {"success": False, "error": "Invalid bot token"}
            
            self.config["telegram"]["bot_token"] = bot_token
            self.config["telegram"]["chat_id"] = chat_id
            self.config["telegram"]["enabled"] = True
            
            self.save_config()
            logger.info(f"📱 Telegram bot configured")
            
            return {"success": True, "message": "Telegram bot configured successfully"}
            
        except Exception as e:
            logger.error(f"Telegram setup error: {e}")
            return {"success": False, "error": str(e)}
    
    def send_free_sms(self, message):
        """Send FREE SMS via email-to-SMS gateway"""
        try:
            if not self.config["sms"]["enabled"]:
                return {"success": False, "error": "SMS not configured"}
            
            if not self.config["email"]["enabled"]:
                return {"success": False, "error": "Email must be configured for SMS"}
            
            phone_number = self.config["sms"]["phone_number"]
            carrier = self.config["sms"]["carrier"]
            gateway = self.sms_gateways[carrier]
            
            sms_email = f"{phone_number}{gateway}"
            
            # Create email message
            msg = MIMEText(message)
            msg['From'] = self.config["email"]["email"]
            msg['To'] = sms_email
            msg['Subject'] = ""  # Empty subject for SMS
            
            # Send via SMTP
            server = smtplib.SMTP(
                self.config["email"]["smtp_server"],
                self.config["email"]["smtp_port"]
            )
            server.starttls()
            server.login(
                self.config["email"]["email"],
                self.config["email"]["password"]
            )
            
            server.send_message(msg)
            server.quit()
            
            self.message_count["sms"] += 1
            logger.info(f"📱 FREE SMS sent to: {sms_email}")
            
            return {"success": True, "method": "email-to-sms", "gateway": carrier}
            
        except Exception as e:
            logger.error(f"FREE SMS send error: {e}")
            return {"success": False, "error": str(e)}
    
    def send_discord_message(self, message):
        """Send message to Discord (FREE)"""
        try:
            if not self.config["discord"]["enabled"]:
                return {"success": False, "error": "Discord not configured"}
            
            if self.config["discord"].get("webhook_url"):
                # Use webhook
                webhook_url = self.config["discord"]["webhook_url"]
                
                payload = {
                    "content": f"🤖 **Juggernaut AI Response**\\n{message}",
                    "username": "Juggernaut AI"
                }
                
                response = requests.post(webhook_url, json=payload, timeout=10)
                
                if response.status_code == 204:
                    self.message_count["discord"] += 1
                    logger.info("🎮 Discord message sent via webhook")
                    return {"success": True, "method": "webhook"}
                else:
                    return {"success": False, "error": f"Webhook failed: {response.status_code}"}
            
            else:
                # Use bot (would need discord.py library)
                return {"success": False, "error": "Bot method not implemented yet"}
                
        except Exception as e:
            logger.error(f"Discord send error: {e}")
            return {"success": False, "error": str(e)}
    
    def send_telegram_message(self, message):
        """Send message to Telegram (FREE)"""
        try:
            if not self.config["telegram"]["enabled"]:
                return {"success": False, "error": "Telegram not configured"}
            
            bot_token = self.config["telegram"]["bot_token"]
            chat_id = self.config["telegram"]["chat_id"]
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            
            payload = {
                "chat_id": chat_id,
                "text": f"🤖 *Juggernaut AI Response*\\n\\n{message}",
                "parse_mode": "Markdown"
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                self.message_count["telegram"] += 1
                logger.info("📱 Telegram message sent")
                return {"success": True, "method": "telegram_bot"}
            else:
                return {"success": False, "error": f"Telegram API error: {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Telegram send error: {e}")
            return {"success": False, "error": str(e)}
    
    def start_monitoring(self):
        """Start email monitoring"""
        if not self.config["email"]["enabled"]:
            logger.warning("📧 Email not configured - monitoring disabled")
            return False
        
        if self.is_monitoring:
            logger.info("📧 Email monitoring already running")
            return True
        
        try:
            self.is_monitoring = True
            self.email_monitor_thread = threading.Thread(target=self._email_monitor_worker, daemon=True)
            self.email_monitor_thread.start()
            
            logger.info("📧 Email monitoring started")
            return True
            
        except Exception as e:
            logger.error(f"Email monitoring start error: {e}")
            self.is_monitoring = False
            return False
    
    def stop_monitoring(self):
        """Stop email monitoring"""
        self.is_monitoring = False
        logger.info("📧 Email monitoring stopped")
    
    def _email_monitor_worker(self):
        """Email monitoring worker thread"""
        while self.is_monitoring:
            try:
                self._check_emails()
                time.sleep(self.config["email"]["check_interval"])
            except Exception as e:
                logger.error(f"Email monitoring error: {e}")
                time.sleep(60)
    
    def _check_emails(self):
        """Check for new emails"""
        try:
            mail = imaplib.IMAP4_SSL(
                self.config["email"]["imap_server"],
                self.config["email"]["imap_port"]
            )
            
            mail.login(
                self.config["email"]["email"],
                self.config["email"]["password"]
            )
            
            mail.select("INBOX")
            
            # Search for unread emails
            status, messages = mail.search(None, 'UNSEEN')
            
            if status == "OK" and messages[0]:
                email_ids = messages[0].split()
                
                for email_id in email_ids:
                    try:
                        self._process_email(mail, email_id)
                    except Exception as e:
                        logger.error(f"Email processing error: {e}")
            
            mail.close()
            mail.logout()
            
        except Exception as e:
            logger.error(f"Email check error: {e}")
    
    def _process_email(self, mail, email_id):
        """Process individual email"""
        try:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            
            if status != "OK":
                return
            
            email_message = email.message_from_bytes(msg_data[0][1])
            
            sender = email_message["From"]
            subject = email_message["Subject"]
            
            # Decode subject if needed
            if subject:
                decoded_subject = decode_header(subject)[0]
                if isinstance(decoded_subject[0], bytes):
                    subject = decoded_subject[0].decode(decoded_subject[1] or 'utf-8')
            
            # Check authorization
            if not self._is_authorized_email(sender):
                logger.warning(f"📧 Unauthorized email from: {sender}")
                return
            
            # Check daily limits
            if not self._check_daily_limit("email"):
                logger.warning("📧 Daily email limit reached")
                return
            
            # Extract message content
            message_content = self._extract_email_content(email_message)
            
            if message_content and self.ai_engine:
                logger.info(f"📧 Processing email from: {sender}")
                
                # Generate AI response
                ai_result = self.ai_engine.generate(message_content, f"email_{sender}")
                ai_response = ai_result["response"]
                
                # Send email response
                self._send_email_response(sender, subject, ai_response, ai_result)
                
                # Also send to other configured channels
                self._broadcast_response(ai_response, f"Email from {sender}")
                
                # Log interaction
                self._log_interaction("email", sender, message_content, ai_response)
                
                self.message_count["email"] += 1
                
        except Exception as e:
            logger.error(f"Email processing error: {e}")
    
    def _broadcast_response(self, response, context):
        """Broadcast response to all configured channels"""
        broadcast_message = f"{context}\\n\\n{response}"
        
        # Send to SMS if configured
        if self.config["sms"]["enabled"]:
            # Truncate for SMS
            sms_message = broadcast_message[:140] + "..." if len(broadcast_message) > 140 else broadcast_message
            self.send_free_sms(sms_message)
        
        # Send to Discord if configured
        if self.config["discord"]["enabled"]:
            self.send_discord_message(broadcast_message)
        
        # Send to Telegram if configured
        if self.config["telegram"]["enabled"]:
            self.send_telegram_message(broadcast_message)
    
    def _extract_email_content(self, email_message):
        """Extract text content from email"""
        try:
            content = ""
            
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            content += payload.decode('utf-8', errors='ignore')
            else:
                payload = email_message.get_payload(decode=True)
                if payload:
                    content = payload.decode('utf-8', errors='ignore')
            
            return content.strip()
            
        except Exception as e:
            logger.error(f"Email content extraction error: {e}")
            return ""
    
    def _send_email_response(self, to_email, original_subject, ai_response, ai_result):
        """Send AI response via email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config["email"]["email"]
            msg['To'] = to_email
            msg['Subject'] = f"Re: {original_subject}" if original_subject else "Juggernaut AI Response"
            
            response_body = f"""
🤖 Juggernaut AI Response

{ai_response}

---
📊 Response Details:
• Model: {ai_result.get('model', 'Unknown')}
• Response Time: {ai_result.get('response_time', 0):.2f}s
• Learning Enabled: {ai_result.get('learning_enabled', False)}
• GPU Accelerated: {ai_result.get('gpu_accelerated', False)}

💡 Reply to continue the conversation!
📱 Also available via FREE SMS, Discord, and Telegram!

Powered by Juggernaut AI with RTX 4070 SUPER
            """
            
            msg.attach(MIMEText(response_body, 'plain'))
            
            server = smtplib.SMTP(
                self.config["email"]["smtp_server"],
                self.config["email"]["smtp_port"]
            )
            server.starttls()
            server.login(
                self.config["email"]["email"],
                self.config["email"]["password"]
            )
            
            server.send_message(msg)
            server.quit()
            
            logger.info(f"📧 Response sent to: {to_email}")
            
        except Exception as e:
            logger.error(f"Email send error: {e}")
    
    def _is_authorized_email(self, email_address):
        """Check if email is authorized"""
        if not self.config["security"]["require_authorization"]:
            return True
        
        authorized = self.config["security"]["authorized_emails"]
        return any(auth_email.lower() in email_address.lower() for auth_email in authorized)
    
    def _check_daily_limit(self, message_type):
        """Check daily message limits"""
        current_date = datetime.now().date()
        if current_date != self.daily_reset_time:
            self.message_count = {"email": 0, "sms": 0, "discord": 0, "telegram": 0}
            self.daily_reset_time = current_date
        
        total_messages = sum(self.message_count.values())
        return total_messages < self.config["security"]["max_daily_messages"]
    
    def _log_interaction(self, message_type, sender, message, response):
        """Log communication interaction"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": message_type,
                "sender": sender,
                "message": message[:200],
                "response": response[:200],
                "success": True
            }
            
            log_data = []
            if os.path.exists(self.message_log):
                with open(self.message_log, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
            
            log_data.append(log_entry)
            
            if len(log_data) > 1000:
                log_data = log_data[-1000:]
            
            os.makedirs(os.path.dirname(self.message_log), exist_ok=True)
            with open(self.message_log, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Interaction logging error: {e}")
    
    def get_status(self):
        """Get communication system status"""
        return {
            "email_enabled": self.config["email"]["enabled"],
            "sms_enabled": self.config["sms"]["enabled"],
            "discord_enabled": self.config["discord"]["enabled"],
            "telegram_enabled": self.config["telegram"]["enabled"],
            "monitoring_active": self.is_monitoring,
            "daily_message_count": self.message_count,
            "sms_method": "FREE Email-to-SMS Gateway",
            "supported_carriers": list(self.sms_gateways.keys()),
            "cost": "100% FREE - No paid services!"
        }
    
    def get_communication_log(self, limit=50):
        """Get recent communication log"""
        try:
            if os.path.exists(self.message_log):
                with open(self.message_log, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                    return log_data[-limit:] if limit else log_data
            return []
        except Exception as e:
            logger.error(f"Log retrieval error: {e}")
            return []
    
    def set_ai_engine(self, ai_engine):
        """Set AI engine reference"""
        self.ai_engine = ai_engine
        logger.info("🤖 AI engine connected to FREE communication manager")
    
    def get_setup_instructions(self):
        """Get setup instructions for free services"""
        return {
            "email": {
                "title": "Gmail Setup (FREE)",
                "steps": [
                    "1. Enable 2-Factor Authentication in Gmail",
                    "2. Go to Google Account Settings → Security",
                    "3. Generate an App Password for 'Mail'",
                    "4. Use your Gmail address and the App Password"
                ]
            },
            "sms": {
                "title": "FREE SMS via Email-to-SMS Gateway",
                "steps": [
                    "1. Know your phone number and carrier",
                    "2. Configure email first (required)",
                    "3. Select your carrier from the list",
                    "4. SMS will be sent via email gateway (100% FREE!)"
                ],
                "supported_carriers": list(self.sms_gateways.keys())
            },
            "discord": {
                "title": "Discord Integration (FREE)",
                "steps": [
                    "1. Create a Discord server or use existing",
                    "2. Go to Server Settings → Integrations → Webhooks",
                    "3. Create New Webhook, copy the URL",
                    "4. Paste webhook URL in configuration"
                ]
            },
            "telegram": {
                "title": "Telegram Bot (FREE)",
                "steps": [
                    "1. Message @BotFather on Telegram",
                    "2. Send /newbot and follow instructions",
                    "3. Copy the bot token",
                    "4. Start a chat with your bot and get chat ID"
                ]
            }
        }

