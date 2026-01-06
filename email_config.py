# """
# Email Configuration Module for Multi-Crop Disease Detection System
# Handles both EmailJS (optional) and SMTP (primary) email delivery
# """

# import os
# import sys
# import json
# import smtplib
# import logging
# from datetime import datetime
# from typing import Dict, List, Optional, Tuple, Any
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.application import MIMEApplication
# from dotenv import load_dotenv

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('logs/email.log'),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger(__name__)

# # Load environment variables
# load_dotenv()

# class EmailConfig:
#     """Email configuration and sending class"""
    
#     def __init__(self):
#         """Initialize email configuration from environment variables"""
        
#         # EmailJS Configuration (Optional - for client-side email)
#         self.emailjs_service_id = os.getenv('EMAILJS_SERVICE_ID', '')
#         self.emailjs_template_id = os.getenv('EMAILJS_TEMPLATE_ID', '')
#         self.emailjs_user_id = os.getenv('EMAILJS_PUBLIC_KEY', '')
        
#         # SMTP Configuration (Primary - using Gmail)
#         self.smtp_user = os.getenv('GMAIL_USER', 'dokkaridileep02@gmail.com')
#         self.smtp_password = os.getenv('GMAIL_APP_PASSWORD', 'wgzkkqojfyumuvbw')
#         self.admin_email = os.getenv('ADMIN_EMAIL', 'dokkaridileep02@gmail.com')
#         self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
#         self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        
#         # Application Configuration
#         self.app_name = "AgriDetect"
#         self.app_url = os.getenv('APP_URL', 'http://localhost:5000')
        
#         # Validate configuration on initialization
#         self.validate_config()
        
#         # Create logs directory if it doesn't exist
#         if not os.path.exists('logs'):
#             os.makedirs('logs')
    
#     def validate_config(self) -> Tuple[bool, List[str]]:
#         """Validate email configuration and return (is_valid, errors)"""
#         errors = []
        
#         # Check SMTP configuration (required)
#         if not self.smtp_user:
#             errors.append("GMAIL_USER is not configured")
#         if not self.smtp_password:
#             errors.append("GMAIL_APP_PASSWORD is not configured")
#         if not self.admin_email:
#             errors.append("ADMIN_EMAIL is not configured")
        
#         # Check if SMTP user is a Gmail address
#         if self.smtp_user and 'gmail.com' not in self.smtp_user.lower():
#             errors.append("SMTP_USER must be a Gmail address for Gmail SMTP")
        
#         # Check EmailJS configuration (optional, but warn if partially configured)
#         emailjs_configs = [self.emailjs_service_id, self.emailjs_template_id, self.emailjs_user_id]
#         if any(emailjs_configs) and not all(emailjs_configs):
#             logger.warning("EmailJS is partially configured. All EmailJS variables must be set to use EmailJS.")
        
#         is_valid = len(errors) == 0
        
#         if is_valid:
#             logger.info("✅ Email configuration validated successfully")
#             logger.info(f"📧 Admin email: {self.admin_email}")
#             logger.info(f"📤 SMTP user: {self.smtp_user}")
#             if all(emailjs_configs):
#                 logger.info("✅ EmailJS configured for client-side email")
#         else:
#             logger.error("❌ Email configuration validation failed:")
#             for error in errors:
#                 logger.error(f"   - {error}")
        
#         return is_valid, errors
    
#     def test_smtp_connection(self) -> Tuple[bool, str]:
#         """Test SMTP connection and return (success, message)"""
#         try:
#             logger.info(f"🔧 Testing SMTP connection to {self.smtp_server}:{self.smtp_port}")
            
#             # Connect to server
#             server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10)
#             server.set_debuglevel(0)
            
#             # Start TLS
#             server.starttls()
            
#             # Login
#             server.login(self.smtp_user, self.smtp_password)
            
#             # Quit
#             server.quit()
            
#             message = f"✅ SMTP connection successful to {self.smtp_server}"
#             logger.info(message)
#             return True, message
            
#         except smtplib.SMTPAuthenticationError:
#             message = "❌ SMTP Authentication failed. Check your Gmail credentials and App Password."
#             logger.error(message)
#             return False, message
            
#         except Exception as e:
#             message = f"❌ SMTP connection failed: {str(e)}"
#             logger.error(message)
#             return False, message
    
#     def create_feedback_email_html(self, feedback_data: Dict[str, Any]) -> str:
#         """Create HTML email content for feedback"""
        
#         # Format timestamp
#         timestamp = feedback_data.get('timestamp', datetime.now().isoformat())
#         if isinstance(timestamp, str):
#             try:
#                 dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
#                 formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
#             except:
#                 formatted_time = timestamp
#         else:
#             formatted_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
#         # Get rating stars
#         rating = feedback_data.get('rating', 'Not rated')
#         if rating.isdigit():
#             stars = '★' * int(rating) + '☆' * (5 - int(rating))
#             rating_display = f"{rating}/5 ({stars})"
#         else:
#             rating_display = "Not rated"
        
