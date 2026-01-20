# 🇵🇭 AI-Powered Sales Performance System for Philippine Companies

A **multi-tenant SaaS platform** for Philippine businesses to track sales agent performance with AI-powered predictions and insights.

## 💰 Pricing: ₱500 per agent/month

- **14-day FREE trial** - No credit card required
- **Per-agent pricing** - Only pay for active agents
- **Philippine payment methods** - GCash, PayMaya, Bank Transfer, Credit Card
- **Cancel anytime** - No long-term contracts

## ✨ Features

### For Company Admins
- Multi-tenant data isolation
- Subscription management
- User and role management
- Company-wide analytics

### For Managers
- Track sales agents and their activities (calls, meetings, leads, sales)
- Calculate performance scores in real-time
- AI-powered predictions to identify agents at risk of missing targets
- Hierarchical dashboards (Division Head → Area Manager → Agent)

### For Agents
- Personal performance dashboard
- Activity logging
- Sales tracking
- Target progress monitoring

## 🏗️ Tech Stack
- Python 3.8+
- Django 4.2
- MongoDB Atlas (Cloud database)
- Scikit-learn (AI/ML)
- Pandas (Data analysis)

## 🚀 Quick Start

### For Philippine Businesses (Non-Technical)

👉 **See [SETUP_GUIDE_PHILIPPINES.md](SETUP_GUIDE_PHILIPPINES.md)** for step-by-step registration and usage guide.

### For Developers

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Configure MongoDB
Create a free MongoDB Atlas account at https://www.mongodb.com/cloud/atlas
- Create a cluster
- Create a database named `sales_ai`
- Get your connection string

#### 3. Configure Environment Variables
Copy `.env.example` to `.env` and update:
```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/sales_ai
SECRET_KEY=your-secret-key-here
DEBUG=True
PRICE_PER_AGENT=500
TRIAL_DAYS=14
```

#### 4. Run Django Server
```bash
cd rada
python manage.py runserver
```

#### 5. Register Your Company
Navigate to: http://localhost:8000/register/

#### 6. Access the Dashboard
Login at: http://localhost:8000/login/

## 📊 Multi-Tenant Architecture

### New Collections for SaaS

#### companies
```json
{
  "_id": "COMP-20260120123456",
  "name": "TechStart Philippines",
  "email": "info@techstart.ph",
  "phone": "+639171234567",
  "address": "Makati City, Metro Manila",
  "tin": "123-456-789-000",
  "status": "active"
}
```

#### subscriptions
```json
{
  "_id": "SUB-20260120123456",
  "company_id": "COMP-20260120123456",
  "status": "trial",
  "price_per_agent": 500,
  "current_agent_count": 15,
  "trial_end_date": "2026-02-03T08:00:00"
}
```

#### payments
```json
{
  "_id": "INV-COMP-20260120-001",
  "company_id": "COMP-20260120123456",
  "amount": 4485,
  "agent_count": 15,
  "status": "paid",
  "payment_method": "gcash"
}
```

#### users
```json
{
  "_id": "USER-20260120123456",
  "email": "juan@techstart.ph",
  "role": "company_admin",
  "company_id": "COMP-20260120123456",
  "api_token": "secure_token"
}
```

### Updated Collections (with company_id)

All existing collections now support multi-tenancy:
- `agents` - Sales agents (with company_id)
- `activities` - Agent activities (with company_id)
- `sales` - Sales records (with company_id)
- `area_managers` - Area managers (with company_id)
- `division_heads` - Division heads (with company_id)
- `products` - Product catalog (with company_id)
- `leads` - Sales leads (with company_id)

## 🔐 Authentication & Authorization

### User Roles Hierarchy
1. **Super Admin** - Platform administrator
2. **Company Admin** - Company owner/manager
3. **Division Head** - Oversees multiple area managers
4. **Area Manager** - Manages multiple agents
5. **Agent** - Sales representative

### API Authentication
```bash
# Using Bearer Token
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
     http://localhost:8000/api/subscription/
```

