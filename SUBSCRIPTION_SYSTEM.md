# 🇵🇭 Multi-Tenant Subscription System Documentation

## Overview
This system has been transformed into a **multi-tenant SaaS platform** for Philippine companies with **per-agent pricing** model.

## Pricing Model
- **₱500 per agent per month**
- Companies are billed based on the number of active agents they have
- 14-day free trial for new companies
- Monthly billing cycle

## Key Features

### 1. Multi-Tenancy
- Each company is a separate tenant with isolated data
- All models include `company_id` for data segregation
- Automatic data filtering based on user's company

### 2. User Roles & Permissions
- **Super Admin**: Platform administrator (manages all companies)
- **Company Admin**: Company owner (manages subscription, users, all data)
- **Division Head**: Views division performance
- **Area Manager**: Manages agents in their area
- **Agent**: Views own performance only

### 3. Subscription Management
- Automatic agent count tracking
- Trial period management (14 days)
- Invoice generation
- Payment tracking
- Subscription status: `trial`, `active`, `past_due`, `cancelled`, `expired`

### 4. Authentication
- Email/password authentication
- API token authentication (Bearer token)
- Session-based authentication
- Role-based access control

### 5. Philippine-Specific Features
- Timezone: `Asia/Manila`
- Currency: PHP (₱)
- TIN (Tax Identification Number) field for companies
- Local payment methods support (GCash, PayMaya, Bank Transfer)

## Database Collections

### New Collections

#### companies
```json
{
  "_id": "COMP-20260120123456",
  "name": "ABC Corporation",
  "email": "admin@abc.com",
  "phone": "+639171234567",
  "address": "Manila, Philippines",
  "tin": "123-456-789-000",
  "business_type": "Banking",
  "contact_person": "Juan Dela Cruz",
  "status": "active",
  "created_at": "2026-01-20T08:00:00",
  "updated_at": "2026-01-20T08:00:00"
}
```

#### subscriptions
```json
{
  "_id": "SUB-20260120123456",
  "company_id": "COMP-20260120123456",
  "status": "trial",
  "billing_email": "billing@abc.com",
  "price_per_agent": 500,
  "current_agent_count": 10,
  "billing_cycle": "monthly",
  "start_date": "2026-01-20T08:00:00",
  "trial_end_date": "2026-02-03T08:00:00",
  "next_billing_date": "2026-02-03T08:00:00",
  "created_at": "2026-01-20T08:00:00",
  "updated_at": "2026-01-20T08:00:00"
}
```

#### payments
```json
{
  "_id": "INV-COMP-20260120-001",
  "company_id": "COMP-20260120123456",
  "invoice_number": "INV-COMP-20260120-001",
  "amount": 2990,
  "agent_count": 10,
  "billing_period_start": "2026-01-20T08:00:00",
  "billing_period_end": "2026-02-20T08:00:00",
  "due_date": "2026-02-27T08:00:00",
  "status": "pending",
  "currency": "PHP",
  "created_at": "2026-01-20T08:00:00"
}
```

#### users
```json
{
  "_id": "USER-20260120123456",
  "email": "juan@abc.com",
  "password": "hashed_password",
  "role": "company_admin",
  "company_id": "COMP-20260120123456",
  "name": "Juan Dela Cruz",
  "phone": "+639171234567",
  "related_id": null,
  "is_active": true,
  "api_token": "secure_random_token",
  "last_login": "2026-01-20T08:00:00",
  "created_at": "2026-01-20T08:00:00"
}
```

### Updated Collections
All existing collections now include `company_id`:
- `agents`
- `activities`
- `sales`
- `area_managers`
- `division_heads`
- `products`
- `leads`

## API Endpoints

### Authentication

#### Register Company
```bash
POST /api/auth/register/
Content-Type: application/json

{
  "company_name": "ABC Corporation",
  "company_email": "admin@abc.com",
  "company_phone": "+639171234567",
  "company_address": "Manila, Philippines",
  "tin": "123-456-789-000",
  "business_type": "Banking",
  "admin_name": "Juan Dela Cruz",
  "admin_email": "juan@abc.com",
  "admin_password": "SecurePass123!",
  "admin_phone": "+639171234567"
}
```

#### Login
```bash
POST /api/auth/login/
Content-Type: application/json

{
  "email": "juan@abc.com",
  "password": "SecurePass123!"
}
```

#### Get Current User
```bash
GET /api/auth/user/
Authorization: Bearer {api_token}
```

### Subscription Management

#### Get Subscription Info
```bash
GET /api/subscription/
Authorization: Bearer {api_token}
```