#         # Create HTML content
#         html = f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <title>New Feedback Received</title>
#             <style>
#                 body {{
#                     font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#                     line-height: 1.6;
#                     color: #333;
#                     margin: 0;
#                     padding: 0;
#                     background-color: #f5f7fa;
#                 }}
#                 .container {{
#                     max-width: 600px;
#                     margin: 20px auto;
#                     background: white;
#                     border-radius: 10px;
#                     overflow: hidden;
#                     box-shadow: 0 4px 20px rgba(0,0,0,0.1);
#                 }}
#                 .header {{
#                     background: linear-gradient(135deg, #2e7d32, #1b5e20);
#                     color: white;
#                     padding: 30px 20px;
#                     text-align: center;
#                 }}
#                 .header h1 {{
#                     margin: 0;
#                     font-size: 24px;
#                     display: flex;
#                     align-items: center;
#                     justify-content: center;
#                     gap: 10px;
#                 }}
#                 .content {{
#                     padding: 30px;
#                 }}
#                 .feedback-info {{
#                     background: #f8f9fa;
#                     border-radius: 8px;
#                     padding: 20px;
#                     margin-bottom: 25px;
#                 }}
#                 .info-grid {{
#                     display: grid;
#                     grid-template-columns: 1fr 1fr;
#                     gap: 15px;
#                     margin-bottom: 20px;
#                 }}
#                 .info-item {{
#                     margin-bottom: 10px;
#                 }}
#                 .info-label {{
#                     font-weight: 600;
#                     color: #495057;
#                     font-size: 14px;
#                     margin-bottom: 5px;
#                 }}
#                 .info-value {{
#                     color: #212529;
#                     font-size: 15px;
#                 }}
#                 .message-box {{
#                     background: white;
#                     border: 1px solid #e9ecef;
#                     border-radius: 8px;
#                     padding: 20px;
#                     margin-top: 20px;
#                 }}
#                 .message-box h3 {{
#                     color: #1b5e20;
#                     margin-top: 0;
#                     display: flex;
#                     align-items: center;
#                     gap: 10px;
#                 }}
#                 .message-content {{
#                     white-space: pre-line;
#                     line-height: 1.7;
#                     color: #495057;
#                 }}
#                 .rating-stars {{
#                     color: #ffc107;
#                     font-size: 18px;
#                     letter-spacing: 2px;
#                 }}
#                 .footer {{
#                     background: #f8f9fa;
#                     padding: 20px;
#                     text-align: center;
#                     border-top: 1px solid #e9ecef;
#                     color: #6c757d;
#                     font-size: 12px;
#                 }}
#                 .badge {{
#                     display: inline-block;
#                     padding: 4px 12px;
#                     border-radius: 20px;
#                     font-size: 12px;
#                     font-weight: 600;
#                 }}
#                 .badge-bug {{ background: #f8d7da; color: #721c24; }}
#                 .badge-feature {{ background: #d1ecf1; color: #0c5460; }}
#                 .badge-improvement {{ background: #d4edda; color: #155724; }}
#                 .badge-accuracy {{ background: #fff3cd; color: #856404; }}
#                 .badge-other {{ background: #e2e3e5; color: #383d41; }}
#             </style>
#         </head>
#         <body>
#             <div class="container">
#                 <div class="header">
#                     <h1>
#                         <span style="font-size: 28px;">📬</span>
#                         New Feedback Received
#                     </h1>
#                     <p>AgriDetect Feedback System</p>
#                 </div>
                
#                 <div class="content">
#                     <div class="feedback-info">
#                         <div class="info-grid">
#                             <div class="info-item">
#                                 <div class="info-label">👤 Name</div>
#                                 <div class="info-value">{feedback_data.get('name', 'Not provided')}</div>
#                             </div>
#                             <div class="info-item">
#                                 <div class="info-label">📧 Email</div>
#                                 <div class="info-value">{feedback_data.get('email', 'Not provided')}</div>
#                             </div>
#                             <div class="info-item">
#                                 <div class="info-label">📞 Contact</div>
#                                 <div class="info-value">{feedback_data.get('contact', 'Not provided')}</div>
#                             </div>
#                             <div class="info-item">
#                                 <div class="info-label">📅 Date & Time</div>
#                                 <div class="info-value">{formatted_time}</div>
#                             </div>
#                             <div class="info-item">
#                                 <div class="info-label">🏷️ Feedback Type</div>
#                                 <div class="info-value">
#                                     <span class="badge badge-{feedback_data.get('category', 'other')}">
#                                         {feedback_data.get('category', 'other').upper()}
#                                     </span>
#                                 </div>
#                             </div>
#                             <div class="info-item">
#                                 <div class="info-label">⭐ Rating</div>
#                                 <div class="info-value">
#                                     <span class="rating-stars">{rating_display}</span>
#                                 </div>
#                             </div>
#                         </div>
                        
