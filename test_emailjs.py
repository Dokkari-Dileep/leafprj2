# """
# EmailJS Testing Script
# Test EmailJS configuration and sending emails
# """

# import requests
# import json
# from dotenv import load_dotenv
# import os

# load_dotenv()

# def test_emailjs():
#     """Test EmailJS integration"""
    
#     # EmailJS configuration
#     service_id = os.getenv('EMAILJS_SERVICE_ID', '')
#     template_id = os.getenv('EMAILJS_TEMPLATE_ID', '')
#     user_id = os.getenv('EMAILJS_PUBLIC_KEY', '')
    
#     if not all([service_id, template_id, user_id]):
#         print("❌ EmailJS configuration missing. Check .env file.")
#         print(f"Service ID: {'✓' if service_id else '✗'}")
#         print(f"Template ID: {'✓' if template_id else '✗'}")
#         print(f"User ID: {'✓' if user_id else '✗'}")
#         return False
    
#     # Test data
#     test_data = {
#         'service_id': service_id,
#         'template_id': template_id,
#         'user_id': user_id,
#         'template_params': {
#             'from_name': 'Test User',
#             'from_email': 'test@example.com',
#             'phone': '1234567890',
#             'message': 'This is a test message from EmailJS testing script.',
#             'feedback_type': 'Test',
#             'rating': '5',
#             'to_email': os.getenv('ADMIN_EMAIL', 'admin@example.com')
#         }
#     }
    
#     try:
#         # EmailJS API endpoint
#         url = 'https://api.emailjs.com/api/v1.0/email/send'
        
#         # Headers
#         headers = {
#             'Content-Type': 'application/json',
#             'origin': 'http://localhost',
#             'User-Agent': 'Mozilla/5.0'
#         }
        
#         print("🚀 Testing EmailJS integration...")
#         print(f"📧 Sending test email to: {test_data['template_params']['to_email']}")
        
#         # Send request
#         response = requests.post(url, headers=headers, json=test_data)
        
#         if response.status_code == 200:
#             print("✅ EmailJS test successful!")
#             print(f"📤 Response: {response.text}")
#             return True
#         else:
#             print(f"❌ EmailJS test failed with status: {response.status_code}")
#             print(f"📤 Response: {response.text}")
#             return False
            
#     except Exception as e:
#         print(f"❌ Error testing EmailJS: {e}")
#         return False

# def check_feedback_log():
#     """Check feedback log file"""
#     try:
#         if os.path.exists('feedback_log.json'):
#             with open('feedback_log.json', 'r') as f:
#                 feedback = json.load(f)
#                 print(f"📊 Feedback log entries: {len(feedback)}")
#                 return True
#         else:
#             print("📄 Creating new feedback log file...")
#             with open('feedback_log.json', 'w') as f:
#                 json.dump([], f)
#             return True
#     except Exception as e:
#         print(f"❌ Error with feedback log: {e}")
#         return False

# def test_backup_email():
#     """Test backup email functionality"""
#     import smtplib
#     from email.mime.text import MIMEText
#     from email.mime.multipart import MIMEMultipart
    
#     # Configuration for backup email (using Gmail SMTP)
#     smtp_server = 'smtp.gmail.com'
#     smtp_port = 587
#     sender_email = os.getenv('BACKUP_EMAIL', '')
#     sender_password = os.getenv('BACKUP_EMAIL_PASSWORD', '')
#     receiver_email = os.getenv('ADMIN_EMAIL', '')
    
#     if not all([sender_email, sender_password, receiver_email]):
#         print("⚠️ Backup email configuration incomplete")
#         return False
    
#     try:
#         print("🔄 Testing backup email (SMTP)...")
        
#         # Create message
#         message = MIMEMultipart()
#         message['From'] = sender_email
#         message['To'] = receiver_email
#         message['Subject'] = 'Test Email from Disease Detection System'
        
#         body = """
#         This is a test email from the Multi-Crop Disease Detection System.
        
#         If you're receiving this, the backup email system is working correctly.
        
#         System Details:
#         - Application: CropGuard AI
#         - Feature: Feedback/Notification System
#         - Status: Operational
        
#         Best regards,
#         CropGuard AI Team
#         """
        
#         message.attach(MIMEText(body, 'plain'))
        
#         # Connect and send
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()
#         server.login(sender_email, sender_password)
#         server.send_message(message)
#         server.quit()
        
#         print("✅ Backup email test successful!")
#         return True
        
#     except Exception as e:
#         print(f"❌ Backup email test failed: {e}")
#         return False

