# SalesAI Deployment Checklist

Use this checklist to ensure your deployment goes smoothly.

## Pre-Deployment Checklist

### Code Preparation
- ✅ `requirements.txt` includes all dependencies (gunicorn, whitenoise, python-dotenv)
- ✅ `Procfile` created for Heroku/Railway
- ✅ `render.yaml` created for Render.com
- ✅ `runtime.txt` specifies Python version
- ✅ `.env.example` provided as template
- ✅ `.gitignore` excludes sensitive files (.env, *.pyc, __pycache__)

### Django Settings
- ✅ `SECRET_KEY` uses environment variable
- ✅ `DEBUG` uses environment variable (default False)
- ✅ `ALLOWED_HOSTS` configured
- ✅ WhiteNoise middleware added for static files
- ✅ `STATIC_ROOT` configured
- ✅ Security settings enabled when DEBUG=False
- ✅ MongoDB URI uses environment variable

### Database Setup
- ⬜ MongoDB Atlas account created
- ⬜ Free tier cluster created
- ⬜ Database user created with password
- ⬜ Network access allows 0.0.0.0/0
- ⬜ Connection string obtained and tested

### Version Control
- ⬜ Git repository initialized
- ⬜ All files committed
- ⬜ GitHub repository created
- ⬜ Code pushed to GitHub

---

## Deployment Steps (Render.com)

### Account Setup
- ⬜ Render.com account created
- ⬜ GitHub connected to Render

### Service Configuration
- ⬜ New Web Service created from GitHub repo
- ⬜ Build command set: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- ⬜ Start command set: `gunicorn salesAI.wsgi:application`
- ⬜ Python version set to 3.11.0

### Environment Variables Set
- ⬜ `SECRET_KEY` (generate at https://djecrety.ir/)
- ⬜ `DEBUG=False`
- ⬜ `MONGODB_URI` (from MongoDB Atlas)
- ⬜ `PYTHON_VERSION=3.11.0`

### Deployment
- ⬜ Service deployed successfully
- ⬜ Build logs checked (no errors)
- ⬜ Live URL accessible

---

## Post-Deployment Tasks

### Data Initialization
- ⬜ Sample data created via Render shell
- ⬜ Banking products added
- ⬜ Leads and sales generated
- ⬜ AI model trained

### Testing
- ⬜ Main dashboard loads: `/`
- ⬜ Area managers page works: `/area-managers/`
- ⬜ Division heads page works: `/division-heads/`
- ⬜ Agent detail page works: `/agent/A101/`
- ⬜ AI chat widget functional
- ⬜ Sales funnel displays correctly
- ⬜ All 6 agents visible

### Verification
- ⬜ Static files load correctly (CSS/styling works)
- ⬜ No 404 errors in browser console
- ⬜ Philippine Peso (₱) symbol displays correctly
- ⬜ AI predictions show data
- ⬜ Interactive features work (chat, quick questions)

---

## Optional Enhancements

### Custom Domain
- ⬜ Domain purchased
- ⬜ DNS configured with CNAME
- ⬜ Custom domain added in Render
- ⬜ SSL certificate active

### Monitoring
- ⬜ Error tracking set up
- ⬜ Uptime monitoring configured
- ⬜ MongoDB Atlas alerts enabled

### Performance
- ⬜ Static files compression verified
- ⬜ Database indexes added if needed
- ⬜ Response times acceptable

---

## Final Checks

### Security
- ⬜ DEBUG is False in production
- ⬜ SECRET_KEY is unique and secure
- ⬜ HTTPS enabled (automatic on Render)
- ⬜ No sensitive data in GitHub
- ⬜ MongoDB password is strong

### Functionality
- ⬜ All dashboards accessible
- ⬜ Data displays correctly
- ⬜ AI features working
- ⬜ Philippine banking products visible
- ⬜ Navigation links work

### Documentation
- ⬜ README.md updated with live URL
- ⬜ Deployment notes documented
- ⬜ Environment variables documented

---

## Common Issues & Solutions

### Build Fails
- Check requirements.txt for correct package versions
- Verify Python version compatibility
- Check build logs for specific errors

### App Crashes on Start
- Verify environment variables are set
- Check MongoDB connection string
- Review startup logs in Render dashboard

### Static Files Not Loading
- Run collectstatic command
- Verify STATIC_ROOT setting
- Check WhiteNoise configuration

### MongoDB Connection Error
- Verify connection string format
- Check MongoDB Atlas IP whitelist
- Ensure database user has correct permissions

---

## Deployment Complete! 🎉

### Your Live URLs
- **Production App**: `https://your-app-name.onrender.com`
- **GitHub Repo**: `https://github.com/your-username/salesai-system`
- **MongoDB Atlas**: `https://cloud.mongodb.com`

### Next Steps
1. Share the URL with your team
2. Monitor the app for any issues
3. Set up regular backups
4. Consider upgrading to paid tier for better performance

---

## Quick Commands

### Update Deployment
```bash
git add .
git commit -m "Update message"
git push origin main
```

### View Logs (Render Shell)
```bash
# In Render dashboard → Shell tab
tail -f /var/log/render.log
```

### Initialize Data (Render Shell)
```python
python manage.py shell
exec(open('setup_data.py').read())
```

---

**Status**: Ready for deployment! ✅
