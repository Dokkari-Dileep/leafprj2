"""
Test Gmail SMTP connection
"""

import smtplib
from email.mime.text import MIMEText

def test_gmail():
    print("Testing Gmail SMTP connection...")
    
    # Your Gmail credentials
    gmail_user = "dokkaridileep02@gmail.com"
    gmail_password = "wgzkkqojfyumuvbw"  # This might be incorrect
    
    try:
        # Try to connect to Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print(f"Attempting to login with: {gmail_user}")
        server.login(gmail_user, gmail_password)
        print("✅ SMTP Login successful!")
        
        # Create a simple test email
        msg = MIMEText("This is a test email from Python script.")
        msg['Subject'] = 'Test Email from Script'
        msg['From'] = gmail_user
        msg['To'] = gmail_user
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        print("✅ Test email sent successfully!")
        print(f"📧 Check your inbox at: {gmail_user}")
        
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("\n❌ SMTP Authentication Failed!")
        print("\n🔧 Common Issues & Solutions:")
        print("=" * 50)
        print("1. ❌ You're using your regular Gmail password")
        print("   ✅ Solution: You MUST use an App Password")
        print()
        print("2. ❌ 2-Step Verification not enabled")
        print("   ✅ Solution: Enable 2-Step Verification first")
        print()
        print("3. ❌ Incorrect App Password")
        print("   ✅ Solution: Generate a new App Password")
        print()
        print("📋 Steps to fix:")
        print("   1. Go to: https://myaccount.google.com/security")
        print("   2. Enable 2-Step Verification (if not already)")
        print("   3. Under 'Signing in to Google', click 'App passwords'")
        print("   4. Select 'Mail' and 'Other' (name it 'Python App')")
        print("   5. Copy the 16-character password")
        print("   6. Update your .env file with the new password")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_gmail()