#### Get Payment History
```bash
GET /api/subscription/payments/
Authorization: Bearer {api_token}
```

#### Record Payment (Admin only)
```bash
POST /api/subscription/record-payment/
Authorization: Bearer {api_token}
Content-Type: application/json

{
  "invoice_id": "INV-COMP-20260120-001",
  "amount_paid": 2990,
  "payment_method": "gcash",
  "reference_number": "GC-123456789",
  "notes": "Payment via GCash"
}
```

#### Generate Invoices (Super Admin only)
```bash
POST /api/subscription/generate-invoices/
Authorization: Bearer {api_token}
```

## Usage Examples

### 1. Register a New Company
```python
import requests

response = requests.post('http://localhost:8000/api/auth/register/', json={
    "company_name": "TechStart Philippines",
    "company_email": "info@techstart.ph",
    "company_phone": "+639171234567",
    "company_address": "Makati City, Metro Manila",
    "tin": "123-456-789-000",
    "business_type": "Technology",
    "admin_name": "Maria Santos",
    "admin_email": "maria@techstart.ph",
    "admin_password": "SecurePass123!",
    "admin_phone": "+639171234567"
})

print(response.json())
# Returns: api_token, company_id, user_id, trial_days
```

### 2. Create an Agent (with Multi-Tenancy)
```python
from core.models import Agent

# company_id is automatically set from authenticated user
agent = Agent.create(
    agent_id="A001",
    name="Pedro Reyes",
    email="pedro@techstart.ph",
    monthly_target=500000,
    company_id=request.company_id,  # From middleware
    area_manager_id="AM001"
)

# Subscription agent count is automatically updated
```

### 3. Check Subscription Status
```python
from core.models import Subscription

company_id = "COMP-20260120123456"
is_active = Subscription.is_active(company_id)

if not is_active:
    print("Subscription expired or inactive")
else:
    monthly_cost = Subscription.calculate_monthly_cost(company_id)
    print(f"Monthly cost: ₱{monthly_cost:,.2f}")
```

## Middleware

### AuthenticationMiddleware
- Authenticates users via session or API token
- Adds `request.user` to all requests
- Returns 401 for unauthenticated requests on protected routes

### MultiTenantMiddleware
- Adds `request.company_id` based on authenticated user
- Ensures data isolation between companies

### SubscriptionMiddleware
- Checks if company subscription is active
- Returns 403 for inactive subscriptions
- Bypasses check for super admins

## Payment Methods Supported

1. **GCash** - `gcash`
2. **PayMaya** - `paymaya`
3. **Bank Transfer** - `bank_transfer`
4. **Credit Card** - `credit_card`
5. **Cash** - `cash`
6. **Check** - `check`

## Environment Variables

```env
# MongoDB Configuration
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/sales_ai

# Django Configuration
SECRET_KEY=your-secret-key
DEBUG=True

# Subscription Configuration
PRICE_PER_AGENT=500
TRIAL_DAYS=14

# Payment Gateway (Optional)
PAYMONGO_SECRET_KEY=sk_test_...
PAYMONGO_PUBLIC_KEY=pk_test_...

# Email Configuration (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=notifications@yourdomain.com
EMAIL_HOST_PASSWORD=your-password
EMAIL_USE_TLS=True
```

## Business Metrics

### Monthly Recurring Revenue (MRR)
```python
from core.models import Payment

mrr = Payment.get_monthly_recurring_revenue()
print(f"MRR: ₱{mrr:,.2f}")
```

### Total Revenue
```python
from datetime import datetime
from core.models import Payment

start_date = datetime(2026, 1, 1)
end_date = datetime(2026, 1, 31)

revenue = Payment.get_total_revenue(start_date, end_date)
print(f"January Revenue: ₱{revenue:,.2f}")
```

## Next Steps for Production

1. **Payment Gateway Integration**
   - Integrate PayMongo or other PH payment gateway
   - Add webhook handlers for automatic payment confirmation

2. **Email Notifications**
   - Trial expiration reminders
   - Invoice generation notifications
   - Payment confirmations
   - Subscription status changes

3. **Automated Billing**
   - Cron job for invoice generation
   - Automatic subscription expiration
   - Payment retry logic

4. **Admin Dashboard**
   - Company management interface
   - Revenue analytics
   - Subscription monitoring

5. **Security Enhancements**
   - Rate limiting
   - IP whitelisting
   - 2FA for admin accounts

## Support

For questions or issues, contact the development team.

---

**Built for Philippine Companies** 🇵🇭
