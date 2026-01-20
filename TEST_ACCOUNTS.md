# 🧪 Test Accounts for SalesAI System

## Overview
This document contains the test account credentials for testing the role-based authentication system.

**Test Company:** Test Company Inc.  
**Company ID:** COMP-TEST001  
**Subscription:** 14-day free trial (₱500/agent/month)

---

## 🔐 Test Account Credentials

### 👨‍💼 Company Admin
- **Name:** Admin User
- **Email:** `admin@test.com`
- **Password:** `admin123`
- **Role:** Company Admin
- **Access:**
  - Full system access
  - User management
  - Dashboard: `/dashboard/`
  - Can create users at: `/users/`

---

### 👔 Division Head
- **Name:** John Division
- **Email:** `division@test.com`
- **Password:** `division123`
- **Role:** Division Head
- **Division:** NCR Division
- **Access:**
  - Division oversight
  - View area managers and agents
  - Dashboard: `/division-head/dashboard/`

---

### 👨‍💻 Area Manager
- **Name:** Maria Manager
- **Email:** `manager@test.com`
- **Password:** `manager123`
- **Role:** Area Manager
- **Area:** Manila Area
- **Reports to:** John Division (Division Head)
- **Access:**
  - Team management
  - View agents under supervision
  - Dashboard: `/area-manager/dashboard/`

---

### 👤 Sales Agent
- **Name:** Pedro Agent
- **Email:** `agent@test.com`
- **Password:** `agent123`
- **Role:** Sales Agent
- **Reports to:** Maria Manager (Area Manager)
- **Monthly Target:** ₱100,000
- **Access:**
  - Personal performance dashboard
  - View own metrics and AI predictions
  - Dashboard: `/agent/dashboard/`

---

## 🧪 How to Test

### 1. Access the Login Page
Visit: https://salesai-system.onrender.com/login/

### 2. Test Each Role
For each account:
1. Select the appropriate role from the role selector
2. Enter the email and password
3. Click "Sign In"
4. Verify you're redirected to the correct dashboard

### 3. Test Role Validation
Try logging in with the wrong role selected to verify the system validates role matching.

### 4. Test User Management (Company Admin Only)
1. Login as `admin@test.com`
2. Navigate to `/users/`
3. View existing users
4. Try creating a new user

---

## 🔄 Regenerating Test Accounts

If you need to regenerate the test accounts:

```bash
python create_test_accounts.py
```

This script will:
- Create a test company if it doesn't exist
- Create organizational hierarchy (Division Head → Area Manager → Agent)
- Create user accounts for all 4 roles
- Link users to their respective profiles

---

## 🗑️ Cleaning Up Test Data

To remove test accounts (use with caution):

```python
# In Django shell or create a cleanup script
from core.models import User, Company, Agent, AreaManager, DivisionHead, Subscription
from core.database import db

# Delete test company and all related data
company_id = "COMP-TEST001"
db.users.delete_many({"company_id": company_id})
db.agents.delete_many({"company_id": company_id})
db.area_managers.delete_many({"company_id": company_id})
db.division_heads.delete_many({"company_id": company_id})
db.subscriptions.delete_many({"company_id": company_id})
db.companies.delete_one({"_id": company_id})
```

---

## 📊 Organizational Structure

```
Test Company Inc. (COMP-TEST001)
│
├── 👨‍💼 Admin User (Company Admin)
│   └── Can manage all users
│
├── 👔 John Division (Division Head)
│   └── NCR Division
│       │
│       └── 👨‍💻 Maria Manager (Area Manager)
│           └── Manila Area
│               │
│               └── 👤 Pedro Agent (Sales Agent)
│                   └── Target: ₱100,000/month
```

---

## 🔒 Security Notes

⚠️ **Important:**
- These are **test accounts only**
- **DO NOT use in production**
- Passwords are simple for testing purposes
- In production, use strong passwords and proper password policies
- Consider removing these accounts before going live

---

## 📝 Next Steps

After testing:
1. ✅ Verify each role can log in
2. ✅ Check dashboard access is correct
3. ✅ Test user management features
4. ✅ Verify role-based permissions
5. ✅ Test logout functionality
6. ⚠️ Remove test accounts before production deployment

---

**Last Updated:** 2026-01-20  
**Created By:** SalesAI Development Team
