# Fix for 502 Bad Gateway Error on Render

## Problem
Workers were timing out after 30 seconds with `WORKER TIMEOUT` and `SIGKILL` errors because:
1. MongoDB connection was being established immediately on import
2. Default gunicorn timeout (30s) was too short if MongoDB was slow to respond
3. Worker was killed before it could finish starting up

## Solution Applied

### 1. Lazy MongoDB Connection (core/database.py)
Changed from eager to lazy initialization:
- **Before**: Connection created immediately when module imported (`db = MongoDB()`)
- **After**: Connection created only when first accessed (via `_ensure_connection()`)
- **Result**: WSGI application starts in ~0.25s instead of waiting for MongoDB

Added connection timeouts to prevent indefinite hangs:
```python
MongoClient(
    settings.MONGODB_URI,
    serverSelectionTimeoutMS=5000,   # 5 second timeout
    connectTimeoutMS=10000,          # 10 second connection timeout
    socketTimeoutMS=10000,           # 10 second socket timeout
)
```

### 2. Optimized Gunicorn Configuration (Procfile)
Updated from:
```
web: gunicorn salesAI.wsgi:application --bind 0.0.0.0:$PORT
```

To:
```
web: gunicorn salesAI.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --workers 1 --threads 2 --worker-class gthread
```

**Changes explained:**
- `--timeout 120`: Increased from 30s to 120s to allow for slow MongoDB connections
- `--workers 1`: Use 1 worker (Render free tier has limited memory)
- `--threads 2`: Use 2 threads per worker for better concurrency
- `--worker-class gthread`: Use threaded worker for better performance with I/O-bound operations

## Deploy the Fix

### Step 1: Commit and Push
```bash
git add core/database.py Procfile
git commit -m "Fix worker timeout: lazy MongoDB connection + optimized gunicorn config"
git push origin main
```

### Step 2: Deploy on Render
Render will automatically detect the push and redeploy. You can also:
1. Go to https://dashboard.render.com
2. Find your `salesai-system` service
3. Click **Manual Deploy** → **Deploy latest commit**

### Step 3: Monitor Deployment
Watch the logs during deployment:
- Should see `Booting worker with pid: X` without timeout errors
- Application should start successfully
- Workers should not be killed with SIGKILL

## Expected Results

✓ Fast startup: WSGI application loads in < 1 second
✓ No timeouts: Workers stay alive and don't get killed
✓ Lazy connection: MongoDB connects only when first request hits the database
✓ Better error handling: Connection timeouts prevent indefinite hangs

## Verification

Once deployed, test:
1. Visit https://salesai-system.onrender.com/
2. Should load without 502 error
3. Check logs for successful worker boot
4. Verify no WORKER TIMEOUT or SIGKILL messages

## If Still Having Issues

### Check MongoDB Connection String
Ensure `MONGODB_URI` environment variable is set correctly in Render:
- Format: `mongodb+srv://<user>:<password>@<cluster>.mongodb.net/sales_ai?retryWrites=true&w=majority`
- Check username/password are correct
- Verify cluster URL is accessible

### Check Render Free Tier Limits
- Free tier has 512MB RAM limit
- If memory issues persist, may need to upgrade or optimize further

### Review Logs
Look for specific errors in Render logs:
- MongoDB connection errors
- Memory issues
- Import/dependency errors
