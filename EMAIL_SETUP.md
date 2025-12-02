# Email Configuration Guide for Bwire Finance Cloud

## Issue: Email Verification Not Being Received

The application is configured to send emails through Gmail SMTP, but requires an **App Password** instead of your regular Gmail password.

## Steps to Configure Email:

### 1. Generate Gmail App Password

1. Go to your Google Account: https://myaccount.google.com/
2. Click on **Security** in the left sidebar
3. Under "How you sign in to Google", enable **2-Step Verification** (if not already enabled)
4. After enabling 2FA, go back to Security settings
5. Click on **App passwords** (or search for "app passwords")
6. Select **Mail** as the app and **Other** as the device
7. Enter "Bwire Finance Cloud" as the device name
8. Click **Generate**
9. Copy the 16-character password (without spaces)

### 2. Update .env File

Open `.env` file and replace the placeholder:

```env
MAIL_USERNAME=bilfordderek917@gmail.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx
```

Replace `xxxx xxxx xxxx xxxx` with your generated app password (remove spaces).

Also update:
```env
SMTP_USERNAME=bilfordderek917@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
FROM_EMAIL=bilfordderek917@gmail.com
```

### 3. Restart the Application

After updating the `.env` file:
```bash
# Stop the current server (Ctrl+C)
# Then restart
python run.py
```

### 4. Test Email Sending

Register a new user or use the "Forgot Password" feature to test email delivery.

## Alternative: Use a Different Email Service

If you prefer not to use Gmail, you can configure other SMTP services:

### SendGrid:
```env
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=your_sendgrid_api_key
```

### Mailgun:
```env
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USERNAME=postmaster@your-domain.mailgun.org
MAIL_PASSWORD=your_mailgun_password
```

### Office 365:
```env
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USERNAME=your_email@outlook.com
MAIL_PASSWORD=your_password
```

## Current User Status

✅ **User: bilfordderek917@gmail.com**
- Role: **admin** (site owner with all rights)
- Email Verified: **True** (manually verified)
- Can now access all admin features

## Admin Privileges

As the first user and site owner, you now have:
- Full access to all system features
- Ability to manage all users
- Access to subscription management
- System configuration rights
- Security monitoring dashboard
- Financial reports and analytics
- Chama management for all groups
- M-Pesa integration controls

You can log in immediately without email verification.
