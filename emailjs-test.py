# """
# EmailJS Testing Script with SMTP Backup
# Test EmailJS configuration and sending emails to dokkaridileep02@gmail.com
# """

# import os
# import sys
# import json
# import requests
# import smtplib
# from datetime import datetime
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from dotenv import load_dotenv

# # Add parent directory to path for imports
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# load_dotenv()

# class EmailTester:
#     """Comprehensive email testing class"""
    
#     def __init__(self):
#         # EmailJS Configuration
#         self.emailjs_service_id = os.getenv('EMAILJS_SERVICE_ID', '')
#         self.emailjs_template_id = os.getenv('EMAILJS_TEMPLATE_ID', '')
#         self.emailjs_user_id = os.getenv('EMAILJS_PUBLIC_KEY', '')
        
#         # SMTP Configuration (Primary - using your Gmail)
#         self.smtp_user = os.getenv('GMAIL_USER', 'dokkaridileep02@gmail.com')
#         self.smtp_password = os.getenv('GMAIL_APP_PASSWORD', 'wgzkkqojfyumuvbw')
#         self.admin_email = os.getenv('ADMIN_EMAIL', 'dokkaridileep02@gmail.com')
#         self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
#         self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        
#         # Test data
#         self.test_data = {
#             'name': 'Test User',
#             'email': 'test@example.com',
#             'contact': '+91 9876543210',
#             'category': 'Test',
#             'subject': 'Test Feedback from Script',
#             'message': 'This is a test message to verify email delivery system.',
#             'rating': '5',
#             'subscribe': True,
#             'timestamp': datetime.now().isoformat()
#         }

#     def print_header(self, title):
#         """Print formatted header"""
#         print("\n" + "="*60)
#         print(f"🔧 {title}")
#         print("="*60)

#     def check_configuration(self):
#         """Check all email configurations"""
#         self.print_header("CONFIGURATION CHECK")
        
#         configs = {
#             'EmailJS Service ID': self.emailjs_service_id,
#             'EmailJS Template ID': self.emailjs_template_id,
#             'EmailJS Public Key': self.emailjs_user_id,
#             'Gmail User': self.smtp_user,
#             'Gmail App Password': '✓ Set' if self.smtp_password else '✗ Missing',
#             'Admin Email': self.admin_email,
#             'SMTP Server': self.smtp_server,
#             'SMTP Port': self.smtp_port
#         }
        
#         all_ok = True
#         for key, value in configs.items():
#             status = '✓' if value and value not in ['✗ Missing'] else '✗'
#             print(f"  {status} {key}: {value}")
#             if not value or value == '✗ Missing':
#                 all_ok = False
        
#         return all_ok

#     def test_emailjs(self):
#         """Test EmailJS integration"""
#         self.print_header("EMAILJS TEST")
        
#         if not all([self.emailjs_service_id, self.emailjs_template_id, self.emailjs_user_id]):
#             print("❌ EmailJS configuration incomplete")
#             return False
        
#         # Prepare EmailJS data
#         emailjs_data = {
#             'service_id': self.emailjs_service_id,
#             'template_id': self.emailjs_template_id,
#             'user_id': self.emailjs_user_id,
#             'template_params': {
#                 'from_name': self.test_data['name'],
#                 'from_email': self.test_data['email'],
#                 'phone': self.test_data['contact'],
#                 'feedback_type': self.test_data['category'],
#                 'subject': self.test_data['subject'],
#                 'message': self.test_data['message'],
#                 'rating': self.test_data['rating'],
#                 'subscribe': 'Yes' if self.test_data['subscribe'] else 'No',
#                 'to_email': self.admin_email,
#                 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             }
#         }
        
#         try:
#             print(f"📧 Sending test email to: {self.admin_email}")
#             print(f"📤 Using template: {self.emailjs_template_id}")
            
#             # EmailJS API endpoint
#             url = 'https://api.emailjs.com/api/v1.0/email/send'
            
#             # Headers
#             headers = {
#                 'Content-Type': 'application/json',
#                 'origin': 'http://localhost:5000',
#                 'User-Agent': 'Mozilla/5.0 (EmailJS-Tester)'
#             }
            
#             # Send request
#             response = requests.post(url, headers=headers, json=emailjs_data, timeout=30)
            
#             if response.status_code == 200:
#                 print("✅ EmailJS test SUCCESSFUL!")
#                 print(f"📊 Response: {response.text}")
#                 return True
#             else:
#                 print(f"❌ EmailJS test FAILED - Status: {response.status_code}")
#                 print(f"📊 Response: {response.text}")
#                 if response.status_code == 400:
#                     print("💡 Tip: Check if your EmailJS service is connected to your email")
#                 return False
                
