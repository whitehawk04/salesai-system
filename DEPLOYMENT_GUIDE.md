# SalesAI Deployment Guide

This guide will help you deploy the SalesAI system to a live hosting platform.

## Prerequisites

1. **GitHub Account** - To host your code repository
2. **MongoDB Atlas Account** - For cloud database (free tier available)
3. **Hosting Platform Account** - Choose one:
   - Render.com (Recommended)
   - Railway.app
   - Heroku
   - PythonAnywhere

---

## Step 1: Set Up MongoDB Atlas (Free Cloud Database)

### 1.1 Create MongoDB Atlas Account
1. Go to [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Click "Try Free" and sign up
3. Choose the **FREE tier** (M0 Sandbox - 512MB)

### 1.2 Create Database Cluster
1. Select **AWS** as cloud provider
2. Choose a region close to Philippines (e.g., Singapore)
3. Cluster Name: `salesai-cluster`
4. Click "Create Cluster" (takes 3-5 minutes)

### 1.3 Set Up Database Access
1. Go to **Database Access** in left menu
2. Click "Add New Database User"
3. Choose **Password** authentication
4. Username: `salesai_user`
5. Password: Generate a strong password (save it!)
6. User Privileges: **Read and write to any database**
7. Click "Add User"

### 1.4 Set Up Network Access
1. Go to **Network Access** in left menu
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (0.0.0.0/0)
4. Click "Confirm"

### 1.5 Get Connection String
1. Go to **Database** → Click "Connect"
2. Choose "Connect your application"
3. Copy the connection string, it looks like:
   ```
   mongodb+srv://salesai_user:<password>@salesai-cluster.xxxxx.mongodb.net/
   ```
4. Replace `<password>` with your actual password
5. Add database name at the end: `/sales_ai`
6. Final format:
   ```
   mongodb+srv://salesai_user:YOUR_PASSWORD@salesai-cluster.xxxxx.mongodb.net/sales_ai
   ```

---

## Step 2: Push Code to GitHub

### 2.1 Create GitHub Repository
1. Go to [https://github.com/new](https://github.com/new)
2. Repository name: `salesai-system`
3. Make it **Public** (or Private if you have paid plan)
4. Don't initialize with README (we already have files)
5. Click "Create repository"

### 2.2 Push Your Code
```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - SalesAI system ready for deployment"

# Add GitHub remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/salesai-system.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Step 3: Deploy to Render.com (Recommended)

### 3.1 Create Render Account
1. Go to [https://render.com](https://render.com)
2. Sign up with GitHub (easier integration)

### 3.2 Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `salesai-system`
3. Grant Render access to the repository

### 3.3 Configure Web Service
Fill in the following:

**Basic Settings:**
- **Name**: `salesai-system`
- **Region**: Singapore (closest to Philippines)
- **Branch**: `main`
- **Root Directory**: Leave blank
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: 
  ```
  pip install -r requirements.txt && python manage.py collectstatic --noinput
  ```
- **Start Command**: 
  ```
  gunicorn salesAI.wsgi:application
  ```

### 3.4 Set Environment Variables
Click "Environment" tab and add these variables:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Generate at https://djecrety.ir/ |
| `DEBUG` | `False` |
| `MONGODB_URI` | Your MongoDB Atlas connection string from Step 1.5 |
| `PYTHON_VERSION` | `3.11.0` |

### 3.5 Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for deployment
3. Your app will be live at: `https://salesai-system.onrender.com`

### 3.6 Initialize Sample Data
Once deployed, you need to populate the database:

**Option A: Via Render Shell**
1. Go to your Render service dashboard
2. Click "Shell" tab
3. Run these commands:
   ```bash
   python manage.py shell
   ```
   Then in Python shell:
   ```python
   import os
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salesAI.settings')
   import django
   django.setup()
   
   from core.utils.sample_data import create_sample_data
   from core.utils.banking_products_data import create_banking_products, create_sample_leads_and_sales
   
   create_sample_data()
   create_banking_products()
   create_sample_leads_and_sales()
   
   from core.ai.trainer import AITrainer
   model, accuracy = AITrainer.train_model()
   print(f"Done! Model accuracy: {accuracy*100:.2f}%")
   ```

**Option B: Create a setup endpoint (Recommended)**
We can add an admin endpoint to initialize data via web browser.

---

## Step 4: Alternative Platforms

### Railway.app
1. Go to [https://railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `salesai-system`
5. Add environment variables (same as Render)
6. Deploy automatically starts

### Heroku
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create salesai-system`
4. Add buildpack: `heroku buildpacks:set heroku/python`
5. Set env vars: `heroku config:set SECRET_KEY=xxx MONGODB_URI=xxx`
6. Deploy: `git push heroku main`

### PythonAnywhere
1. Sign up at [https://www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload code via Git or Files tab
3. Create new web app with manual configuration
4. Set up WSGI file pointing to `salesAI.wsgi`
5. Install requirements via Bash console
6. Set environment variables in WSGI file

---

## Step 5: Post-Deployment Setup

### 5.1 Test Your Deployment
1. Visit your live URL
2. You should see empty dashboard (no data yet)
3. Initialize sample data (see Step 3.6)

### 5.2 Access Your Live System
- **Main Dashboard**: `https://your-app.onrender.com/`
- **Area Managers**: `https://your-app.onrender.com/area-managers/`
- **Division Heads**: `https://your-app.onrender.com/division-heads/`
- **Agent Details**: `https://your-app.onrender.com/agent/A101/`
- **Train AI Model**: `https://your-app.onrender.com/train/`

### 5.3 Configure Custom Domain (Optional)
1. Purchase domain from Namecheap, GoDaddy, etc.
2. In Render dashboard, go to Settings → Custom Domain
3. Add your domain
4. Update DNS records with provided CNAME

---

## Troubleshooting

### Issue: Static files not loading
**Solution**: Run `python manage.py collectstatic` in deployment

### Issue: MongoDB connection fails
**Solution**: 
- Check MongoDB Atlas IP whitelist (should allow 0.0.0.0/0)
- Verify connection string format
- Ensure password has no special characters or is URL-encoded

### Issue: 500 Internal Server Error
**Solution**:
- Check Render logs (Logs tab in dashboard)
- Verify all environment variables are set
- Check SECRET_KEY is set and not default value

### Issue: Application takes long to load
**Solution**: Free tier on Render sleeps after inactivity. First request takes 30-60 seconds.

---

## Maintenance

### Update Your Deployment
```bash
# Make changes to code
git add .
git commit -m "Your update message"
git push origin main
```
Render automatically redeploys on git push!

### Monitor Your App
- **Render Dashboard**: View logs, metrics, and deployment status
- **MongoDB Atlas**: Monitor database usage and performance

### Backup Data
Export from MongoDB Atlas:
1. Go to Clusters → Collections
2. Use mongodump or export to JSON

---

## Cost Breakdown

### Free Forever
- **Render Free Tier**: 750 hours/month (enough for 1 app 24/7)
- **MongoDB Atlas**: 512MB storage (good for 1000s of records)
- **Total**: ₱0/month

### Upgrade Options (if needed)
- **Render Starter**: $7/month (better performance, no sleep)
- **MongoDB Atlas M10**: $0.08/hour (~$57/month for production)

---

## Security Checklist

- ✅ SECRET_KEY is unique and not in code
- ✅ DEBUG=False in production
- ✅ MongoDB password is strong
- ✅ HTTPS is enabled (automatic on Render)
- ✅ ALLOWED_HOSTS is configured
- ✅ Environment variables are set properly

---

## Support

Need help? Check:
- Render Documentation: https://render.com/docs
- MongoDB Atlas Docs: https://docs.atlas.mongodb.com/
- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/

---

## Quick Reference

### Important URLs
- **Render Dashboard**: https://dashboard.render.com
- **MongoDB Atlas**: https://cloud.mongodb.com
- **GitHub Repo**: https://github.com/YOUR_USERNAME/salesai-system

### Environment Variables Needed
```
SECRET_KEY=your-secret-key
DEBUG=False
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/sales_ai
PYTHON_VERSION=3.11.0
```

---

🎉 **Congratulations!** Your SalesAI system is now live and accessible worldwide!