# def main():
#     """Main testing function"""
#     print("=" * 50)
#     print("🔧 EMAILJS & FEEDBACK SYSTEM TEST")
#     print("=" * 50)
    
#     # Test 1: Check configuration
#     print("\n📋 Test 1: Configuration Check")
#     load_dotenv()
    
#     required_vars = [
#         'EMAILJS_SERVICE_ID',
#         'EMAILJS_TEMPLATE_ID', 
#         'EMAILJS_PUBLIC_KEY',
#         'ADMIN_EMAIL'
#     ]
    
#     all_present = True
#     for var in required_vars:
#         value = os.getenv(var)
#         status = '✓' if value else '✗'
#         print(f"  {status} {var}: {value if value else 'Not Set'}")
#         if not value:
#             all_present = False
    
#     if not all_present:
#         print("\n⚠️ Please set all required environment variables in .env file")
#         print("   Required variables:")
#         print("   - EMAILJS_SERVICE_ID")
#         print("   - EMAILJS_TEMPLATE_ID")
#         print("   - EMAILJS_PUBLIC_KEY")
#         print("   - ADMIN_EMAIL")
#         print("\n   Optional (for backup):")
#         print("   - BACKUP_EMAIL")
#         print("   - BACKUP_EMAIL_PASSWORD")
    
#     # Test 2: Check feedback log
#     print("\n📋 Test 2: Feedback Log System")
#     feedback_log_ok = check_feedback_log()
    
#     # Test 3: Test EmailJS
#     print("\n📋 Test 3: EmailJS Integration")
#     if all_present:
#         emailjs_ok = test_emailjs()
#     else:
#         print("⏭️ Skipping - Configuration incomplete")
#         emailjs_ok = False
    
#     # Test 4: Backup email
#     print("\n📋 Test 4: Backup Email System")
#     backup_email = os.getenv('BACKUP_EMAIL')
#     backup_password = os.getenv('BACKUP_EMAIL_PASSWORD')
    
#     if backup_email and backup_password:
#         backup_ok = test_backup_email()
#     else:
#         print("⏭️ Skipping - Backup email not configured")
#         backup_ok = False
    
#     # Summary
#     print("\n" + "=" * 50)
#     print("📊 TEST RESULTS SUMMARY")
#     print("=" * 50)
    
#     results = {
#         "Configuration": "✓" if all_present else "✗",
#         "Feedback Log": "✓" if feedback_log_ok else "✗",
#         "EmailJS": "✓" if emailjs_ok else "✗",
#         "Backup Email": "✓" if backup_ok else "N/A"
#     }
    
#     for test, result in results.items():
#         print(f"  {test}: {result}")
    
#     print("\n💡 Recommendations:")
#     if not all_present:
#         print("  • Complete .env file with EmailJS credentials")
#     if not emailjs_ok and all_present:
#         print("  • Check EmailJS service/template IDs")
#         print("  • Verify EmailJS account is active")
#     if backup_email and not backup_password:
#         print("  • Add backup email password to .env")
    
#     print("\n✅ Setup complete. Run 'python app.py' to start the application.")

# if __name__ == '__main__':
#     main()








# app.py (Flask backend)
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Email configuration from your email_config.py
GMAIL_USER = "dokkaridileep02@gmail.com"
GMAIL_APP_PASSWORD = "wtgnntcqksxsipdb"  # Your Gmail app password
ADMIN_EMAIL = "dokkaridileep02@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Ensure feedback log directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

def validate_email_config():
    """Validate email configuration"""
    errors = []
    
    if not GMAIL_USER:
        errors.append("GMAIL_USER is not configured")
    
    if not GMAIL_APP_PASSWORD:
        errors.append("GMAIL_APP_PASSWORD is not configured")
    
    if not ADMIN_EMAIL:
        errors.append("ADMIN_EMAIL is not configured")
    
    return errors

