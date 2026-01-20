# 🇵🇭 Setup Guide for Philippine Companies

## Quick Start for Philippine Businesses

This system is designed specifically for Philippine companies that want to track their sales agents' performance with AI-powered predictions.

## Pricing

**₱500 per agent per month**
- Only pay for active agents
- 14-day free trial
- No setup fees
- Cancel anytime

### Example Pricing
- **10 agents**: ₱2,990/month
- **25 agents**: ₱7,475/month
- **50 agents**: ₱14,950/month
- **100 agents**: ₱29,900/month

## System Requirements

1. **Internet connection**
2. **Modern web browser** (Chrome, Firefox, Edge)
3. **Company information**:
   - Company name
   - Business address
   - TIN (Tax Identification Number)
   - Contact person details

## Registration Process

### Step 1: Company Registration

Visit the registration page and provide:

```
Company Information:
- Company Name: Your Business Name Inc.
- Email: admin@yourcompany.com
- Phone: +639171234567
- Address: Your business address in Philippines
- TIN: 123-456-789-000 (your BIR TIN)
- Business Type: (e.g., Banking, Insurance, Real Estate)

Admin Account:
- Name: Juan Dela Cruz
- Email: juan@yourcompany.com
- Password: (create a secure password)
- Phone: +639171234567
```

### Step 2: Trial Period

- You get **14 days free trial**
- Add your agents and start using the system
- No credit card required for trial

### Step 3: Add Your Team

After registration, you can add:

1. **Division Heads** - Oversee multiple area managers
2. **Area Managers** - Manage multiple agents
3. **Agents** - Your sales force

Each person gets their own login account with appropriate permissions.

### Step 4: Track Performance

The system automatically:
- Tracks agent activities (calls, meetings, leads)
- Records sales and commissions
- Calculates performance scores
- Predicts which agents need help

## Payment Methods

We accept the following payment methods:

1. **GCash** ✅
2. **PayMaya** ✅
3. **Bank Transfer** ✅
4. **Credit Card** ✅
5. **Check** ✅
6. **Cash** (at office) ✅

### How Billing Works

1. **Monthly Billing**: You're billed on the same day each month
2. **Agent-Based**: Only pay for active agents
3. **Invoice Generation**: Automatic invoice sent to your email
4. **Payment Period**: 7 days to pay after invoice
5. **Grace Period**: 3 days grace period after due date

### Example Bill

```
Invoice #INV-COMP-20260120-001
Billing Period: Jan 20, 2026 - Feb 20, 2026

Active Agents: 15
Rate per Agent: ₱500
Total Amount: ₱7,500

Due Date: Feb 27, 2026
Payment Method: GCash / Bank Transfer / Others
```

## Adding Agents

### Option 1: Via Web Interface

1. Login as Company Admin
2. Go to "Agents" section
3. Click "Add New Agent"
4. Fill in agent details:
   - Name
   - Email
   - Monthly Target (in Pesos)
   - Assigned Area Manager

### Option 2: Via API

```python
import requests

response = requests.post('http://yourdomain.com/api/agents/', 
    headers={'Authorization': 'Bearer YOUR_API_TOKEN'},
    json={
        "agent_id": "A001",
        "name": "Maria Santos",
        "email": "maria@yourcompany.com",
        "monthly_target": 500000,  # ₱500,000
        "area_manager_id": "AM001"
    }
)
```

## User Roles Explained

### 1. Company Admin
**Access**: Everything
- Manage subscription and billing
- Add/remove users
- View all reports
- Configure settings

### 2. Division Head
**Access**: Division level
- View all area managers in division
- View all agents in division
- Performance reports
- Cannot modify subscription

### 3. Area Manager
**Access**: Area level
- View agents in their area
- Track agent performance
- Add activities and sales
- Cannot access other areas

### 4. Agent
**Access**: Personal only
- View own performance
- Log activities
- View own sales history
- Cannot see other agents

## Philippine-Specific Features

### Timezone
- All dates/times in **Philippine Time (PHT/PST)**
- Automatic daylight saving adjustment

### Currency
- All amounts in **Philippine Peso (₱)**
- Formatted with Philippine number format
- Example: ₱1,234,567.89

### Compliance
- TIN field for BIR compliance
- Official receipts generation ready
- VAT-compliant invoicing

### Local Support
- Business hours: 8:00 AM - 6:00 PM PHT
- Support in English and Filipino
- Local phone support: +63 XXX XXX XXXX

## Common Questions

### Q: What happens after the 14-day trial?
**A**: You'll receive an email reminder 3 days before trial ends. After trial, you'll be billed monthly based on your active agents.

### Q: Can I cancel anytime?
**A**: Yes! You can cancel anytime. You'll have access until the end of your billing period.

### Q: What if I add/remove agents mid-month?
**A**: Your next invoice will reflect the current number of active agents. We count agents at the time of billing.

### Q: Is my data secure?
**A**: Yes! Your company data is completely isolated from other companies. We use bank-level security.

### Q: Can I export my data?
**A**: Yes, you can export all your data (agents, sales, activities) anytime.

### Q: Do you provide training?
**A**: Yes! We provide free onboarding training for all Company Admins.

### Q: What if I forget my password?
**A**: Use the "Forgot Password" link on the login page. A reset link will be sent to your email.

### Q: Can multiple people access the same account?
**A**: Each person should have their own account with appropriate role. Don't share login credentials.

## Technical Setup (For Developers)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd rada

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your MongoDB URI

# Run the server
python manage.py runserver
```

### Environment Variables

```env
# MongoDB (Required)
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/sales_ai

# Django (Required)
SECRET_KEY=your-secret-key-here
DEBUG=False

# Subscription (Optional - has defaults)
PRICE_PER_AGENT=500
TRIAL_DAYS=14

# Email Notifications (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=notifications@yourcompany.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
```

### Database Collections

The system automatically creates these MongoDB collections:
- `companies` - Company information
- `subscriptions` - Subscription details
- `payments` - Invoices and payments
- `users` - User accounts
- `agents` - Sales agents
- `activities` - Agent activities
- `sales` - Sales records
- `area_managers` - Area managers
- `division_heads` - Division heads
- `products` - Product catalog
- `leads` - Sales leads

## Support & Contact

**Email**: support@yourcompany.com
**Phone**: +63 XXX XXX XXXX
**Business Hours**: Monday-Friday, 8:00 AM - 6:00 PM PHT

**Documentation**: See SUBSCRIPTION_SYSTEM.md for detailed technical documentation

---

## Getting Started Checklist

- [ ] Register your company
- [ ] Verify email address
- [ ] Add Division Heads (if applicable)
- [ ] Add Area Managers
- [ ] Add Sales Agents
- [ ] Import your products
- [ ] Train your team on the system
- [ ] Start tracking activities
- [ ] Review first performance reports
- [ ] Setup payment method before trial ends

**Welcome to the future of sales performance management!** 🇵🇭

