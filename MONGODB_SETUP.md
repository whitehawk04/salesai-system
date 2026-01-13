# 🔌 MongoDB Setup Guide

## Current Issue
The system tried to connect to MongoDB on localhost:27017, but MongoDB isn't running.

## ✅ Two Solutions

### Option 1: Use MongoDB Atlas (Recommended - Free & Easy)

**Why:** Cloud-based, free tier available, no local installation needed

**Steps:**

1. **Create Free Account**
   - Go to: https://www.mongodb.com/cloud/atlas/register
   - Sign up (it's free)

2. **Create Free Cluster**
   - Click "Build a Database"
   - Choose "Free" (M0 tier)
   - Select your region
   - Click "Create"

3. **Set Up Security**
   - Username: Choose a username (e.g., "admin")
   - Password: Create a strong password (save it!)
   - IP Whitelist: Click "Add My Current IP Address" 
   - Or add "0.0.0.0/0" for access from anywhere (less secure but easier for testing)

4. **Get Connection String**
   - Click "Connect"
   - Choose "Connect your application"
   - Copy the connection string (looks like):
   ```
   mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

5. **Create .env File**
   - In your project folder, create a file named `.env`
   - Add this line (replace with your connection string):
   ```
   MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/sales_ai?retryWrites=true&w=majority
   ```
   - Make sure to replace `username` and `password` with your credentials
   - Add `/sales_ai` after `.mongodb.net` to specify the database name

6. **Run Setup Again**
   ```bash
   python tmp_rovodev_quick_setup.py
   ```

**Total Time: 5-10 minutes**

---

### Option 2: Install MongoDB Locally

**Why:** Run everything on your computer, no internet needed after setup

**Steps:**

1. **Download MongoDB Community**
   - Go to: https://www.mongodb.com/try/download/community
   - Choose your OS (Windows)
   - Download and install

2. **Install MongoDB**
   - Run the installer
   - Choose "Complete" installation
   - Install "MongoDB as a Service" (check the box)
   - Keep default settings

3. **Verify Installation**
   ```bash
   mongo --version
   ```
   or
   ```bash
   mongod --version
   ```

4. **Start MongoDB Service** (if not started)
   ```bash
   # Windows:
   net start MongoDB
   
   # Or from Services app:
   # Press Win+R, type "services.msc", find MongoDB, and Start it
   ```

5. **Run Setup**
   ```bash
   python tmp_rovodev_quick_setup.py
   ```

**Total Time: 10-15 minutes**

---

## 🚀 Quick Start (Recommended: MongoDB Atlas)

I recommend **Option 1 (MongoDB Atlas)** because:
- ✅ Free forever (M0 tier)
- ✅ No local installation needed
- ✅ Works from anywhere
- ✅ Automatic backups
- ✅ Easy to scale
- ✅ 5 minutes to set up

---

## 📝 After MongoDB is Set Up

Once MongoDB is configured, run:

```bash
# Setup demo data and train AI
python tmp_rovodev_quick_setup.py

# Start the server
python manage.py runserver

# Open browser
http://localhost:8000
```

You'll see:
- 📊 6 sample agents
- 🤖 AI predictions
- 📈 Performance metrics
- 🎯 Risk assessments

---

## 🆘 Troubleshooting

### "ServerSelectionTimeoutError"
→ MongoDB isn't running or .env file is incorrect

**Fix:**
- For Atlas: Check .env file has correct connection string
- For Local: Start MongoDB service

### "Authentication failed"
→ Username/password in .env is wrong

**Fix:**
- Double-check credentials in MongoDB Atlas
- Update .env file with correct values

### "Database not found"
→ No problem! MongoDB creates it automatically

**Fix:**
- Just run the setup script, it will create the database

---

## 💡 Pro Tip

For this demo/development, **use MongoDB Atlas**. It's:
- Faster to set up (5 min vs 15 min)
- No local resources used
- Accessible from anywhere
- Free forever for small projects

For production later, you can:
- Keep using Atlas (they have paid tiers for scaling)
- Or migrate to self-hosted MongoDB

---

## ✅ What Happens After Setup

Once MongoDB is connected and setup runs:

1. **Creates Database:** `sales_ai`
2. **Creates Collections:** `agents`, `activities`, `sales`
3. **Inserts Sample Data:**
   - 6 agents with realistic profiles
   - 200+ activities (calls, meetings, leads, deals)
   - 50+ sales transactions
4. **Trains AI Model:**
   - Uses RandomForest classifier
   - Learns from synthetic data
   - Saves model to disk
5. **Ready to Use:**
   - Dashboard shows all agents
   - AI predictions are live
   - System fully operational

---

## 📞 Need Help?

**Quick links:**
- MongoDB Atlas: https://www.mongodb.com/cloud/atlas
- MongoDB Docs: https://docs.mongodb.com/
- Connection String Help: https://docs.mongodb.com/manual/reference/connection-string/

**Common questions:**
- "Which option?" → Use Atlas (Option 1)
- "Is Atlas really free?" → Yes, M0 tier is free forever
- "Can I change later?" → Yes, easily migrate between options

---

**Let's get MongoDB set up so you can see your AI sales system in action! 🚀**
