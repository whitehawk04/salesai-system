# ⚡ Quick Start - Get Running in 10 Minutes

## 🎯 Goal
Get your AI Sales Performance System running with MongoDB Atlas.

---

## 📋 Checklist (Follow in Order)

### ✅ Step 1: Create MongoDB Atlas Account (2 min)
```
1. Visit: https://www.mongodb.com/cloud/atlas/register
2. Sign up with email or Google
3. Verify your email
```

### ✅ Step 2: Create Free Database (3 min)
```
1. Click "Build a Database"
2. Choose "M0 FREE" (free forever!)
3. Select any cloud provider & region
4. Click "Create"
5. Wait 1-3 minutes for cluster creation
```

### ✅ Step 3: Create Database User (1 min)
```
1. Username: salesai_user
2. Click "Autogenerate Secure Password"
3. 📝 COPY AND SAVE THE PASSWORD!
4. Select "Read and write to any database"
5. Click "Add User"
```

### ✅ Step 4: Allow Network Access (1 min)
```
1. Click "Network Access"
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere"
4. Confirm (IP: 0.0.0.0/0)
```

### ✅ Step 5: Get Connection String (1 min)
```
1. Click "Database" in sidebar
2. Click "Connect" button
3. Choose "Connect your application"
4. Copy the connection string
5. Replace <password> with your actual password
```

**Your connection string looks like:**
```
mongodb+srv://salesai_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### ✅ Step 6: Create .env File (30 sec)
```
1. In your project folder, create file named: .env
2. Add this line (with YOUR connection string):

MONGODB_URI=mongodb+srv://salesai_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/sales_ai?retryWrites=true&w=majority
SECRET_KEY=django-insecure-your-secret-key-12345
DEBUG=True

3. Save the file
```

**⚠️ IMPORTANT:** Add `/sales_ai` before the `?` in the connection string!

### ✅ Step 7: Test Connection (10 sec)
```bash
python test_mongodb_connection.py
```

**Expected output:**
```
✅ Successfully connected to MongoDB!
📊 Available databases: ['admin', 'local']
```

### ✅ Step 8: Setup Demo Data (30 sec)
```bash
python tmp_rovodev_quick_setup.py
```

**This creates:**
- 6 sample agents
- 200+ activities
- 50+ sales records
- Trains AI model

### ✅ Step 9: Start Django Server (5 sec)
```bash
python manage.py runserver
```

### ✅ Step 10: Open Dashboard! 🎉
```
Open browser: http://localhost:8000
```

**You should see:**
- 6 agents with performance data
- Risk badges (HIGH/MEDIUM/LOW)
- AI predictions (HIT/MISS)
- Sales progress bars
- Beautiful minimalist design!

---

## 🆘 Troubleshooting

### ❌ "ServerSelectionTimeoutError"
**Fix:** 
- Check .env file exists in project root
- Verify password in connection string is correct
- Ensure Network Access allows 0.0.0.0/0

### ❌ "Authentication failed"
**Fix:**
- Double-check password (no typos)
- Make sure username is correct
- Recreate database user if needed

### ❌ ".env file not found"
**Fix:**
- File must be in project root (same folder as manage.py)
- File name must be exactly `.env` (not `env.txt`)

---

## 📞 Need Help?

**Test your connection:**
```bash
python test_mongodb_connection.py
```

**Read detailed guide:**
```
MONGODB_SETUP_GUIDE.md
```

**Check if .env is correct:**
```bash
cat .env
```
or on Windows:
```bash
type .env
```

---

## ✨ After Setup

Once running, you can:
1. ✅ View 6 sample agents
2. ✅ See AI predictions
3. ✅ Check risk assessments
4. ✅ Train the model at /train/
5. ✅ Add your own agents
6. ✅ Start building the hierarchy system!

---

## 🎯 Example .env File

```env
MONGODB_URI=mongodb+srv://salesai_user:MySecurePass123@cluster0.abc12.mongodb.net/sales_ai?retryWrites=true&w=majority
SECRET_KEY=django-insecure-change-in-production-12345
DEBUG=True
```

**Make sure:**
- No spaces around the `=`
- `/sales_ai` is before the `?`
- Password has no special characters that need escaping

---

## 🚀 Commands Summary

```bash
# Test MongoDB connection
python test_mongodb_connection.py

# Setup demo data and train AI
python tmp_rovodev_quick_setup.py

# Start Django server
python manage.py runserver

# Open in browser
http://localhost:8000
```

---

**Total Time: ~10 minutes**
**Difficulty: Easy**
**Cost: $0 (completely free)**

Let's get started! 🎉
