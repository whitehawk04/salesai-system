# 🚀 Deployment Guide

## Production Deployment Checklist

### 1. Security Settings

**Update `salesAI/settings.py`:**

```python
# Generate a strong secret key
SECRET_KEY = os.getenv('SECRET_KEY')  # NEVER commit this!

# Disable debug mode
DEBUG = False

# Set allowed hosts
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# HTTPS settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### 2. Environment Variables

Create a `.env` file (never commit this):

```bash
# Django
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# MongoDB Atlas
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/sales_ai?retryWrites=true&w=majority

# Email (optional, for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 3. MongoDB Atlas Setup

1. **Create Production Cluster**
   - Go to https://cloud.mongodb.com
   - Create a new cluster (M0 free tier or paid)
   - Create database: `sales_ai`

2. **Security**
   - Enable IP whitelist (add your server's IP)
   - Create database user with strong password
   - Enable connection string encryption

3. **Collections**
   - The app will auto-create: `agents`, `activities`, `sales`

### 4. Static Files

```bash
# Collect static files
python manage.py collectstatic
```

Update `settings.py`:
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
```

### 5. Deployment Options

#### Option A: Heroku

```bash
# Install Heroku CLI
heroku login
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set MONGODB_URI=your-mongodb-uri
heroku config:set DEBUG=False

# Deploy
git push heroku main
```

**Procfile:**
```
web: gunicorn salesAI.wsgi --log-file -
```

**runtime.txt:**
```
python-3.11.0
```

Add to requirements.txt:
```
gunicorn==21.2.0
```

#### Option B: AWS EC2

1. **Launch EC2 Instance**
   - Amazon Linux 2 or Ubuntu
   - t2.micro (free tier eligible)

2. **Install Dependencies**
```bash
sudo yum update -y
sudo yum install python3 python3-pip git -y
```

3. **Clone and Setup**
```bash
git clone your-repo-url
cd salesAI
pip3 install -r requirements.txt
```

4. **Configure Nginx**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/salesAI/staticfiles/;
    }
}
```

5. **Run with Gunicorn**
```bash
gunicorn salesAI.wsgi:application --bind 0.0.0.0:8000
```

6. **Create Systemd Service**
```ini
[Unit]
Description=Sales AI Django App
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/salesAI
ExecStart=/usr/local/bin/gunicorn salesAI.wsgi:application --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Option C: DigitalOcean App Platform

1. Connect your GitHub repository
2. Set environment variables in dashboard
3. Deploy automatically on push

#### Option D: Docker

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "salesAI.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - MONGODB_URI=${MONGODB_URI}
      - DEBUG=False
    restart: always
```

Build and run:
```bash
docker-compose up -d
```

### 6. Model Training Schedule

For production, set up periodic model retraining:

**Using Cron (Linux):**
```bash
# Run every week
0 0 * * 0 cd /path/to/salesAI && python manage.py shell -c "from core.ai.trainer import AITrainer; AITrainer.train_model()"
```

**Using Celery (Advanced):**
```python
# tasks.py
from celery import shared_task
from core.ai.trainer import AITrainer

@shared_task
def retrain_model():
    AITrainer.train_model()
```

### 7. Monitoring

**Add logging:**
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'salesai.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### 8. Backup Strategy

**MongoDB Atlas Backups:**
- Enable automatic backups in Atlas dashboard
- Set retention period (7-365 days)

**Manual Backup:**
```bash
# Export data
mongoexport --uri="mongodb+srv://..." --collection=agents --out=agents.json
mongoexport --uri="mongodb+srv://..." --collection=activities --out=activities.json
mongoexport --uri="mongodb+srv://..." --collection=sales --out=sales.json
```

### 9. Performance Optimization

1. **Enable caching:**
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

2. **Database indexing:**
```python
# In MongoDB
db.activities.createIndex({"agent_id": 1, "date": -1})
db.sales.createIndex({"agent_id": 1, "date": -1})
```

3. **Compress static files**

### 10. Health Checks

Add a health check endpoint:

```python
# core/views.py
def health_check(request):
    return JsonResponse({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# core/urls.py
path('health/', views.health_check, name='health_check'),
```

### 11. SSL Certificate

**Using Let's Encrypt (Free):**
```bash
sudo certbot --nginx -d yourdomain.com
```

### 12. Post-Deployment

1. Test all endpoints
2. Verify MongoDB connection
3. Train initial model with production data
4. Set up monitoring/alerting
5. Configure backups
6. Document admin procedures

---

## Production URLs

- Dashboard: https://yourdomain.com/
- Admin: https://yourdomain.com/admin/
- API: https://yourdomain.com/api/agents/
- Health: https://yourdomain.com/health/

---

**Security Note:** Never commit `.env` files or expose secret keys!