#         except requests.exceptions.Timeout:
#             print("❌ EmailJS test TIMEOUT - Server is not responding")
#             return False
#         except requests.exceptions.ConnectionError:
#             print("❌ EmailJS test CONNECTION ERROR - Check your internet connection")
#             return False
#         except Exception as e:
#             print(f"❌ EmailJS test ERROR: {str(e)}")
#             return False

#     def test_smtp(self):
#         """Test SMTP email sending (backup system)"""
#         self.print_header("SMTP EMAIL TEST")
        
#         if not all([self.smtp_user, self.smtp_password, self.admin_email]):
#             print("❌ SMTP configuration incomplete")
#             return False
        
#         try:
#             print(f"📧 Testing SMTP connection to: {self.smtp_server}:{self.smtp_port}")
#             print(f"📤 Sending from: {self.smtp_user}")
#             print(f"📥 Sending to: {self.admin_email}")
            
#             # Create message
#             msg = MIMEMultipart('alternative')
#             msg['From'] = self.smtp_user
#             msg['To'] = self.admin_email
#             msg['Subject'] = f"[TEST] SMTP Email Test - {datetime.now().strftime('%H:%M:%S')}"
            
#             # Create HTML content
#             html_content = f"""
#             <html>
#             <body style="font-family: Arial, sans-serif; line-height: 1.6;">
#                 <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
#                     <h2 style="color: #2e7d32;">✅ SMTP Email Test Successful!</h2>
                    
#                     <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
#                         <h3 style="color: #1b5e20;">Test Details</h3>
#                         <p><strong>Test Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
#                         <p><strong>System:</strong> Multi-Crop Disease Detection</p>
#                         <p><strong>Feature:</strong> Feedback System</p>
#                         <p><strong>Status:</strong> <span style="color: #4caf50;">Operational</span></p>
#                     </div>
                    
#                     <div style="margin-top: 20px; padding: 15px; background: #e8f5e9; border-radius: 5px;">
#                         <h4>Test Parameters:</h4>
#                         <ul>
#                             <li><strong>SMTP Server:</strong> {self.smtp_server}</li>
#                             <li><strong>SMTP Port:</strong> {self.smtp_port}</li>
#                             <li><strong>Sender:</strong> {self.smtp_user}</li>
#                             <li><strong>Receiver:</strong> {self.admin_email}</li>
#                         </ul>
#                     </div>
                    
#                     <hr style="margin: 20px 0;">
                    
#                     <div style="font-size: 12px; color: #666;">
#                         <p><strong>Test Message:</strong> {self.test_data['message']}</p>
#                         <p>This is an automated test email from the Email Testing Script.</p>
#                         <p>If you received this, your SMTP configuration is working correctly.</p>
#                     </div>
                    
#                     <div style="margin-top: 30px; padding-top: 15px; border-top: 1px solid #ddd; text-align: center;">
#                         <p style="color: #666; font-size: 11px;">
#                             © 2024 AgriDetect System | Automated Test Email
#                         </p>
#                     </div>
#                 </div>
#             </body>
#             </html>
#             """
            
#             # Create plain text version
#             text_content = f"""
# SMTP Email Test - SUCCESSFUL

# Test Details:
# -------------
# Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# System: Multi-Crop Disease Detection System
# Feature: Feedback System
# Status: OPERATIONAL

# Configuration:
# --------------
# SMTP Server: {self.smtp_server}
# SMTP Port: {self.smtp_port}
# Sender: {self.smtp_user}
# Receiver: {self.admin_email}

# Test Message:
# -------------
# {self.test_data['message']}

# This is an automated test email. If you received this, your SMTP configuration is working correctly.

# © 2024 AgriDetect System | Automated Test Email
#             """
            
#             # Attach both versions
#             msg.attach(MIMEText(text_content, 'plain'))
#             msg.attach(MIMEText(html_content, 'html'))
            
#             # Connect to SMTP server
#             print("🔄 Connecting to SMTP server...")
#             server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30)
#             server.set_debuglevel(0)  # Set to 1 for debug output
            
#             # Start TLS encryption
#             print("🔒 Starting TLS encryption...")
#             server.starttls()
            
#             # Login
#             print("🔑 Authenticating...")
#             server.login(self.smtp_user, self.smtp_password)
            
#             # Send email
#             print("📤 Sending email...")
#             server.send_message(msg)
            
