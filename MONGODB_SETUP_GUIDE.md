# 🔌 MongoDB Atlas Setup - Step-by-Step Guide

## Quick Setup (5-10 minutes)

Follow these steps to get your free MongoDB database running.

---

## Step 1: Create MongoDB Atlas Account

1. **Visit:** https://www.mongodb.com/cloud/atlas/register

2. **Sign Up:**
   - Enter your email address
   - Create a password
   - Click "Create your Atlas account"
   - Or sign up with Google

3. **Verify Email:**
   - Check your email inbox
   - Click the verification link

---

## Step 2: Create a Free Cluster

1. **Choose Deployment Type:**
   - Click "Build a Database"
   - Select **"M0 FREE"** (This is completely free forever!)

2. **Choose Cloud Provider & Region:**
   - Provider: AWS, Google Cloud, or Azure (any is fine)
   - Region: Choose closest to you for better speed
   - Click "Create"

3. **Wait for Cluster Creation:**
   - Takes about 1-3 minutes
   - You'll see "Cluster0" being created

---

## Step 3: Set Up Database Access

### Create Database User:

1. **Security QuickStart will appear:**
   - Or go to: Database Access → Add New Database User

2. **Create User:**
   - Authentication Method: Password
   - Username: `salesai_user` (or your choice)
   - Password: Click "Autogenerate Secure Password" 
     - **IMPORTANT: Copy this password!** You'll need it
   - Or create your own password (save it somewhere!)

3. **Database User Privileges:**
   - Select: "Read and write to any database"
   - Click "Add User"

---

## Step 4: Set Up Network Access

### Allow Connections:

1. **Go to Network Access:**
   - Click "Network Access" in left sidebar
   - Click "Add IP Address"

2. **Choose Option:**
   
   **Option A: Allow from Anywhere (Easy for testing)**
   - Click "Allow Access from Anywhere"
   - IP: `0.0.0.0/0`
   - Click "Confirm"
   - ⚠️ This works everywhere but is less secure

   **Option B: Add Your Current IP (More Secure)**
   - Click "Add Current IP Address"
   - Your IP will be auto-detected
   - Click "Confirm"
   - Note: You'll need to update this if your IP changes

---

## Step 5: Get Your Connection String

1. **Go to Database:**
   - Click "Database" in left sidebar
   - Click "Connect" button on your cluster

2. **Choose Connection Method:**
   - Click "Connect your application"

3. **Copy Connection String:**
   - Driver: Python
   - Version: 3.12 or later
   - Copy the connection string (looks like):
   ```
   mongodb+srv://salesai_user:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

4. **Replace `<password>`:**
   - Replace `<password>` with the password you created
   - Example:
   ```
   mongodb+srv://salesai_user:MyPass123@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

---

## Step 6: Create .env File

1. **In your project folder**, create a new file named: `.env`

2. **Add this content** (replace with your actual connection string):

```env
# MongoDB Connection
MONGODB_URI=mongodb+srv://salesai_user:YOUR_PASSWORD_HERE@cluster0.xxxxx.mongodb.net/sales_ai?retryWrites=true&w=majority

# Django Settings
SECRET_KEY=django-insecure-change-this-in-production-12345
DEBUG=True
```

3. **IMPORTANT:** 
   - Replace `YOUR_PASSWORD_HERE` with your actual password
   - Add `/sales_ai` before the `?` to specify database name
   - Save the file

**Example .env file:**
```env
MONGODB_URI=mongodb+srv://salesai_user:SecurePass789@cluster0.abc12.mongodb.net/sales_ai?retryWrites=true&w=majority
SECRET_KEY=django-insecure-change-this-in-production-12345
DEBUG=True
```

---

## Step 7: Install Python dotenv Package

```bash
pip install python-dotenv
```

---

## Step 8: Update Django Settings

The settings are already configured to read from .env file, but let's verify:

**File: `salesAI/settings.py`**

Make sure these lines exist:
```python
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_NAME = 'sales_ai'
```

---

## Step 9: Test Connection

Run this test script:

```bash
python -c "from pymongo import MongoClient; import os; from dotenv import load_dotenv; load_dotenv(); client = MongoClient(os.getenv('MONGODB_URI')); print('✅ Connected to MongoDB!'); print('Databases:', client.list_database_names())"
```

**Expected Output:**
```
✅ Connected to MongoDB!
Databases: ['admin', 'local']
```

---

## Step 10: Set Up Demo Data

Now run the setup script:

```bash
python tmp_rovodev_quick_setup.py
```

**This will:**
- Create database: `sales_ai`
- Create collections: `agents`, `activities`, `sales`
- Insert 6 sample agents
- Generate 200+ activities
- Create 50+ sales records
- Train the AI model
- Display success message

---

## Step 11: Start Django Server

```bash
python manage.py runserver
```

---

## Step 12: View Your System!

Open your browser to:
**http://localhost:8000**

You should see:
- ✅ 6 sample agents
- ✅ Real data from MongoDB
- ✅ AI predictions
- ✅ Performance metrics
- ✅ Beautiful minimalist design!

---

## 🎉 Success Checklist

- [ ] MongoDB Atlas account created
- [ ] Free M0 cluster created
- [ ] Database user created (with password saved)
- [ ] Network access configured
- [ ] Connection string copied
- [ ] `.env` file created with connection string
- [ ] Connection tested successfully
- [ ] Demo data created
- [ ] Django server running
- [ ] Dashboard accessible at http://localhost:8000

---

## 🆘 Troubleshooting

### "ServerSelectionTimeoutError"

**Problem:** Can't connect to MongoDB

**Solutions:**
1. Check `.env` file exists in project root
2. Verify connection string has correct password
3. Make sure network access allows your IP (0.0.0.0/0)
4. Check cluster is running (not paused)

### "Authentication failed"

**Problem:** Wrong username or password

**Solutions:**
1. Double-check password in .env file
2. Verify username matches (case-sensitive)
3. Recreate database user if needed

### "Database not found"

**Problem:** Database name incorrect

**Solution:**
- Make sure connection string includes `/sales_ai` before `?`
- Example: `...mongodb.net/sales_ai?retryWrites=...`

### ".env file not found"

**Problem:** File in wrong location

**Solutions:**
1. Make sure .env is in project root (same folder as manage.py)
2. Check file name is exactly `.env` (not `env.txt` or `.env.txt`)
3. On Windows, make sure extensions are visible

---

## 📝 Quick Reference

**Your MongoDB Details:**
```
Cluster: Cluster0
Database: sales_ai
Collections: agents, activities, sales
User: salesai_user
Connection: mongodb+srv://...
```

**Your .env Location:**
```
/path/to/project/.env
```

**Test Command:**
```bash
python -c "from pymongo import MongoClient; from dotenv import load_dotenv; import os; load_dotenv(); client = MongoClient(os.getenv('MONGODB_URI')); print('✅ Connected!')"
```

---

## 🎯 Next Steps After Setup

1. **Explore the dashboard** - See all 6 agents
2. **Check AI predictions** - View HIT/MISS forecasts
3. **Train the model** - Visit /train/ to retrain
4. **Add real data** - Replace sample data with actual agents
5. **Implement hierarchy** - Add Area Managers and Division Heads

---

## 💡 Pro Tips

1. **Save your credentials** - Store username/password securely
2. **Backup .env** - But never commit it to git!
3. **Use environment variables** - For production deployments
4. **Monitor usage** - Free tier: 512MB storage, shared RAM
5. **Upgrade if needed** - Paid tiers available for larger datasets

---

**Ready? Let's set it up! Follow the steps above and let me know if you need help at any point.** 🚀
