# Fix MongoDB SSL Warning

## The Warning
```
UserWarning: Unknown option ssl_cert_reqs
```

This is just a warning - your connection is working! But we can fix it.

## Problem
The MongoDB connection string uses an outdated SSL parameter format:
```
mongodb+srv://user:pass@cluster.mongodb.net/db?ssl=true&ssl_cert_reqs=CERT_NONE
```

## Solution
Update your `MONGODB_URI` in Render to use the modern format:

### Go to Render Dashboard
1. Visit: https://dashboard.render.com
2. Click on `salesai-system` service
3. Go to **Environment** tab
4. Find `MONGODB_URI`
5. Click **Edit**

### Update to Modern Format

**Change from:**
```
mongodb+srv://username:password@ac-swnbz3j.lfm9kj8.mongodb.net/sales_ai?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE
```

**Change to:** (remove the SSL parameters entirely)
```
mongodb+srv://username:password@ac-swnbz3j.lfm9kj8.mongodb.net/sales_ai?retryWrites=true&w=majority
```

### Why This Works
- `mongodb+srv://` (SRV connection string) **automatically uses SSL/TLS**
- No need to specify `ssl=true` or `ssl_cert_reqs`
- The Python driver handles SSL automatically
- Modern and recommended by MongoDB

### Save and Redeploy
1. Click **Save**
2. Render will automatically redeploy
3. Warning will disappear

---

## Important: Your Site is Working!

The warning doesn't prevent functionality. Your dashboard is loading (HTTP 200 response).

You can:
1. **Ignore the warning** - it's cosmetic
2. **Fix it later** when convenient
3. **Fix it now** using steps above

---

## Verify After Fix

After updating and redeploying, check logs. You should see:
```
✓ MongoDB connection successful
✓ No warnings
```

Instead of:
```
⚠ UserWarning: Unknown option ssl_cert_reqs
```
