# MongoDB SSL Connection Fix for Render

## The Problem
Getting SSL/TLS handshake errors on Render with MongoDB Atlas:
```
[SSL: TLSV1_ALERT_INTERNAL_ERROR] tlsv1 alert internal error
```

## Root Cause
The MongoDB connection string in Render's environment variables is missing SSL parameters.

## Solution: Update MONGODB_URI in Render

### Current Format (Incorrect)
```
mongodb+srv://<username>:<password>@<cluster>.mongodb.net/sales_ai?retryWrites=true&w=majority
```

### Required Format (Correct)
```
mongodb+srv://<username>:<password>@<cluster>.mongodb.net/sales_ai?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE
```

**OR** (Recommended - more secure)
```
mongodb+srv://<username>:<password>@<cluster>.mongodb.net/sales_ai?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=false
```

## How to Fix in Render

### Step 1: Get Your MongoDB Connection String
1. Go to MongoDB Atlas: https://cloud.mongodb.com/
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string

### Step 2: Update in Render
1. Go to Render Dashboard: https://dashboard.render.com
2. Find your `salesai-system` service
3. Click **Environment** tab
4. Find `MONGODB_URI` variable
5. Update the value to include SSL parameters

### Recommended Connection String
Replace with your actual credentials:
```
mongodb+srv://<username>:<password>@ac-swnbz3j.lfm9kj8.mongodb.net/sales_ai?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE
```

**Important Notes:**
- Replace `<username>` with your MongoDB username
- Replace `<password>` with your MongoDB password (URL-encoded if it contains special characters)
- Keep `ac-swnbz3j.lfm9kj8.mongodb.net` (your cluster URL)
- Keep `sales_ai` as the database name
- Add `&ssl=true&ssl_cert_reqs=CERT_NONE` at the end

### Step 3: Redeploy
After updating the environment variable:
1. Click **Manual Deploy** → **Deploy latest commit**
2. Wait for deployment to complete
3. Check logs for successful connection

## Alternative: Use MongoDB Atlas Network Access

If SSL issues persist, ensure Render can access MongoDB:

1. **In MongoDB Atlas:**
   - Go to "Network Access" (Security menu)
   - Click "Add IP Address"
   - Choose **"Allow access from anywhere"** (0.0.0.0/0)
   - This allows Render's dynamic IPs to connect

2. **Security Note:**
   - This is safe because you still have username/password authentication
   - MongoDB Atlas enforces authentication regardless of IP whitelist

## Testing Locally

Your local connection works because your environment likely has better SSL/TLS support. To test the fix:

```bash
# Test with the updated connection string
python test_mongodb_connection.py
```

## What Changed in the Code

1. **Python version**: Updated from 3.11.0 → 3.11.9 (better SSL support)
2. **Simplified SSL config**: Let pymongo handle SSL automatically via connection string
3. **Increased timeouts**: 10-20 seconds to handle slow connections

## Verification

Once deployed, you should see in logs:
```
✓ Starting application...
✓ MongoDB connection successful
✓ Worker started successfully
```

Instead of:
```
✗ SSL handshake failed
✗ WORKER TIMEOUT
```