#                         <div class="info-item">
#                             <div class="info-label">📝 Subject</div>
#                             <div class="info-value" style="font-size: 16px; font-weight: 500; color: #1b5e20;">
#                                 {feedback_data.get('subject', 'No subject')}
#                             </div>
#                         </div>
#                     </div>
                    
#                     <div class="message-box">
#                         <h3><span>💬</span> Message</h3>
#                         <div class="message-content">
#                             {feedback_data.get('message', 'No message provided').replace('\n', '<br>')}
#                         </div>
#                     </div>
                    
#                     <div style="margin-top: 25px; padding: 15px; background: #e8f5e9; border-radius: 8px;">
#                         <div class="info-item">
#                             <div class="info-label">📰 Subscription Preference</div>
#                             <div class="info-value">
#                                 <strong>{'✅ Subscribed to updates' if feedback_data.get('subscribe') else '❌ Not subscribed to updates'}</strong>
#                             </div>
#                         </div>
#                     </div>
#                 </div>
                
#                 <div class="footer">
#                     <p>
#                         This feedback was submitted via {self.app_name} Feedback System.<br>
#                         <a href="{self.app_url}" style="color: #2e7d32; text-decoration: none;">{self.app_url}</a>
#                     </p>
#                     <p style="margin-top: 10px; font-size: 11px;">
#                         © {datetime.now().year} {self.app_name}. This is an automated message.
#                     </p>
#                 </div>
#             </div>
#         </body>
#         </html>
      

#         """
#         return html
    
#     def create_feedback_email_text(self, feedback_data: Dict[str, Any]) -> str:
#         """Create plain text email content for feedback"""
        
#         timestamp = feedback_data.get('timestamp', datetime.now().isoformat())
#         if isinstance(timestamp, str):
#             try:
#                 dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
#                 formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
#             except:
#                 formatted_time = timestamp
#         else:
#             formatted_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
#         text = f"""
# NEW FEEDBACK RECEIVED
# =====================

# System: {self.app_name}
# Time: {formatted_time}

# USER INFORMATION:
# -----------------
# Name: {feedback_data.get('name', 'Not provided')}
# Email: {feedback_data.get('email', 'Not provided')}
# Contact: {feedback_data.get('contact', 'Not provided')}

# FEEDBACK DETAILS:
# -----------------
# Type: {feedback_data.get('category', 'Not specified')}
# Rating: {feedback_data.get('rating', 'Not rated')}/5
# Subject: {feedback_data.get('subject', 'No subject')}

# MESSAGE:
# --------
# {feedback_data.get('message', 'No message provided')}

# ADDITIONAL INFO:
# ----------------
# Subscribe to updates: {'Yes' if feedback_data.get('subscribe') else 'No'}
# Reference ID: {feedback_data.get('reference_id', 'N/A')}

# ---
# This feedback was submitted via {self.app_name} Feedback System.
# Automated message - © {datetime.now().year} {self.app_name}
# """
        
#         return text
    
#     def send_feedback_email(self, feedback_data: Dict[str, Any]) -> Tuple[bool, str, Optional[str]]:
#         """
#         Send feedback email via SMTP
        
#         Returns:
#             Tuple[bool, str, Optional[str]]: 
#                 (success, message, reference_id)
#         """
        
#         # Generate reference ID
#         ref_id = feedback_data.get('reference_id', 
#                                   f"FB-{datetime.now().strftime('%Y%m%d')}-{int(datetime.now().timestamp() % 10000):04d}")
        
#         try:
#             # Validate configuration
#             is_valid, errors = self.validate_config()
#             if not is_valid:
#                 return False, f"Configuration error: {', '.join(errors)}", ref_id
            
#             # Create email message
#             msg = MIMEMultipart('alternative')
#             msg['From'] = f"{self.app_name} <{self.smtp_user}>"
#             msg['To'] = self.admin_email
#             msg['Subject'] = f"[{self.app_name}] New Feedback: {feedback_data.get('subject', 'No Subject')}"
#             msg['X-Priority'] = '3'  # Normal priority
            
#             # Add headers for better tracking
#             msg['X-Feedback-ID'] = ref_id
#             msg['X-Feedback-Type'] = feedback_data.get('category', 'unknown')
            
#             # Create email content
#             text_content = self.create_feedback_email_text(feedback_data)
#             html_content = self.create_feedback_email_html(feedback_data)
            
#             # Attach both versions
#             msg.attach(MIMEText(text_content, 'plain'))
#             msg.attach(MIMEText(html_content, 'html'))
            
