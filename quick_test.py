"""
Quick test to check Gmail App Password
"""

import smtplib

print("🔧 QUICK GMAIL APP PASSWORD TEST")
print("="*50)

# Let the user enter the password manually
password = input("\nEnter your NEW 16-character App Password (without spaces): ").strip()

# Remove any spaces if user accidentally entered them
password = password.replace(" ", "")

if len(password) != 16:
    print(f"\n❌ ERROR: Password should be 16 characters. You entered {len(password)} characters.")
    print("   Please generate a new App Password.")
    exit()

print(f"\n🔐 Testing password: {password[:4]}****{password[-4:]}")

try:
    # Test connection
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    
    print("📡 Connecting to Gmail...")
    server.login("dokkaridileep02@gmail.com", password)
    
    print("\n✅ SUCCESS! Your App Password works!")
    
    # Send test email
    from email.mime.text import MIMEText
    msg = MIMEText("This is a test email from the Python script. Your App Password is working!")
    msg['Subject'] = '✅ App Password Test - SUCCESS'
    msg['From'] = "dokkaridileep02@gmail.com"
    msg['To'] = "dokkaridileep02@gmail.com"
    
    server.send_message(msg)
    server.quit()
    
    print("\n📧 Test email sent successfully!")
    print("📬 Check your inbox at: dokkaridileep02@gmail.com")
    
    # Update .env file
    print("\n🔄 Updating .env file with new password...")
    try:
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        with open('.env', 'w') as f:
            for line in lines:
                if line.startswith('GMAIL_APP_PASSWORD='):
                    f.write(f'GMAIL_APP_PASSWORD={password}\n')
                else:
                    f.write(line)
        
        print("✅ .env file updated successfully!")
        print("\n🎉 Now run: python app.py")
        
    except:
        print("\n⚠️ Could not update .env file. Please update it manually:")
        print(f"   Change this line to: GMAIL_APP_PASSWORD={password}")
        
except Exception as e:
    print(f"\n❌ FAILED: {e}")
    
    if "Application-specific password required" in str(e):
        print("\n🔧 SOLUTION: You need to generate an App Password, not use your regular password.")
        print("   Follow these steps:")
        print("   1. Go to: https://myaccount.google.com/apppasswords")
        print("   2. Select 'Mail' and 'Other'")
        print("   3. Name it 'Python App'")
        print("   4. Copy the 16-character password")
        print("   5. Use that password (without spaces)")
    
    elif "Invalid credentials" in str(e):
        print("\n🔧 SOLUTION: The password is incorrect or expired.")
        print("   Generate a NEW App Password and try again.")
    
    elif "Username and Password not accepted" in str(e):
        print("\n🔧 SOLUTION: Make sure 2-Step Verification is ENABLED.")
        print("   Go to: https://myaccount.google.com/security")
        print("   Enable 2-Step Verification first")
    
    else:
        print("\n🔧 UNKNOWN ERROR. Try these steps:")
        print("   1. Enable 2-Step Verification")
        print("   2. Generate new App Password")
        print("   3. Make sure you copy ALL 16 characters without spaces")

print("\n" + "="*50)