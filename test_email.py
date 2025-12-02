from app import create_app
from app.utils.email_service import email_service

app = create_app()

with app.app_context():
    print("=" * 60)
    print("EMAIL CONFIGURATION TEST")
    print("=" * 60)
    print(f"Email Server: {email_service.smtp_server}")
    print(f"Port: {email_service.port}")
    print(f"Sender Email: {email_service.sender_email}")
    print(f"Password Configured: {'Yes' if email_service.password else 'No'}")
    print(f"Use TLS: {email_service.use_tls}")
    print("=" * 60)
    
    print("\nSending test email to bilfordderek917@gmail.com...")
    print("This will verify that email verification works for customers.\n")
    
    result = email_service.send_email(
        recipient_email='bilfordderek917@gmail.com',
        subject='Test Email - Bwire Finance Cloud Email Verification Working',
        html_content='''
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h1 style="color: #667eea;">✅ Email System is Working!</h1>
            <p>Congratulations! Your email configuration is working correctly.</p>
            <p><strong>From:</strong> chamalink.system@gmail.com</p>
            <p><strong>To:</strong> bilfordderek917@gmail.com</p>
            <hr>
            <h2>What This Means:</h2>
            <ul>
                <li>✅ Customer email verification will work</li>
                <li>✅ Password reset emails will be sent</li>
                <li>✅ 2FA codes will be delivered</li>
                <li>✅ System notifications will reach users</li>
            </ul>
            <hr>
            <p style="color: #666; font-size: 12px;">
                This is a test email from Bwire Finance Cloud.<br>
                Powered by Bwire Global Tech
            </p>
        </body>
        </html>
        ''',
        text_content='Email System Test - Your Bwire Finance Cloud email configuration is working correctly!'
    )
    
    print("=" * 60)
    if result:
        print("✅ EMAIL SENT SUCCESSFULLY!")
        print("✅ Check bilfordderek917@gmail.com inbox")
        print("✅ Customer verification emails will now work!")
    else:
        print("❌ EMAIL FAILED TO SEND")
        print("Check the error messages above for details")
    print("=" * 60)
