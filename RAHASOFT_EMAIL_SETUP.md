# 📧 Rahasoft Email Configuration Guide

## ✅ What's Configured

Your Bwire Finance Cloud application is set up to send emails from:
**rahasoft.app@gmail.com**

This email will be used for:
- ✉️ Email verification for new users
- 🔒 Password reset requests
- 🔐 Two-factor authentication codes
- 🔔 System notifications
- 💳 Subscription confirmations
- 📊 Loan approval requests

## 🚀 Steps to Enable Email Sending

### 1. Get the Gmail App Password for rahasoft.app@gmail.com

You need the **Gmail App Password** (not regular password) for `rahasoft.app@gmail.com`.

#### To Generate a New App Password:

1. **Sign in to Google Account**: https://myaccount.google.com/
   - Use the rahasoft.app@gmail.com account
   
2. **Enable 2-Step Verification** (if not already enabled):
   - Go to Security → 2-Step Verification
   - Follow the prompts to enable it

3. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Or: Security → App passwords (appears after 2FA is enabled)
   - Select app: **Mail**
   - Select device: **Other** (enter "Bwire Finance Cloud")
   - Click **Generate**
   - Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

### 2. Update the .env File

Open the `.env` file in your project root and replace the placeholders:

```env
# Email Configuration
MAIL_USERNAME=rahasoft.app@gmail.com
MAIL_PASSWORD=abcdefghijklmnop  # ← Paste your 16-character app password here (remove spaces)

# Security Email Configuration
SMTP_USERNAME=rahasoft.app@gmail.com
SMTP_PASSWORD=abcdefghijklmnop  # ← Same password here
FROM_EMAIL=rahasoft.app@gmail.com
```

**Important:** Remove all spaces from the app password!

### 3. Restart the Application

```powershell
# Stop the running server (Ctrl+C in the terminal)
# Then restart:
python run.py
```

### 4. Test Email Sending

To test if emails are working:

1. **Register a New User**: Try registering with a real email address
2. **Check Inbox**: Look for verification email from rahasoft.app@gmail.com
3. **Check Spam**: Sometimes first emails go to spam folder

#### Test with Python:

```powershell
cd "c:\Users\Afronic\Desktop\Bwire Finance Cloud"
python -c "from app import create_app; from app.utils.email_service import email_service; app = create_app(); app.app_context().push(); print('Testing email...'); result = email_service.send_email('your_test_email@gmail.com', 'Test Email', '<h1>Test from Bwire Finance Cloud</h1><p>Email is working!</p>'); print('Email sent!' if result else 'Email failed - check MAIL_PASSWORD in .env')"
```

## 🔍 Troubleshooting

### Email Not Received?

1. **Check .env file**: Ensure `MAIL_PASSWORD` is set correctly
2. **Check spam folder**: First emails often go to spam
3. **Verify 2FA is enabled**: On rahasoft.app@gmail.com account
4. **Check app password**: Make sure it's copied without spaces
5. **Check logs**: Look for errors in the terminal output

### Common Error Messages:

**"Email password not configured"**
- Solution: Add the app password to `.env` file

**"SMTP Authentication failed"**
- Solution: Generate a new app password
- Make sure 2FA is enabled on the Gmail account

**"Connection refused"**
- Solution: Check internet connection
- Verify MAIL_SERVER and MAIL_PORT settings

### Debug Mode Output:

In development mode, the application logs email attempts. Check the terminal for:
```
✅ Email sent successfully to user@example.com
```
or
```
❌ Email sending failed: [error message]
```

## 📋 Current Configuration Summary

| Setting | Value |
|---------|-------|
| **Email Server** | smtp.gmail.com |
| **Port** | 587 |
| **TLS** | Enabled |
| **Sender Email** | rahasoft.app@gmail.com |
| **Sender Name** | Bwire Finance Cloud Support |

## 🎯 What Happens After Setup

Once configured, customers will receive professional emails:

### Email Verification Example:
```
From: Bwire Finance Cloud Support <rahasoft.app@gmail.com>
Subject: [Bwire Finance Cloud] Please Verify Your Email Address

[Beautiful HTML email with branding, verification button, and instructions]
```

### Features:
- ✅ Professional HTML email templates
- ✅ Mobile-responsive design
- ✅ Clear call-to-action buttons
- ✅ Security warnings and tips
- ✅ Branded headers and footers
- ✅ Plain text fallback for old email clients

## 🔐 Security Best Practices

1. **Never commit .env file**: It contains sensitive passwords
2. **Use App Passwords**: Never use regular Gmail password
3. **Keep 2FA enabled**: On rahasoft.app@gmail.com
4. **Monitor email logs**: Check for unusual activity
5. **Update passwords regularly**: Generate new app passwords periodically

## 📞 Need Help?

If you continue to have issues:
1. Check that rahasoft.app@gmail.com has 2FA enabled
2. Generate a fresh app password
3. Verify the password is copied correctly (no spaces)
4. Check Gmail account isn't locked or suspended
5. Test with the Python command above to see detailed errors

## ✅ Quick Checklist

- [ ] rahasoft.app@gmail.com has 2FA enabled
- [ ] Generated new Gmail App Password
- [ ] Updated .env file with correct password (no spaces)
- [ ] Restarted the application
- [ ] Tested with real email address
- [ ] Checked spam folder
- [ ] Email received successfully!

---

**Ready to enable emails?** Just add the app password to `.env` and restart! 🚀