#             # Connect to SMTP server and send
#             logger.info(f"📧 Sending feedback email to {self.admin_email} (Ref: {ref_id})")
            
#             server = smtplib.SMTP(self.smtp_server, self.smtp_port)
#             server.starttls()
#             server.login(self.smtp_user, self.smtp_password)
#             server.send_message(msg)
#             server.quit()
            
#             success_message = f"Feedback email sent successfully to {self.admin_email} (Ref: {ref_id})"
#             logger.info(f"✅ {success_message}")
            
#             return True, success_message, ref_id
            
#         except smtplib.SMTPAuthenticationError as e:
#             error_message = f"SMTP Authentication failed: {str(e)}"
#             logger.error(f"❌ {error_message}")
#             return False, error_message, ref_id
            
#         except Exception as e:
#             error_message = f"Failed to send email: {str(e)}"
#             logger.error(f"❌ {error_message}")
#             return False, error_message, ref_id
    
#     def log_feedback(self, feedback_data: Dict[str, Any]) -> Tuple[bool, str]:
#         """Log feedback to JSON file"""
#         try:
#             log_file = 'logs/feedback_log.json'
            
#             # Read existing feedback
#             if os.path.exists(log_file):
#                 with open(log_file, 'r') as f:
#                     try:
#                         existing_data = json.load(f)
#                     except json.JSONDecodeError:
#                         existing_data = []
#             else:
#                 existing_data = []
            
#             # Add timestamp and reference ID if not present
#             if 'timestamp' not in feedback_data:
#                 feedback_data['timestamp'] = datetime.now().isoformat()
            
#             if 'reference_id' not in feedback_data:
#                 feedback_data['reference_id'] = f"FB-{datetime.now().strftime('%Y%m%d')}-{len(existing_data) + 1:04d}"
            
#             # Add to existing data
#             existing_data.append(feedback_data)
            
#             # Save to file
#             with open(log_file, 'w') as f:
#                 json.dump(existing_data, f, indent=2, default=str)
            
#             logger.info(f"📝 Feedback logged successfully (Ref: {feedback_data['reference_id']})")
#             return True, f"Feedback logged successfully (Ref: {feedback_data['reference_id']})"
            
#         except Exception as e:
#             error_message = f"Failed to log feedback: {str(e)}"
#             logger.error(f"❌ {error_message}")
#             return False, error_message
    
#     def get_feedback_stats(self) -> Dict[str, Any]:
#         """Get feedback statistics"""
#         try:
#             log_file = 'logs/feedback_log.json'
            
#             if not os.path.exists(log_file):
#                 return {
#                     'total': 0,
#                     'by_type': {},
#                     'by_rating': {},
#                     'recent': []
#                 }
            
#             with open(log_file, 'r') as f:
#                 feedback_data = json.load(f)
            
#             # Calculate statistics
#             total = len(feedback_data)
            
#             by_type = {}
#             by_rating = {}
            
#             for entry in feedback_data:
#                 # Count by type
#                 fb_type = entry.get('category', 'other')
#                 by_type[fb_type] = by_type.get(fb_type, 0) + 1
                
#                 # Count by rating
#                 rating = entry.get('rating', 'Not rated')
#                 by_rating[rating] = by_rating.get(rating, 0) + 1
            
#             # Get recent feedback (last 5)
#             recent = feedback_data[-5:] if total > 5 else feedback_data
#             recent = list(reversed(recent))  # Show newest first
            
#             return {
#                 'total': total,
#                 'by_type': by_type,
#                 'by_rating': by_rating,
#                 'recent': recent
#             }
            
#         except Exception as e:
#             logger.error(f"Error getting feedback stats: {str(e)}")
#             return {
#                 'total': 0,
#                 'by_type': {},
#                 'by_rating': {},
#                 'recent': []
#             }

# # Create global instance
# email_config = EmailConfig()

# # Convenience functions
# def send_feedback(feedback_data: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     Send feedback email and log it
    
#     Returns:
#         Dict with keys: success, message, reference_id
#     """
#     # Log feedback first
#     log_success, log_message = email_config.log_feedback(feedback_data)
    
#     # Send email
#     email_success, email_message, ref_id = email_config.send_feedback_email(feedback_data)
    
#     # Use reference ID from logging if email sending failed
#     if not ref_id and log_success:
#         ref_id = feedback_data.get('reference_id', 'N/A')
    
#     return {
#         'success': email_success and log_success,
#         'message': f"{email_message} | {log_message}",
#         'reference_id': ref_id,
#         'email_sent': email_success,
#         'logged': log_success
#     }

# def test_email_system() -> Dict[str, Any]:
#     """Test the entire email system"""
#     test_data = {
#         'name': 'System Test',
#         'email': 'test@system.com',
#         'contact': 'Test Contact',
#         'category': 'test',
#         'subject': 'System Test Email',
#         'message': 'This is an automated test of the email system.',
#         'rating': '5',
#         'subscribe': True
#     }
    
