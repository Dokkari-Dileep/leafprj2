"""
Alternative Email Solution without App Password
Uses smtplib with a different approach
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alternative():
    """Alternative method to send email"""
    
    # Try different methods
    methods = [
        {
            'name': 'Method 1: Standard Gmail',
            'port': 587,
            'context': None
        },
        {
            'name': 'Method 2: SSL Gmail',
            'port': 465,
            'context': ssl.create_default_context()
        },
        {
            'name': 'Method 3: Alternative SMTP',
            'server': 'smtp-mail.outlook.com',
            'port': 587,
            'context': None
        }
    ]
    
    sender_email = "dokkaridileep02@gmail.com"
    receiver_email = "dokkaridileep02@gmail.com"
    
    # Let user enter password
    print("\n🔑 Enter your App Password (16 characters, no spaces):")
    print("   Or press Enter to skip and try alternative methods")
    password = input("Password: ").strip()
    
    if password:
        password = password.replace(" ", "")
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "Test Email from Alternative Method"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    text = """This is a test email sent using alternative method."""
    html = """<html><body><h2>Test Email</h2><p>This is a test email.</p></body></html>"""
    
    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html, "html"))
    
    for method in methods:
        print(f"\nTrying {method['name']}...")
        
        try:
            if method['name'] == 'Method 3: Alternative SMTP':
                server = smtplib.SMTP(method['server'], method['port'])
            else:
                server = smtplib.SMTP("smtp.gmail.com", method['port'])
            
            if method.get('context'):
                server.starttls(context=method['context'])
            else:
                server.starttls()
            
            if password:
                server.login(sender_email, password)
            else:
                print("Skipping login (testing connection only)")
            
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()
            
            print(f"✅ {method['name']} SUCCESS!")
            return True
            
        except Exception as e:
            print(f"❌ {method['name']} failed: {str(e)[:100]}")
    
    return False

def setup_temp_email():
    """Setup temporary email using free service"""
    print("\n📧 TEMPORARY SOLUTION: Use free email service")
    print("\nSince Gmail App Password isn't working, let's use a free SMTP service:")
    
    print("\nOption 1: Use Brevo (Sendinblue) - FREE")
    print("   1. Sign up at: https://www.brevo.com/")
    print("   2. Get SMTP credentials")
    print("   3. Use these settings:")
    print("      SMTP server: smtp-relay.brevo.com")
    print("      Port: 587")
    print("      Login: your brevo login")
    print("      Password: your brevo SMTP key")
    
    print("\nOption 2: Use Elastic Email - FREE")
    print("   1. Sign up at: https://elasticemail.com/")
    print("   2. Get SMTP credentials")
    
    print("\nOption 3: Use SMTP2GO - FREE tier")
    print("   1. Sign up at: https://www.smtp2go.com/")
    
    print("\n⚡ QUICK FIX: Update your .env file with:")
    print("""
# Using Brevo (Sendinblue) example:
SMTP_SERVER=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=your_login@brevo.com
SMTP_PASSWORD=wtgnntcqksxsipdb
FROM_EMAIL=noreply@yourdomain.com
ADMIN_EMAIL=dokkaridileep02@gmail.com
""")

if __name__ == "__main__":
    print("="*60)
    print("ALTERNATIVE EMAIL SOLUTIONS")
    print("="*60)
    
    print("\n1. Try alternative Gmail methods")
    print("2. Use free email service")
    print("3. Test current setup")
    
    choice = input("\nChoose option (1, 2, or 3): ").strip()
    
    if choice == "1":
        send_email_alternative()
    elif choice == "2":
        setup_temp_email()
    elif choice == "3":
        import test_gmail
        test_gmail.test_gmail()