## 🤖 AI-Powered Predictions

### Performance Formula
The system calculates performance based on:
- Number of calls made
- Number of meetings held
- Number of leads generated
- Number of deals closed
- Sales amount vs target

### AI Prediction
Uses RandomForestClassifier to predict:
- **HIT**: Agent likely to meet target 🎯
- **MISS**: Agent at risk of missing target ⚠️

## 📱 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new company
- `POST /api/auth/login/` - User login
- `GET /api/auth/user/` - Get current user
- `POST /api/auth/logout/` - Logout

### Subscription Management
- `GET /api/subscription/` - Get subscription info
- `GET /api/subscription/payments/` - Payment history
- `POST /api/subscription/record-payment/` - Record payment (admin)

### Agent Management
- `GET /api/agents/` - List all agents (filtered by company)
- `POST /api/agents/` - Create new agent
- `GET /api/agents/<id>/` - Get agent details

See **[SUBSCRIPTION_SYSTEM.md](SUBSCRIPTION_SYSTEM.md)** for complete API documentation.

## 📁 Project Structure
```
rada/
├── manage.py
├── salesAI/
│   ├── settings.py          # Django settings (PH timezone, currency)
│   ├── urls.py              # Main URL routing
│   └── wsgi.py
└── core/
    ├── models/
    │   ├── company.py       # Company/tenant model
    │   ├── subscription.py  # Subscription management
    │   ├── payment.py       # Payment & invoicing
    │   ├── user.py          # User authentication
    │   ├── agent.py         # Sales agents
    │   ├── activity.py      # Agent activities
    │   ├── sale.py          # Sales records
    │   └── ...
    ├── middleware.py        # Auth & multi-tenant middleware
    ├── views.py             # Dashboard views
    ├── views_auth.py        # Authentication views
    ├── views_subscription.py # Subscription views
    ├── ai/
    │   └── trainer.py       # AI model training
    ├── services/            # Business logic
    ├── templates/           # HTML templates
    └── urls.py              # URL routing
```

## 📚 Documentation

- **[SETUP_GUIDE_PHILIPPINES.md](SETUP_GUIDE_PHILIPPINES.md)** - Non-technical setup guide for PH businesses
- **[SUBSCRIPTION_SYSTEM.md](SUBSCRIPTION_SYSTEM.md)** - Complete technical documentation
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment guide

## 💳 Subscription Features

### What's Included
✅ Unlimited data storage per company  
✅ AI-powered performance predictions  
✅ Multi-level hierarchy support  
✅ Real-time dashboards  
✅ Mobile-responsive interface  
✅ Data export capabilities  
✅ Email notifications  
✅ Technical support  

### Pricing Examples
- **Small Team (10 agents)**: ₱2,990/month
- **Medium Team (25 agents)**: ₱7,475/month
- **Large Team (50 agents)**: ₱14,950/month
- **Enterprise (100+ agents)**: ₱29,900+/month

## 🛠️ For Developers

### Running Tests
```bash
python manage.py test
```

### Creating a Super Admin
```python
from core.models import User

User.create(
    user_id="SUPERADMIN001",
    email="admin@platform.com",
    password="SecurePassword123!",
    role=User.ROLE_SUPER_ADMIN,
    name="Platform Admin"
)
```

### Generating Invoices (Scheduled Task)
```python
from core.views_subscription import generate_invoices

# Run this monthly via cron job
generate_invoices(request)
```

## 🤝 Support

**For Philippine Businesses:**
- Setup assistance: See SETUP_GUIDE_PHILIPPINES.md
- Technical support: support@yourdomain.com
- Sales inquiries: sales@yourdomain.com

**For Developers:**
- Technical docs: SUBSCRIPTION_SYSTEM.md
- Issues: Create a GitHub issue
- Contributions: Pull requests welcome

## 📄 License
MIT

---

**Built for Philippine Companies** 🇵🇭  
**Powered by AI** 🤖  
**Designed for Growth** 📈