def send_email_via_smtp(form_data):
    """Send email using SMTP (Gmail)"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = f"New Feedback: {form_data['subject']}"
        
        # Create HTML email body
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2 style="color: #2e7d32;">New Feedback Received</h2>
            <div style="background: #f5f5f5; padding: 20px; border-radius: 5px;">
                <h3 style="color: #1b5e20;">Feedback Details</h3>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Name:</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid #ddd;">{form_data['name']}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Email:</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid #ddd;">{form_data['email']}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Contact:</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid #ddd;">{form_data.get('contact', 'Not provided')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Type:</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid #ddd;">{form_data['category']}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Rating:</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid #ddd;">{form_data.get('rating', 'Not rated')}/5</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Subject:</strong></td>
                        <td style="padding: 8px; border-bottom: 1px solid #ddd;">{form_data['subject']}</td>
                    </tr>
                </table>
                
                <h4 style="color: #1b5e20; margin-top: 20px;">Message:</h4>
                <div style="background: white; padding: 15px; border-radius: 5px; border-left: 4px solid #4caf50;">
                    {form_data['message'].replace('\n', '<br>')}
                </div>
                
                <p style="margin-top: 20px;">
                    <strong>Subscribe to updates:</strong> {'Yes' if form_data.get('subscribe') else 'No'}
                </p>
                
                <hr style="margin: 20px 0;">
                <p style="font-size: 12px; color: #666;">
                    This feedback was submitted via AgriDetect Feedback System at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </p>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version
        text_content = f"""
New Feedback Received

Name: {form_data['name']}
Email: {form_data['email']}
Contact: {form_data.get('contact', 'Not provided')}
Feedback Type: {form_data['category']}
Rating: {form_data.get('rating', 'Not rated')}/5
Subject: {form_data['subject']}

Message:
{form_data['message']}

Subscribe to updates: {'Yes' if form_data.get('subscribe') else 'No'}

Submitted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        # Attach both HTML and plain text
        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        # Connect to SMTP server and send
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email sent successfully to {ADMIN_EMAIL}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

def log_feedback(form_data):
    """Log feedback to JSON file"""
    try:
        log_file = 'logs/feedback_log.json'
        
        # Read existing feedback or create new list
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                try:
                    feedback_log = json.load(f)
                except json.JSONDecodeError:
                    feedback_log = []
        else:
            feedback_log = []
        
        # Add timestamp and reference ID
        feedback_entry = {
            'timestamp': datetime.now().isoformat(),
            'reference_id': f"FB-{datetime.now().strftime('%Y%m%d')}-{len(feedback_log) + 1:04d}",
            **form_data
        }
        
        feedback_log.append(feedback_entry)
        
        # Save to file
        with open(log_file, 'w') as f:
            json.dump(feedback_log, f, indent=2, default=str)
        
        print(f"✅ Feedback logged with ID: {feedback_entry['reference_id']}")
        return feedback_entry['reference_id']
        
    except Exception as e:
        print(f"❌ Error logging feedback: {e}")
        return None

@app.route('/feedback')
def feedback_page():
    """Render feedback page"""
    return render_template('feedback.html')

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    """Handle feedback submission"""
    try:
        # Get form data
        form_data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'category', 'subject', 'message']
        for field in required_fields:
            if not form_data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'Please fill in the {field.replace("_", " ")} field.'
                }), 400
        
        # Log feedback to file
        reference_id = log_feedback(form_data)
        
        # Send email notification
        email_sent = send_email_via_smtp(form_data)
        
        if email_sent:
            return jsonify({
                'success': True,
                'message': 'Feedback submitted successfully!',
                'reference_id': reference_id
            })
        else:
            return jsonify({
                'success': True,
                'message': 'Feedback logged but email notification failed.',
                'reference_id': reference_id,
                'warning': 'Could not send email notification'
            })
            
    except Exception as e:
        print(f"❌ Error processing feedback: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing your feedback. Please try again.'
        }), 500

@app.route('/api/feedback')
def get_feedback():
    """API endpoint to get feedback data (protected)"""
    try:
        log_file = 'logs/feedback_log.json'
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                feedback_data = json.load(f)
            return jsonify({
                'success': True,
                'count': len(feedback_data),
                'feedback': feedback_data
            })
        else:
            return jsonify({
                'success': True,
                'count': 0,
                'feedback': []
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# Test email configuration on startup
@app.before_first_request
def test_email_config():
    """Test email configuration on startup"""
    print("🔧 Testing email configuration...")
    errors = validate_email_config()
    
    if errors:
        print("❌ Email configuration errors:")
        for error in errors:
            print(f"   - {error}")
    else:
        print("✅ Email configuration is valid")
        
        # Test SMTP connection
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.quit()
            print("✅ SMTP connection successful")
        except Exception as e:
            print(f"❌ SMTP connection failed: {e}")

if __name__ == '__main__':
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Create feedback log file if it doesn't exist
    log_file = 'logs/feedback_log.json'
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            json.dump([], f)
    
    print("🚀 Starting AgriDetect Feedback System...")
    print(f"📧 Admin email: {ADMIN_EMAIL}")
    print(f"📧 Sender email: {GMAIL_USER}")
    print("🌐 Server running on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)