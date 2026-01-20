# API Quick Reference Guide

## Base URL
```
http://localhost:8000  (Development)
https://yourdomain.com (Production)
```

## Authentication

All authenticated endpoints require either:
- **Session Cookie** (after login via web)
- **Bearer Token** (for API access)

```bash
Authorization: Bearer YOUR_API_TOKEN
```

---

## 🔐 Authentication Endpoints

### Register Company
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

Response 201:
{
  "success": true,
  "company_id": "COMP-20260120123456",
  "user_id": "USER-20260120123456",
  "api_token": "your-api-token-here",
  "trial_days": 14
}
```

### Login
```bash
POST /api/auth/login/
Content-Type: application/json

{
  "email": "juan@abc.com",
  "password": "SecurePass123!"
}

Response 200:
{
  "success": true,
  "user": {
    "id": "USER-20260120123456",
    "email": "juan@abc.com",
    "name": "Juan Dela Cruz",
    "role": "company_admin",
    "company_id": "COMP-20260120123456"
  },
  "api_token": "your-api-token-here"
}
```

### Get Current User
```bash
GET /api/auth/user/
Authorization: Bearer YOUR_API_TOKEN

Response 200:
{
  "user": {
    "id": "USER-20260120123456",
    "email": "juan@abc.com",
    "name": "Juan Dela Cruz",
    "role": "company_admin",
    "company_id": "COMP-20260120123456"
  },
  "company": {
    "id": "COMP-20260120123456",
    "name": "ABC Corporation",
    "email": "admin@abc.com",
    "status": "active"
  },
  "subscription": {
    "status": "trial",
    "trial_end_date": "2026-02-03T08:00:00",
    "agent_count": 10,
    "price_per_agent": 500
  }
}
```

### Logout
```bash
POST /api/auth/logout/
Authorization: Bearer YOUR_API_TOKEN

Response 200:
{
  "success": true,
  "message": "Logged out successfully"
}
```

### Change Password
```bash
POST /api/auth/change-password/
Authorization: Bearer YOUR_API_TOKEN
Content-Type: application/json

{
  "old_password": "OldPass123!",
  "new_password": "NewPass123!"
}

Response 200:
{
  "success": true,
  "message": "Password changed successfully"
}
```

### Create User (Admin Only)
```bash
POST /api/users/create/
Authorization: Bearer YOUR_API_TOKEN
Content-Type: application/json

{
  "email": "maria@abc.com",
  "password": "SecurePass123!",
  "role": "agent",
  "name": "Maria Santos",
  "phone": "+639171234567",
  "related_id": "A001"
}

Response 201:
{
  "success": true,
  "user_id": "USER-20260120123457",
  "api_token": "user-api-token-here"
}
```

---

## 💳 Subscription Endpoints

### Get Subscription Info
```bash
GET /api/subscription/
Authorization: Bearer YOUR_API_TOKEN

Response 200:
{
  "subscription": {
    "_id": "SUB-20260120123456",
    "company_id": "COMP-20260120123456",
    "status": "trial",
    "price_per_agent": 500,
    "current_agent_count": 10,
    "monthly_cost": 5000,
    "next_billing_date": "2026-02-03T08:00:00",
    "trial_end_date": "2026-02-03T08:00:00",
    "billing_cycle": "monthly"
  },
  "is_active": true
}
```

### Get Payment History
```bash
GET /api/subscription/payments/
Authorization: Bearer YOUR_API_TOKEN

Response 200:
{
  "payments": [
    {
      "_id": "INV-COMP-20260120-001",
      "invoice_number": "INV-COMP-20260120-001",
      "amount": 5000,
      "status": "paid",
      "agent_count": 10,
      "due_date": "2026-02-27T08:00:00",
      "payment_date": "2026-02-25T10:30:00",
      "payment_method": "gcash",
      "reference_number": "GC-123456789"
    }
  ]
}
```

### Record Payment (Admin Only)
```bash
POST /api/subscription/record-payment/
Authorization: Bearer YOUR_API_TOKEN
Content-Type: application/json

{
  "invoice_id": "INV-COMP-20260120-001",
  "amount_paid": 2990,
  "payment_method": "gcash",
  "reference_number": "GC-123456789",
  "notes": "Payment via GCash"
}

Response 200:
{
  "success": true,
  "message": "Payment recorded successfully"
}
```

### Generate Invoices (Super Admin Only)
```bash
POST /api/subscription/generate-invoices/
Authorization: Bearer YOUR_API_TOKEN

