# Fix: MongoDB DNS Query Error on Render

## Error Message
```
pymongo.errors.ConfigurationError: The DNS query name does not exist: 
_mongodb._tcp.salesai-cluster.xxxxx.mongodb.net.
```

## What This Means
Your `MONGODB_URI` environment variable either:
1. Still has the placeholder value (`mongodb://localhost:27017/`)
2. Has an incorrect MongoDB Atlas connection string
3. MongoDB Atlas cluster doesn't exist yet

---

## ✅ SOLUTION: Set Up MongoDB Atlas Properly

Follow these steps in order:

### Step 1: Create MongoDB Atlas Cluster (5 minutes)

1. **Go to**: https://www.mongodb.com/cloud/atlas

2. **Sign up** (if you haven't):
   - Click "Try Free"
   - Sign up with Google (easiest)

3. **Create Cluster**:
   - Choose: **M0 Shared** (FREE forever)
   - Cloud Provider: **AWS**
   - Region: **Singapore (ap-southeast-1)** ✅
   - Cluster Name: `salesai-cluster`
   - Click **"Create"**
   - Wait 2-3 minutes for cluster to be created

---

### Step 2: Create Database User

1. Left sidebar → **"Database Access"**
2. Click **"Add New Database User"**

**Fill in:**
- Username: `salesai_admin`
- Authentication: **Password**
- Click **"Autogenerate Secure Password"**
- **⚠️ COPY THIS PASSWORD AND SAVE IT!** (you won't see it again)
- Privileges: **"Read and write to any database"**
- Click **"Add User"**

---

### Step 3: Allow Network Access

1. Left sidebar → **"Network Access"**
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (0.0.0.0/0)
4. Click **"Confirm"**

---

### Step 4: Get Connection String

1. Left sidebar → **"Database"**
2. Wait for cluster status to show **"Active"** (green dot)
3. Click **"Connect"** button on your cluster
4. Choose **"Connect your application"**
5. Driver: **Python**, Version: **3.6 or later**
6. **Copy the connection string**:
   ```
   mongodb+srv://salesai_admin:<password>@salesai-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

---

### Step 5: Format Connection String Correctly

Take the connection string and modify it:

**Original**:
```
mongodb+srv://salesai_admin:<password>@salesai-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

**Change to** (3 modifications):
1. Replace `<password>` with your ACTUAL password from Step 2
2. Add `/sales_ai` BEFORE the `?` (this is the database name)
3. Keep the rest

**Final format**:
```
mongodb+srv://salesai_admin:YOUR_ACTUAL_PASSWORD@salesai-cluster.xxxxx.mongodb.net/sales_ai?retryWrites=true&w=majority
```

**Example** (with fake password):
```
mongodb+srv://salesai_admin:MyP@ssw0rd123@salesai-cluster.abc123.mongodb.net/sales_ai?retryWrites=true&w=majority
```

⚠️ **Important**: 
- Replace `YOUR_ACTUAL_PASSWORD` with your real password
- Make sure `/sales_ai` comes BEFORE the `?`
- Don't remove `?retryWrites=true&w=majority`

---

### Step 6: Update MONGODB_URI in Render

1. Go to your **Render dashboard**
2. Click on your **salesai-system** service
3. Click **"Environment"** tab (top menu)
4. Find **`MONGODB_URI`**
5. Click **"Edit"**
6. **Delete** the old value
7. **Paste** your new MongoDB Atlas connection string from Step 5
8. Click **"Save Changes"**

**Render will automatically redeploy!**

---

### Step 7: Wait for Deployment

1. Click **"Logs"** tab
2. Watch the deployment
3. Wait for: **"Your service is live 🎉"**

✅ **Success!** Your app is now deployed with proper database!

---

## Alternative: Quick Deploy Without Persistent Database

If you just want to test deployment quickly (data won't persist):

1. In Render, go to **"Environment"** → **`MONGODB_URI`** → **"Edit"**
2. Change to: `mongodb://localhost:27017/sales_ai`
3. Save
4. App will deploy successfully
5. **BUT**: No data persistence, resets on every deploy

**Not recommended for production!**

---

## Troubleshooting

### "Cluster is still creating"
**Solution**: Wait 2-3 minutes for cluster to be "Active" before getting connection string

### "Authentication failed"
**Solution**: 
- Make sure you replaced `<password>` with actual password
- Password has no special characters that need URL encoding
- Or regenerate password in Database Access

### "Connection string format is wrong"
**Solution**: Make sure format is:
```
mongodb+srv://username:password@cluster.mongodb.net/sales_ai?retryWrites=true&w=majority
```

Key points:
- `mongodb+srv://` (not `mongodb://`)
- `/sales_ai` comes BEFORE the `?`
- Keep `?retryWrites=true&w=majority` at the end

### "Still getting DNS error"
**Solution**:
- Verify cluster name in MongoDB Atlas matches the connection string
- Check cluster is "Active" (green) in MongoDB Atlas
- Try removing and re-adding the MONGODB_URI environment variable

---

## After Successful Deployment

Your app will be live but **empty** (no data yet).

**Next Step**: Initialize sample data:
1. In Render dashboard → **"Shell"** tab
2. Run the data initialization script (I'll guide you)

---

## Quick Reference

### MongoDB Atlas URL
https://cloud.mongodb.com

### Connection String Format
```
mongodb+srv://salesai_admin:PASSWORD@salesai-cluster.XXXXX.mongodb.net/sales_ai?retryWrites=true&w=majority
```

### What to Replace
- `PASSWORD` = Your actual password from Database Access
- `XXXXX` = Your cluster ID (auto-generated)
- `/sales_ai` = Database name (must be before `?`)

---

**Start with Step 1 now!** Create your MongoDB Atlas account and cluster. It takes 5 minutes. 🚀
