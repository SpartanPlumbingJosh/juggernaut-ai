"""
Juggernaut AI - Communication Manager
Email and SMS integration for remote AI interaction
"""

import smtplib
import imaplib
import email
import json
import logging
import threading
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
import requests
import os

logger = logging.getLogger(__name__)

class CommunicationManager:
    """
    Handles email and SMS communication for Juggernaut AI
    Features:
    - Email monitoring and responses
    - SMS integration via Twilio
    - Secure credential management
    - Auto-response system
    - Message threading and context
    """
    
    def __init__(self, data_path="D:\\JUGGERNAUT_DATA"):
        self.data_path = data_path
        self.config_file = os.path.join(data_path, "communication_config.json")
        self.message_log = os.path.join(data_path, "communication_log.json")
        
        # Configuration
        self.config = {
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "imap_server": "imap.gmail.com",
                "imap_port": 993,
                "email": "",
                "password": "",  # Use app password for Gmail
                "check_interval": 60  # seconds
            },
            "sms": {
                "enabled": False,
                "twilio_account_sid": "",
                "twilio_auth_token": "",
                "twilio_phone_number": "",
                "your_phone_number": ""
            },
            "security": {
                "authorized_emails": [],
                "authorized_phones": [],
                "require_authorization": True,
                "max_daily_messages": 100
            }
        }
        
        # State
        self.is_monitoring = False
        self.message_count = {"email": 0, "sms": 0}
        self.daily_reset_time = datetime.now().date()
        
        # Load configuration
        self.load_config()
        
        # Initialize services
        self.email_monitor_thread = None
        self.ai_engine = None  # Will be set by main app
        
        logger.info("📧 Communication Manager initialized")
    
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
    
    def setup_sms(self, account_sid, auth_token, twilio_number, your_number):
        """Setup SMS configuration with Twilio"""
        try:
            self.config["sms"]["twilio_account_sid"] = account_sid
            self.config["sms"]["twilio_auth_token"] = auth_token
            self.config["sms"]["twilio_phone_number"] = twilio_number
            self.config["sms"]["your_phone_number"] = your_number
            self.config["sms"]["enabled"] = True
            
            # Add to authorized phones
            if your_number not in self.config["security"]["authorized_phones"]:
                self.config["security"]["authorized_phones"].append(your_number)
            
            self.save_config()
            logger.info(f"📱 SMS configured: {your_number}")
            
            return {"success": True, "message": "SMS configured successfully"}
            
        except Exception as e:
            logger.error(f"SMS setup error: {e}")
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
                time.sleep(60)  # Wait longer on error
    
    def _check_emails(self):
        """Check for new emails"""
        try:
            # Connect to IMAP server
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
            # Fetch email
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            
            if status != "OK":
                return
            
            # Parse email
            email_message = email.message_from_bytes(msg_data[0][1])
            
            # Get sender
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
                # Generate AI response
                logger.info(f"📧 Processing email from: {sender}")
                
                ai_result = self.ai_engine.generate(message_content, f"email_{sender}")
                ai_response = ai_result["response"]
                
                # Send response
                self._send_email_response(sender, subject, ai_response, ai_result)
                
                # Log interaction
                self._log_interaction("email", sender, message_content, ai_response)
                
                self.message_count["email"] += 1
                
        except Exception as e:
            logger.error(f"Email processing error: {e}")
    
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
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.config["email"]["email"]
            msg['To'] = to_email
            msg['Subject'] = f"Re: {original_subject}" if original_subject else "Juggernaut AI Response"
            
            # Create response body
            response_body = f"""
🤖 Juggernaut AI Response

{ai_response}

---
📊 Response Details:
• Model: {ai_result.get('model', 'Unknown')}
• Response Time: {ai_result.get('response_time', 0):.2f}s
• Learning Enabled: {ai_result.get('learning_enabled', False)}
• GPU Accelerated: {ai_result.get('gpu_accelerated', False)}

💡 You can reply to this email to continue the conversation!

Powered by Juggernaut AI with RTX 4070 SUPER
            """
            
            msg.attach(MIMEText(response_body, 'plain'))
            
            # Send email
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
    
    def send_sms(self, phone_number, message):
        """Send SMS via Twilio"""
        try:
            if not self.config["sms"]["enabled"]:
                return {"success": False, "error": "SMS not configured"}
            
            # Check authorization
            if not self._is_authorized_phone(phone_number):
                return {"success": False, "error": "Unauthorized phone number"}
            
            # Check daily limits
            if not self._check_daily_limit("sms"):
                return {"success": False, "error": "Daily SMS limit reached"}
            
            # Send via Twilio
            from twilio.rest import Client
            
            client = Client(
                self.config["sms"]["twilio_account_sid"],
                self.config["sms"]["twilio_auth_token"]
            )
            
            message = client.messages.create(
                body=message,
                from_=self.config["sms"]["twilio_phone_number"],
                to=phone_number
            )
            
            self.message_count["sms"] += 1
            logger.info(f"📱 SMS sent to: {phone_number}")
            
            return {"success": True, "message_sid": message.sid}
            
        except Exception as e:
            logger.error(f"SMS send error: {e}")
            return {"success": False, "error": str(e)}
    
    def process_sms_webhook(self, request_data):
        """Process incoming SMS webhook from Twilio"""
        try:
            from_number = request_data.get('From')
            message_body = request_data.get('Body', '').strip()
            
            if not from_number or not message_body:
                return {"success": False, "error": "Invalid SMS data"}
            
            # Check authorization
            if not self._is_authorized_phone(from_number):
                logger.warning(f"📱 Unauthorized SMS from: {from_number}")
                return {"success": False, "error": "Unauthorized"}
            
            # Check daily limits
            if not self._check_daily_limit("sms"):
                logger.warning("📱 Daily SMS limit reached")
                return {"success": False, "error": "Daily limit reached"}
            
            if self.ai_engine:
                # Generate AI response
                logger.info(f"📱 Processing SMS from: {from_number}")
                
                ai_result = self.ai_engine.generate(message_body, f"sms_{from_number}")
                ai_response = ai_result["response"]
                
                # Truncate response for SMS (160 char limit)
                if len(ai_response) > 140:
                    ai_response = ai_response[:137] + "..."
                
                # Send response
                sms_result = self.send_sms(from_number, f"🤖 {ai_response}")
                
                # Log interaction
                self._log_interaction("sms", from_number, message_body, ai_response)
                
                return {"success": True, "response_sent": sms_result["success"]}
            
            return {"success": False, "error": "AI engine not available"}
            
        except Exception as e:
            logger.error(f"SMS webhook processing error: {e}")
            return {"success": False, "error": str(e)}
    
    def _is_authorized_email(self, email_address):
        """Check if email is authorized"""
        if not self.config["security"]["require_authorization"]:
            return True
        
        authorized = self.config["security"]["authorized_emails"]
        return any(auth_email.lower() in email_address.lower() for auth_email in authorized)
    
    def _is_authorized_phone(self, phone_number):
        """Check if phone number is authorized"""
        if not self.config["security"]["require_authorization"]:
            return True
        
        # Normalize phone number (remove +1, spaces, etc.)
        normalized = ''.join(filter(str.isdigit, phone_number))
        authorized = self.config["security"]["authorized_phones"]
        
        return any(''.join(filter(str.isdigit, auth_phone)) == normalized for auth_phone in authorized)
    
    def _check_daily_limit(self, message_type):
        """Check daily message limits"""
        # Reset daily count if new day
        current_date = datetime.now().date()
        if current_date != self.daily_reset_time:
            self.message_count = {"email": 0, "sms": 0}
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
                "message": message[:200],  # Truncate for privacy
                "response": response[:200],
                "success": True
            }
            
            # Load existing log
            log_data = []
            if os.path.exists(self.message_log):
                with open(self.message_log, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
            
            # Add new entry
            log_data.append(log_entry)
            
            # Keep only last 1000 entries
            if len(log_data) > 1000:
                log_data = log_data[-1000:]
            
            # Save log
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
            "monitoring_active": self.is_monitoring,
            "daily_message_count": self.message_count,
            "authorized_emails": len(self.config["security"]["authorized_emails"]),
            "authorized_phones": len(self.config["security"]["authorized_phones"]),
            "daily_limit": self.config["security"]["max_daily_messages"]
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
        logger.info("🤖 AI engine connected to communication manager")