#     logger.info("🔧 Running email system test...")
    
#     # Test configuration
#     config_valid, config_errors = email_config.validate_config()
    
#     # Test SMTP connection
#     smtp_success, smtp_message = email_config.test_smtp_connection()
    
#     # Test sending email
#     result = send_feedback(test_data)
    
#     # Get feedback stats
#     stats = email_config.get_feedback_stats()
    
#     return {
#         'config_valid': config_valid,
#         'config_errors': config_errors,
#         'smtp_test': {
#             'success': smtp_success,
#             'message': smtp_message
#         },
#         'email_test': result,
#         'stats': stats,
#         'timestamp': datetime.now().isoformat()
#     }

# if __name__ == '__main__':
#     """Run email system test when executed directly"""
#     print("="*60)
#     print("🔧 Email Configuration Module Test")
#     print("="*60)
    
#     # Test the system
#     result = test_email_system()
    
#     print(f"\n📋 Configuration: {'✅ Valid' if result['config_valid'] else '❌ Invalid'}")
#     if result['config_errors']:
#         print("   Errors:", ", ".join(result['config_errors']))
    
#     print(f"\n📡 SMTP Connection: {'✅ Success' if result['smtp_test']['success'] else '❌ Failed'}")
#     print(f"   Message: {result['smtp_test']['message']}")
    
#     print(f"\n📧 Email Test: {'✅ Success' if result['email_test']['success'] else '❌ Failed'}")
#     print(f"   Message: {result['email_test']['message']}")
#     print(f"   Reference ID: {result['email_test']['reference_id']}")
    
#     print(f"\n📊 Feedback Statistics:")
#     print(f"   Total Feedback: {result['stats']['total']}")
    
#     print("\n" + "="*60)
    
#     if all([result['config_valid'], result['smtp_test']['success'], result['email_test']['success']]):
#         print("🎉 ALL TESTS PASSED! Email system is ready.")
#         sys.exit(0)
#     else:
#         print("⚠️ Some tests failed. Check the logs for details.")
#         sys.exit(1)














"""
Email Configuration Module for Multi-Crop Disease Detection System
Handles both EmailJS (optional) and SMTP (primary) email delivery
"""