Response 200:
{
  "success": true,
  "message": "Generated 15 invoices"
}
```

---

## 👥 Agent Endpoints

### List Agents
```bash
GET /api/agents/
Authorization: Bearer YOUR_API_TOKEN

Response 200:
{
  "agents": [
    {
      "_id": "A001",
      "name": "Maria Santos",
      "email": "maria@abc.com",
      "monthly_target": 500000,
      "company_id": "COMP-20260120123456",
      "area_manager_id": "AM001",
      "performance_score": 85.5,
      "prediction": "HIT"
    }
  ]
}
```

### Get Agent Details
```bash
GET /api/agents/A001/
Authorization: Bearer YOUR_API_TOKEN

Response 200:
{
  "agent": {
    "_id": "A001",
    "name": "Maria Santos",
    "email": "maria@abc.com",
    "monthly_target": 500000,
    "company_id": "COMP-20260120123456"
  },
  "performance": {
    "calls": 45,
    "meetings": 12,
    "leads": 8,
    "deals": 3,
    "sales_total": 350000,
    "target_progress": 70.0,
    "prediction": "HIT"
  }
}
```

---

## 📊 Dashboard Endpoints

### Company Dashboard
```bash
GET /
Authorization: Bearer YOUR_API_TOKEN

Returns HTML dashboard with:
- All agents in company
- Performance overview
- AI predictions
- Recent activities
```

### Area Manager Dashboard
```bash
GET /area-manager/<manager_id>/
Authorization: Bearer YOUR_API_TOKEN

Returns dashboard for specific area manager
```

### Division Head Dashboard
```bash
GET /division-head/<head_id>/
Authorization: Bearer YOUR_API_TOKEN

Returns dashboard for specific division head
```

---

## 🔑 Payment Methods

Valid payment method values:
- `gcash`
- `paymaya`
- `bank_transfer`
- `credit_card`
- `cash`
- `check`

---

## 🔒 User Roles

Valid role values:
- `super_admin` - Platform administrator
- `company_admin` - Company owner/manager
- `division_head` - Division head
- `area_manager` - Area manager
- `agent` - Sales agent

---

## ⚠️ Error Responses

### 401 Unauthorized
```json
{
  "error": "Authentication required",
  "message": "Please login to access this resource"
}
```

### 403 Forbidden
```json
{
  "error": "Insufficient permissions",
  "message": "This action requires company_admin role or higher"
}
```

### 403 Subscription Inactive
```json
{
  "error": "Subscription inactive",
  "message": "Your company subscription is not active",
  "subscription_url": "/subscription/manage/"
}
```

### 400 Bad Request
```json
{
  "error": "Missing required fields",
  "required": ["email", "password"]
}
```

### 404 Not Found
```json
{
  "error": "Resource not found",
  "message": "Agent with ID A999 not found"
}
```

---

## 📝 Usage Examples

### Python Example
```python
import requests

# Login
response = requests.post('http://localhost:8000/api/auth/login/', json={
    'email': 'juan@abc.com',
    'password': 'SecurePass123!'
})
data = response.json()
token = data['api_token']

# Get subscription info
response = requests.get(
    'http://localhost:8000/api/subscription/',
    headers={'Authorization': f'Bearer {token}'}
)
subscription = response.json()
print(f"Monthly cost: ₱{subscription['subscription']['monthly_cost']}")
```

### JavaScript Example
```javascript
// Login
const loginResponse = await fetch('http://localhost:8000/api/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'juan@abc.com',
    password: 'SecurePass123!'
  })
});
const loginData = await loginResponse.json();
const token = loginData.api_token;

// Get agents
const agentsResponse = await fetch('http://localhost:8000/api/agents/', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const agents = await agentsResponse.json();
console.log(agents);
```

### cURL Example
```bash
# Login
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"juan@abc.com","password":"SecurePass123!"}' \
  | jq -r '.api_token')

# Get subscription
curl http://localhost:8000/api/subscription/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🚀 Rate Limits

Currently no rate limits. Will be added in production:
- 100 requests per minute per user
- 1000 requests per hour per company

---

## 📞 Support

For API support:
- Technical documentation: SUBSCRIPTION_SYSTEM.md
- Email: api-support@yourdomain.com
- Issues: GitHub Issues