#             # Quit
#             server.quit()
            
#             print("✅ SMTP test SUCCESSFUL!")
#             print(f"📨 Email sent successfully to {self.admin_email}")
#             return True
            
#         except smtplib.SMTPAuthenticationError:
#             print("❌ SMTP AUTHENTICATION FAILED")
#             print("💡 Possible issues:")
#             print("   - Incorrect email or password")
#             print("   - 2-Step Verification is enabled (use App Password)")
#             print("   - Less secure app access is disabled")
#             print("\n🔧 How to fix:")
#             print("   1. Go to https://myaccount.google.com/security")
#             print("   2. Enable 2-Step Verification")
#             print("   3. Generate an App Password")
#             print("   4. Use the App Password in your .env file")
#             return False
            
#         except smtplib.SMTPException as e:
#             print(f"❌ SMTP ERROR: {str(e)}")
#             return False
            
#         except Exception as e:
#             print(f"❌ UNEXPECTED ERROR: {str(e)}")
#             return False

#     def test_feedback_log(self):
#         """Test feedback logging system"""
#         self.print_header("FEEDBACK LOG SYSTEM TEST")
        
#         try:
#             log_dir = 'logs'
#             log_file = os.path.join(log_dir, 'feedback_log.json')
            
#             # Create logs directory if it doesn't exist
#             if not os.path.exists(log_dir):
#                 os.makedirs(log_dir)
#                 print(f"📁 Created directory: {log_dir}")
            
#             # Check if log file exists
#             if os.path.exists(log_file):
#                 with open(log_file, 'r') as f:
#                     try:
#                         feedback_data = json.load(f)
#                         entry_count = len(feedback_data)
#                         print(f"📊 Found {entry_count} feedback entries")
                        
#                         # Show recent entries
#                         if entry_count > 0:
#                             print("\n📋 Recent feedback entries:")
#                             for i, entry in enumerate(feedback_data[-3:], 1):
#                                 print(f"  {i}. {entry.get('timestamp', 'No date')} - {entry.get('name', 'Anonymous')}")
#                         return True
#                     except json.JSONDecodeError:
#                         print("⚠️ Log file exists but contains invalid JSON")
#                         return False
#             else:
#                 # Create empty log file
#                 with open(log_file, 'w') as f:
#                     json.dump([], f)
#                 print(f"📄 Created new feedback log: {log_file}")
#                 return True
                
#         except Exception as e:
#             print(f"❌ Error testing feedback log: {str(e)}")
#             return False

#     def simulate_feedback_submission(self):
#         """Simulate a complete feedback submission"""
#         self.print_header("COMPLETE FEEDBACK SUBMISSION SIMULATION")
        
#         try:
#             # Simulate the feedback data that would come from the form
#             feedback_data = {
#                 'name': 'John Doe',
#                 'email': 'john.doe@example.com',
#                 'contact': '+1 (555) 123-4567',
#                 'category': 'bug',
#                 'rating': '4',
#                 'subject': 'Found a bug in disease detection',
#                 'message': 'I found an issue where the system incorrectly identifies healthy leaves as diseased. Here are the steps to reproduce:\n1. Upload a clear image of a healthy tomato leaf\n2. Run detection\n3. System shows "Late Blight" with 85% confidence\n\nExpected: Should show "Healthy"',
#                 'subscribe': True,
#                 'timestamp': datetime.now().isoformat(),
#                 'reference_id': f"FB-{datetime.now().strftime('%Y%m%d')}-{int(datetime.now().timestamp() % 10000):04d}"
#             }
            
#             print("📋 Simulating feedback submission:")
#             print(f"  👤 Name: {feedback_data['name']}")
#             print(f"  📧 Email: {feedback_data['email']}")
#             print(f"  🏷️ Type: {feedback_data['category']}")
#             print(f"  ⭐ Rating: {feedback_data['rating']}/5")
#             print(f"  📝 Subject: {feedback_data['subject']}")
#             print(f"  🆔 Reference ID: {feedback_data['reference_id']}")
            
#             # Save to log file
#             log_dir = 'logs'
#             log_file = os.path.join(log_dir, 'feedback_log.json')
            
#             if os.path.exists(log_file):
#                 with open(log_file, 'r') as f:
#                     try:
#                         existing_data = json.load(f)
#                     except:
#                         existing_data = []
#             else:
#                 existing_data = []
            
#             existing_data.append(feedback_data)
            
#             with open(log_file, 'w') as f:
#                 json.dump(existing_data, f, indent=2)
            
