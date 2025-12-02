# 🏦 Bwire Finance Cloud

**Modern Financial Ecosystem for Individuals, Businesses & Groups**

Powered by **Bwire Global Tech**

---

## 🌟 Overview

Bwire Finance Cloud is a comprehensive, cloud-based financial management platform that evolved from CHAMAlink. It serves individuals, businesses, chamas (investment groups), Saccos, SMEs, cooperatives, and enterprises with a full suite of financial tools.

### What Makes Us Different

- **🌍 Cloud-Native Architecture** - PostgreSQL/Supabase backend, real-time syncing
- **🤖 AI-Powered Intelligence** - Smart budgeting, fraud detection, predictive insights
- **💰 Multiple Payment Integrations** - M-Pesa, Airtel Money, Bank APIs
- **🔒 Enterprise Security** - Role-based access, encryption, audit logs
- **📱 Mobile-First Design** - Responsive across all devices
- **🌐 Multi-Currency Support** - Global deployment ready

---

## 🚀 Key Features

### Financial Management
- **Digital Wallet** - Secure money management
- **Advanced Ledger** - Complete accounting system
- **Investment Tracking** - ROI calculators & goals
- **Loan Management** - Applications, approvals, tracking
- **Receipt Generation** - Automated digital receipts

### Group Finance (Chamas, Saccos)
- **Group Creation & Management**
- **Contribution Tracking**
- **Member Management**
- **Automated Reminders**
- **Multi-signature Transactions**
- **Meeting Minutes**

### Payments & Integrations
- **M-Pesa Integration** - STK Push, C2B, B2C
- **Bank Transfers**
- **Recurring Payments**
- **QR Code Payments** (Coming Soon)

### Reports & Analytics
- **Financial Reports**
- **Custom Analytics**
- **Export to PDF/Excel**
- **Real-time Dashboards**

### Security & Compliance
- **2FA Authentication**
- **Role-Based Access Control**
- **Encrypted Data Storage**
- **Audit Trails**
- **Security Monitoring**

---

## 🛠️ Technology Stack

- **Backend**: Python 3.13, Flask 3.1
- **Database**: PostgreSQL (Supabase)
- **ORM**: SQLAlchemy 2.0
- **Authentication**: Flask-Login, 2FA
- **Payments**: M-Pesa API, Bank Integrations
- **Frontend**: Bootstrap 5, Modern CSS
- **Email**: Flask-Mail
- **Migrations**: Alembic

---

## 📦 Installation

### Prerequisites
- Python 3.11+
- PostgreSQL database
- M-Pesa API credentials (optional)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/RahasoftBwire/CHAMAlink.git
cd "Bwire Finance Cloud"
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
Create a `.env` file:
```env
# Database
SQLALCHEMY_DATABASE_URI=postgresql://user:password@host:port/database

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret

# M-Pesa (Optional)
MPESA_CONSUMER_KEY=your-key
MPESA_CONSUMER_SECRET=your-secret
MPESA_BUSINESS_SHORT_CODE=your-code
MPESA_PASSKEY=your-passkey

# Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-password
```

4. **Initialize database**
```bash
flask db upgrade
```

5. **Run the application**
```bash
python run.py
```

Visit: `http://127.0.0.1:5000`

---

## 🌍 Deployment

### Supabase + Render/Railway
1. Create Supabase project
2. Get PostgreSQL connection string
3. Deploy to Render/Railway
4. Set environment variables
5. Run migrations

---

## 📱 Features by Plan

### **Free Tier**
- 30-day trial
- Up to 10 members
- Basic features
- Community support

### **Basic Plan**
- Up to 50 members
- Full feature access
- Email support
- Monthly/Yearly billing

### **Advanced Plan**
- Up to 200 members
- Priority support
- Advanced analytics
- Custom branding

### **Enterprise**
- Unlimited members
- Dedicated support
- Custom features
- SLA guarantees

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support

- **Website**: https://bwirefinance.cloud
- **Email**: support@bwirefinance.cloud
- **Enterprise**: enterprise@bwirefinance.cloud

---

## 👨‍💼 About Bwire Global Tech

Bwire Finance Cloud is developed and maintained by **Bwire Global Tech**, led by founder **Bilford Bwire**. We're committed to revolutionizing financial management across Africa and beyond.

### Our Mission
Empower individuals, businesses, and communities with accessible, intelligent financial tools that drive economic growth and financial inclusion.

---

## 🎯 Roadmap

- ✅ Core financial management
- ✅ M-Pesa integration
- ✅ Multi-currency support
- ✅ Cloud infrastructure
- 🔄 Mobile apps (iOS/Android)
- 🔄 QR code payments
- 🔄 AI-powered insights
- 🔄 Open Banking APIs

---

**Built with ❤️ by Bwire Global Tech**

*Transforming financial management, one transaction at a time.*