import os
import sys
import json
import smtplib
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/email.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class EmailConfig:
    """Email configuration and sending class"""
    
    def __init__(self):
        """Initialize email configuration from environment variables"""
        
        # EmailJS Configuration (Optional - for client-side email)
        self.emailjs_service_id = os.getenv('EMAILJS_SERVICE_ID', '')
        self.emailjs_template_id = os.getenv('EMAILJS_TEMPLATE_ID', '')
        self.emailjs_user_id = os.getenv('EMAILJS_PUBLIC_KEY', '')
        
        # SMTP Configuration (Primary - using Gmail)
        self.smtp_user = os.getenv('GMAIL_USER', 'dokkaridileep02@gmail.com')
        self.smtp_password = os.getenv('GMAIL_APP_PASSWORD', 'wtgnntcqksxsipdb')
        self.admin_email = os.getenv('ADMIN_EMAIL', 'dokkaridileep02@gmail.com')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        
        # Application Configuration
        self.app_name = "AgriDetect"
        self.app_url = os.getenv('APP_URL', 'http://localhost:5000')
        
        # Validate configuration on initialization
        self.validate_config()
        
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
    
    def validate_config(self) -> Tuple[bool, List[str]]:
        """Validate email configuration and return (is_valid, errors)"""
        errors = []
        
        # Check SMTP configuration (required)
        if not self.smtp_user:
            errors.append("GMAIL_USER is not configured")
        if not self.smtp_password:
            errors.append("GMAIL_APP_PASSWORD is not configured")
        if not self.admin_email:
            errors.append("ADMIN_EMAIL is not configured")
        
        # Check if SMTP user is a Gmail address
        if self.smtp_user and 'gmail.com' not in self.smtp_user.lower():
            errors.append("SMTP_USER must be a Gmail address for Gmail SMTP")
        
        # Check EmailJS configuration (optional, but warn if partially configured)
        emailjs_configs = [self.emailjs_service_id, self.emailjs_template_id, self.emailjs_user_id]
        if any(emailjs_configs) and not all(emailjs_configs):
            logger.warning("EmailJS is partially configured. All EmailJS variables must be set to use EmailJS.")
        
        is_valid = len(errors) == 0
        
        if is_valid:
            logger.info("Email configuration validated successfully")
            logger.info(f"Admin email: {self.admin_email}")
            logger.info(f"SMTP user: {self.smtp_user}")
            if all(emailjs_configs):
                logger.info("EmailJS configured for client-side email")
        else:
            logger.error("Email configuration validation failed:")
            for error in errors:
                logger.error(f"   - {error}")
        
        return is_valid, errors
    
    def test_smtp_connection(self) -> Tuple[bool, str]:
        """Test SMTP connection and return (success, message)"""
        try:
            logger.info(f"Testing SMTP connection to {self.smtp_server}:{self.smtp_port}")
            
            # Connect to server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10)
            server.set_debuglevel(0)
            
            # Start TLS
            server.starttls()
            
            # Login
            server.login(self.smtp_user, self.smtp_password)
            
            # Quit
            server.quit()
            
            message = f"SMTP connection successful to {self.smtp_server}"
            logger.info(message)
            return True, message
            
        except smtplib.SMTPAuthenticationError:
            message = "SMTP Authentication failed. Check your Gmail credentials and App Password."
            logger.error(message)
            return False, message
            
        except Exception as e:
            message = f"SMTP connection failed: {str(e)}"
            logger.error(message)
            return False, message
    
    def create_feedback_email_html(self, feedback_data: Dict[str, Any]) -> str:
        """Create HTML email content for feedback"""
        
        # Format timestamp
        timestamp = feedback_data.get('timestamp', datetime.now().isoformat())
        if isinstance(timestamp, str):
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                formatted_time = timestamp
        else:
            formatted_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Get rating stars
        rating = feedback_data.get('rating', 'Not rated')
        if rating.isdigit():
            stars = '★' * int(rating) + '☆' * (5 - int(rating))
            rating_display = f"{rating}/5 ({stars})"
        else:
            rating_display = "Not rated"
        
        # Get feedback type for badge class
        feedback_type = feedback_data.get('category', 'other')
        badge_class_map = {
            'bug': 'badge-bug',
            'feature': 'badge-feature',
            'improvement': 'badge-improvement',
            'accuracy': 'badge-accuracy',
            'usability': 'badge-accuracy',
            'other': 'badge-other'
        }
        badge_class = badge_class_map.get(feedback_type, 'badge-other')
        
        # Get message and replace newlines with <br> tags
        message = feedback_data.get('message', 'No message provided')
        message_with_br = message.replace('\n', '<br>')
        
        # Create HTML content without backslashes in f-string
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Feedback Received</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: #f5f7fa;
        }}
        .container {{
            max-width: 600px;
            margin: 20px auto;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #2e7d32, #1b5e20);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }}
        .content {{
            padding: 30px;
        }}
        .feedback-info {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 25px;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }}
        .info-item {{
            margin-bottom: 10px;
        }}
        .info-label {{
            font-weight: 600;
            color: #495057;
            font-size: 14px;
            margin-bottom: 5px;
        }}
        .info-value {{
            color: #212529;
            font-size: 15px;
        }}
        .message-box {{
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
        }}
        .message-box h3 {{
            color: #1b5e20;
            margin-top: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .message-content {{
            white-space: pre-line;
            line-height: 1.7;
            color: #495057;
        }}
        .rating-stars {{
            color: #ffc107;
            font-size: 18px;
            letter-spacing: 2px;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            border-top: 1px solid #e9ecef;
            color: #6c757d;
            font-size: 12px;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }}
        .badge-bug {{ background: #f8d7da; color: #721c24; }}
        .badge-feature {{ background: #d1ecf1; color: #0c5460; }}
        .badge-improvement {{ background: #d4edda; color: #155724; }}
        .badge-accuracy {{ background: #fff3cd; color: #856404; }}
        .badge-usability {{ background: #e2e3e5; color: #383d41; }}
        .badge-other {{ background: #e2e3e5; color: #383d41; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>
                <span style="font-size: 28px;">📬</span>
                New Feedback Received
            </h1>
            <p>AgriDetect Feedback System</p>
        </div>
        
        <div class="content">
            <div class="feedback-info">
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">👤 Name</div>
                        <div class="info-value">{feedback_data.get('name', 'Not provided')}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">📧 Email</div>
                        <div class="info-value">{feedback_data.get('email', 'Not provided')}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">📞 Contact</div>
                        <div class="info-value">{feedback_data.get('contact', 'Not provided')}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">📅 Date & Time</div>
                        <div class="info-value">{formatted_time}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">🏷️ Feedback Type</div>
                        <div class="info-value">
                            <span class="badge {badge_class}">
                                {feedback_data.get('category', 'other').upper()}
                            </span>
                        </div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">⭐ Rating</div>
                        <div class="info-value">
                            <span class="rating-stars">{rating_display}</span>
                        </div>
                    </div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">📝 Subject</div>
                    <div class="info-value" style="font-size: 16px; font-weight: 500; color: #1b5e20;">
                        {feedback_data.get('subject', 'No subject')}
                    </div>
                </div>
            </div>
            
            <div class="message-box">
                <h3><span>💬</span> Message</h3>
                <div class="message-content">
                    {message_with_br}
                </div>
            </div>
            
            <div style="margin-top: 25px; padding: 15px; background: #e8f5e9; border-radius: 8px;">
                <div class="info-item">
                    <div class="info-label">📰 Subscription Preference</div>
                    <div class="info-value">
                        <strong>{'✅ Subscribed to updates' if feedback_data.get('subscribe') else '❌ Not subscribed to updates'}</strong>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>
                This feedback was submitted via {self.app_name} Feedback System.<br>
                <a href="{self.app_url}" style="color: #2e7d32; text-decoration: none;">{self.app_url}</a>
            </p>
            <p style="margin-top: 10px; font-size: 11px;">
                © {datetime.now().year} {self.app_name}. This is an automated message.
            </p>
        </div>
    </div>
</body>
</html>"""
        
        return html_content
    
    def create_feedback_email_text(self, feedback_data: Dict[str, Any]) -> str:
        """Create plain text email content for feedback"""
        
        timestamp = feedback_data.get('timestamp', datetime.now().isoformat())
        if isinstance(timestamp, str):
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                formatted_time = timestamp
        else:
            formatted_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Create plain text content
        text_content = f"""NEW FEEDBACK RECEIVED
=====================

System: {self.app_name}
Time: {formatted_time}

USER INFORMATION:
-----------------
Name: {feedback_data.get('name', 'Not provided')}
Email: {feedback_data.get('email', 'Not provided')}
Contact: {feedback_data.get('contact', 'Not provided')}

FEEDBACK DETAILS:
-----------------
Type: {feedback_data.get('category', 'Not specified')}
Rating: {feedback_data.get('rating', 'Not rated')}/5
Subject: {feedback_data.get('subject', 'No subject')}

MESSAGE:
--------
{feedback_data.get('message', 'No message provided')}

ADDITIONAL INFO:
----------------
Subscribe to updates: {'Yes' if feedback_data.get('subscribe') else 'No'}
Reference ID: {feedback_data.get('reference_id', 'N/A')}

---
This feedback was submitted via {self.app_name} Feedback System.
Automated message - © {datetime.now().year} {self.app_name}
"""
        
        return text_content
    
    def send_feedback_email(self, feedback_data: Dict[str, Any]) -> Tuple[bool, str, Optional[str]]:
        """
        Send feedback email via SMTP
        
        Returns:
            Tuple[bool, str, Optional[str]]: 
                (success, message, reference_id)
        """
        
        # Generate reference ID
        ref_id = feedback_data.get('reference_id', 
                                  f"FB-{datetime.now().strftime('%Y%m%d')}-{int(datetime.now().timestamp() % 10000):04d}")
        
        try:
            # Validate configuration
            is_valid, errors = self.validate_config()
            if not is_valid:
                return False, f"Configuration error: {', '.join(errors)}", ref_id
            
            # Create email message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.app_name} <{self.smtp_user}>"
            msg['To'] = self.admin_email
            msg['Subject'] = f"[{self.app_name}] New Feedback: {feedback_data.get('subject', 'No Subject')}"
            msg['X-Priority'] = '3'  # Normal priority
            
            # Add headers for better tracking
            msg['X-Feedback-ID'] = ref_id
            msg['X-Feedback-Type'] = feedback_data.get('category', 'unknown')
            
            # Create email content
            text_content = self.create_feedback_email_text(feedback_data)
            html_content = self.create_feedback_email_html(feedback_data)
            
            # Attach both versions
            msg.attach(MIMEText(text_content, 'plain'))
            msg.attach(MIMEText(html_content, 'html'))
            
            # Connect to SMTP server and send
            logger.info(f"Sending feedback email to {self.admin_email} (Ref: {ref_id})")
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
            success_message = f"Feedback email sent successfully to {self.admin_email} (Ref: {ref_id})"
            logger.info(success_message)
            
            return True, success_message, ref_id
            
        except smtplib.SMTPAuthenticationError as e:
            error_message = f"SMTP Authentication failed: {str(e)}"
            logger.error(error_message)
            return False, error_message, ref_id
            
        except Exception as e:
            error_message = f"Failed to send email: {str(e)}"
            logger.error(error_message)
            return False, error_message, ref_id
    
    def log_feedback(self, feedback_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Log feedback to JSON file"""
        try:
            log_file = 'logs/feedback_log.json'
            
            # Read existing feedback
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        existing_data = []
            else:
                existing_data = []
            
            # Add timestamp and reference ID if not present
            if 'timestamp' not in feedback_data:
                feedback_data['timestamp'] = datetime.now().isoformat()
            
            if 'reference_id' not in feedback_data:
                feedback_data['reference_id'] = f"FB-{datetime.now().strftime('%Y%m%d')}-{len(existing_data) + 1:04d}"
            
            # Add to existing data
            existing_data.append(feedback_data)
            
            # Save to file
            with open(log_file, 'w') as f:
                json.dump(existing_data, f, indent=2, default=str)
            
            logger.info(f"Feedback logged successfully (Ref: {feedback_data['reference_id']})")
            return True, f"Feedback logged successfully (Ref: {feedback_data['reference_id']})"
            
        except Exception as e:
            error_message = f"Failed to log feedback: {str(e)}"
            logger.error(error_message)
            return False, error_message
    
    def get_feedback_stats(self) -> Dict[str, Any]:
        """Get feedback statistics"""
        try:
            log_file = 'logs/feedback_log.json'
            
            if not os.path.exists(log_file):
                return {
                    'total': 0,
                    'by_type': {},
                    'by_rating': {},
                    'recent': []
                }
            
            with open(log_file, 'r') as f:
                feedback_data = json.load(f)
            
            # Calculate statistics
            total = len(feedback_data)
            
            by_type = {}
            by_rating = {}
            
            for entry in feedback_data:
                # Count by type
                fb_type = entry.get('category', 'other')
                by_type[fb_type] = by_type.get(fb_type, 0) + 1
                
                # Count by rating
                rating = entry.get('rating', 'Not rated')
                by_rating[rating] = by_rating.get(rating, 0) + 1
            
            # Get recent feedback (last 5)
            recent = feedback_data[-5:] if total > 5 else feedback_data
            recent = list(reversed(recent))  # Show newest first
            
            return {
                'total': total,
                'by_type': by_type,
                'by_rating': by_rating,
                'recent': recent
            }
            
        except Exception as e:
            logger.error(f"Error getting feedback stats: {str(e)}")
            return {
                'total': 0,
                'by_type': {},
                'by_rating': {},
                'recent': []
            }

# Create global instance
email_config = EmailConfig()

# Convenience functions
def send_feedback(feedback_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send feedback email and log it
    
    Returns:
        Dict with keys: success, message, reference_id
    """
    # Log feedback first
    log_success, log_message = email_config.log_feedback(feedback_data)
    
    # Send email
    email_success, email_message, ref_id = email_config.send_feedback_email(feedback_data)
    
    # Use reference ID from logging if email sending failed
    if not ref_id and log_success:
        ref_id = feedback_data.get('reference_id', 'N/A')
    
    return {
        'success': email_success and log_success,
        'message': f"{email_message} | {log_message}",
        'reference_id': ref_id,
        'email_sent': email_success,
        'logged': log_success
    }

def test_email_system() -> Dict[str, Any]:
    """Test the entire email system"""
    test_data = {
        'name': 'System Test',
        'email': 'test@system.com',
        'contact': 'Test Contact',
        'category': 'test',
        'subject': 'System Test Email',
        'message': 'This is an automated test of the email system.',
        'rating': '5',
        'subscribe': True
    }
    
    logger.info("Running email system test...")
    
    # Test configuration
    config_valid, config_errors = email_config.validate_config()
    
    # Test SMTP connection
    smtp_success, smtp_message = email_config.test_smtp_connection()
    
    # Test sending email
    result = send_feedback(test_data)
    
    # Get feedback stats
    stats = email_config.get_feedback_stats()
    
    return {
        'config_valid': config_valid,
        'config_errors': config_errors,
        'smtp_test': {
            'success': smtp_success,
            'message': smtp_message
        },
        'email_test': result,
        'stats': stats,
        'timestamp': datetime.now().isoformat()
    }

if __name__ == '__main__':
    """Run email system test when executed directly"""
    print("="*60)
    print("Email Configuration Module Test")
    print("="*60)
    
    # Test the system
    result = test_email_system()
    
    print(f"\nConfiguration: {'Valid' if result['config_valid'] else 'Invalid'}")
    if result['config_errors']:
        print("   Errors:", ", ".join(result['config_errors']))
    
    print(f"\nSMTP Connection: {'Success' if result['smtp_test']['success'] else 'Failed'}")
    print(f"   Message: {result['smtp_test']['message']}")
    
    print(f"\nEmail Test: {'Success' if result['email_test']['success'] else 'Failed'}")
    print(f"   Message: {result['email_test']['message']}")
    print(f"   Reference ID: {result['email_test']['reference_id']}")
    
    print(f"\nFeedback Statistics:")
    print(f"   Total Feedback: {result['stats']['total']}")
    
    print("\n" + "="*60)
    
    if all([result['config_valid'], result['smtp_test']['success'], result['email_test']['success']]):
        print("ALL TESTS PASSED! Email system is ready.")
        sys.exit(0)
    else:
        print("Some tests failed. Check the logs for details.")
        sys.exit(1)