#             print("✅ Simulation completed successfully!")
#             print(f"📄 Feedback logged to: {log_file}")
#             return True
            
#         except Exception as e:
#             print(f"❌ Simulation failed: {str(e)}")
#             return False

#     def run_all_tests(self):
#         """Run all tests and show summary"""
#         print("\n" + "="*60)
#         print("🚀 COMPREHENSIVE EMAIL SYSTEM TEST")
#         print("="*60)
#         print(f"📧 Target Email: {self.admin_email}")
#         print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#         print("="*60)
        
#         # Run tests
#         config_ok = self.check_configuration()
#         log_ok = self.test_feedback_log()
#         emailjs_ok = self.test_emailjs() if config_ok else False
#         smtp_ok = self.test_smtp() if config_ok else False
#         simulation_ok = self.simulate_feedback_submission()
        
#         # Print summary
#         self.print_header("TEST RESULTS SUMMARY")
        
#         results = [
#             ("Configuration Check", config_ok),
#             ("Feedback Log System", log_ok),
#             ("EmailJS Integration", emailjs_ok),
#             ("SMTP Email System", smtp_ok),
#             ("Feedback Simulation", simulation_ok)
#         ]
        
#         passed = 0
#         total = len(results)
        
#         for test_name, result in results:
#             status = "✅ PASS" if result else "❌ FAIL"
#             print(f"  {status} {test_name}")
#             if result:
#                 passed += 1
        
#         print("\n" + "="*60)
#         print(f"📊 SCORE: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
#         if passed == total:
#             print("🎉 ALL TESTS PASSED! Your email system is ready.")
#         else:
#             print("⚠️ Some tests failed. See recommendations below.")
        
#         # Recommendations
#         print("\n💡 RECOMMENDATIONS:")
        
#         if not config_ok:
#             print("  1. Complete your .env file with all required variables:")
#             print("     EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, EMAILJS_PUBLIC_KEY")
#             print("     GMAIL_USER, GMAIL_APP_PASSWORD, ADMIN_EMAIL")
        
#         if not emailjs_ok and config_ok:
#             print("  2. EmailJS issues:")
#             print("     - Verify your EmailJS account is active")
#             print("     - Check if service is connected to your email")
#             print("     - Test template in EmailJS dashboard")
        
#         if not smtp_ok and config_ok:
#             print("  3. SMTP issues:")
#             print("     - Enable 2-Step Verification in Google Account")
#             print("     - Generate App Password for your application")
#             print("     - Ensure less secure app access is enabled (if not using App Password)")
        
#         if not log_ok:
#             print("  4. Feedback log issues:")
#             print("     - Check directory permissions")
#             print("     - Ensure logs/ directory exists")
        
#         print("\n🔧 NEXT STEPS:")
#         print("   1. Start your Flask application: python app.py")
#         print("   2. Open http://localhost:5000/feedback")
#         print("   3. Submit a test feedback")
#         print("   4. Check your email at dokkaridileep02@gmail.com")
#         print("   5. Verify feedback appears in logs/feedback_log.json")
        
#         print("\n" + "="*60)
#         return passed == total

# def create_env_template():
#     """Create a template .env file if it doesn't exist"""
#     env_template = """# EmailJS Configuration (Optional - for client-side email)
# EMAILJS_SERVICE_ID=your_service_id_here
# EMAILJS_TEMPLATE_ID=your_template_id_here
# EMAILJS_PUBLIC_KEY=your_public_key_here

# # SMTP Configuration (Primary - using Gmail)
# GMAIL_USER=dokkaridileep02@gmail.com
# GMAIL_APP_PASSWORD=wgzkkqojfyumuvbw
# ADMIN_EMAIL=dokkaridileep02@gmail.com
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587

# # Application Configuration
# SECRET_KEY=your-secret-key-here-change-this
# FLASK_ENV=development
# DEBUG=True
# """
    
#     if not os.path.exists('.env'):
#         with open('.env', 'w') as f:
#             f.write(env_template)
#         print("📄 Created .env template file. Please update with your credentials.")
#         return True
#     return False

# def main():
#     """Main function"""
#     # Check if .env exists, create template if not
#     if not os.path.exists('.env'):
#         print("⚠️ No .env file found!")
#         create = input("Create .env template? (y/n): ")
#         if create.lower() == 'y':
#             create_env_template()
#         else:
#             print("❌ Cannot proceed without .env file")
#             return
    
#     # Load environment variables
#     load_dotenv()
    
#     # Run tests
#     tester = EmailTester()
#     success = tester.run_all_tests()
    
#     # Exit with appropriate code
#     sys.exit(0 if success else 1)

# if __name__ == '__main__':
#     main()













"""
Simplified Email Testing Script
"""

import os
import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def test_email_system():
    """Test the email system"""
    print("="*60)
    print("Testing Email System")
    print("="*60)
    
    # Get credentials from environment or use defaults
    smtp_user = os.getenv('GMAIL_USER', 'dokkaridileep02@gmail.com')
    smtp_password = os.getenv('GMAIL_APP_PASSWORD', 'wtgnntcqksxsipdb')
    admin_email = os.getenv('ADMIN_EMAIL', 'dokkaridileep02@gmail.com')
    
    print(f"\nConfiguration:")
    print(f"  SMTP User: {smtp_user}")
    print(f"  Admin Email: {admin_email}")
    print(f"  SMTP Password: {'Set' if smtp_password else 'Not set'}")
    
    if not smtp_password:
        print("\n❌ ERROR: GMAIL_APP_PASSWORD is not set in .env file")
        print("\nPlease create a .env file with:")
        print("GMAIL_USER=dokkaridileep02@gmail.com")
        print("GMAIL_APP_PASSWORD=your_app_password_here")
        print("ADMIN_EMAIL=dokkaridileep02@gmail.com")
        return False
    
    # Test SMTP connection
    print("\nTesting SMTP connection to Gmail...")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(smtp_user, smtp_password)
        print("✅ SMTP login successful")
        
        # Send test email
        print("\nSending test email...")
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = admin_email
        msg['Subject'] = 'Test Email from Disease Detection System'
        
        body = f"""This is a test email from the Multi-Crop Disease Detection System.
        
If you're receiving this, your email configuration is working correctly.

Test Details:
- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- From: {smtp_user}
- To: {admin_email}
- Status: ✅ SUCCESS

Best regards,
AgriDetect System
"""
        
        msg.attach(MIMEText(body, 'plain'))
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Test email sent successfully to {admin_email}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("\n❌ SMTP Authentication Failed")
        print("\nCommon issues:")
        print("1. Incorrect Gmail App Password")
        print("2. 2-Step Verification not enabled")
        print("3. Less secure app access disabled")
        
        print("\nHow to fix:")
        print("1. Go to https://myaccount.google.com/security")
        print("2. Enable 2-Step Verification")
        print("3. Generate an App Password")
        print("4. Use that password in your .env file")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def check_feedback_log():
    """Check feedback log"""
    print("\nChecking feedback log...")
    
    if not os.path.exists('logs'):
        os.makedirs('logs')
        print("✅ Created logs directory")
    
    log_file = 'logs/feedback_log.json'
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                feedback = json.load(f)
                print(f"✅ Feedback log found with {len(feedback)} entries")
                return True
        except:
            print("⚠️ Feedback log exists but contains invalid JSON")
            return False
    else:
        with open(log_file, 'w') as f:
            json.dump([], f)
        print("✅ Created new feedback log")
        return True

def main():
    """Main function"""
    print("🚀 Starting Email System Test")
    print("="*60)
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("⚠️ No .env file found!")
        print("\nCreating .env template...")
        with open('.env', 'w') as f:
            f.write("""# Email Configuration
GMAIL_USER=dokkaridileep02@gmail.com
GMAIL_APP_PASSWORD=your_app_password_here
ADMIN_EMAIL=dokkaridileep02@gmail.com

# Optional: EmailJS (for client-side email)
EMAILJS_SERVICE_ID=your_service_id
EMAILJS_TEMPLATE_ID=your_template_id
EMAILJS_PUBLIC_KEY=your_public_key

# Flask Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
""")
        print("✅ Created .env file. Please edit it with your credentials.")
        print("\nAfter editing .env, run this script again.")
        return
    
    # Load environment variables
    load_dotenv()
    
    # Run tests
    log_ok = check_feedback_log()
    email_ok = test_email_system()
    
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    print(f"Feedback Log: {'✅ PASS' if log_ok else '❌ FAIL'}")
    print(f"Email System: {'✅ PASS' if email_ok else '❌ FAIL'}")
    
    if log_ok and email_ok:
        print("\n🎉 All tests passed! Your email system is ready.")
        print("\nNext steps:")
        print("1. Run the Flask app: python app.py")
        print("2. Open http://localhost:5000/feedback")
        print("3. Submit a feedback form")
        print("4. Check your email at dokkaridileep02@gmail.com")
    else:
        print("\n⚠️ Some tests failed. See above for details.")

if __name__ == '__main__':
    main()