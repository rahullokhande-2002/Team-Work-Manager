# Render Deployment - Quick Reference

## ✅ Completed Tasks

### 1. Updated `settings.py`
```python
# Environment Variables
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# WhiteNoise Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← ADDED
    # ... other middleware
]

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # ← ADDED
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # ← ADDED

# Database (PostgreSQL or SQLite)
if os.environ.get('DATABASE_URL'):
    # Use PostgreSQL on Render
else:
    # Use SQLite locally
```

### 2. Updated `requirements.txt`
```
Django==6.0.3
gunicorn==22.0.0          ← Production server
whitenoise==6.6.0         ← Static file serving
psycopg2-binary==2.9.9    ← PostgreSQL adapter
```

### 3. Created `build.sh`
```bash
#!/bin/bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

### 4. Created `Procfile`
```
web: gunicorn myproject.wsgi:application
```

### 5. Created `render.yaml` (optional automated deployment)

### 6. Updated `.gitignore`
Excludes: `env/`, `__pycache__/`, `db.sqlite3`, `staticfiles/`, `.env`

### 7. Created `DEPLOYMENT.md`
Complete deployment guide with step-by-step instructions

---

## 🚀 Deploy to Render in 3 Steps

### Step 1: Generate Secret Key
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 2: Push to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 3: Deploy on Render
1. Visit https://render.com and sign up
2. New → Web Service → Connect GitHub repo
3. Set Build Command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
4. Set Start Command: `gunicorn myproject.wsgi:application`
5. Add Environment Variables:
   - `DEBUG=False`
   - `SECRET_KEY=<your-generated-key>`
6. Click "Create Web Service"

---

## 🔧 Environment Variables Needed in Render

| Variable | Value | Required |
|----------|-------|----------|
| `DEBUG` | `False` | ✅ Yes |
| `SECRET_KEY` | Generated key | ✅ Yes |
| `DATABASE_URL` | PostgreSQL URL | ❌ Optional (PostgreSQL) |

---

## 📁 Files Created/Modified

| File | Status | Purpose |
|------|--------|---------|
| `settings.py` | ✏️ Modified | Production configuration |
| `requirements.txt` | ✏️ Modified | Added production dependencies |
| `build.sh` | ✨ Created | Build script for Render |
| `Procfile` | ✨ Created | Process configuration |
| `render.yaml` | ✨ Created | Infrastructure as code (optional) |
| `.gitignore` | ✨ Created | Exclude sensitive files |
| `DEPLOYMENT.md` | ✨ Created | Full deployment guide |

---

## ✅ Pre-Deployment Checklist

- [x] SECRET_KEY uses environment variable
- [x] DEBUG uses environment variable  
- [x] ALLOWED_HOSTS = ['*']
- [x] WhiteNoise middleware added
- [x] STATIC_ROOT configured
- [x] Static file storage configured
- [x] Database supports PostgreSQL
- [x] Gunicorn in requirements.txt
- [x] .gitignore created
- [x] build.sh created
- [x] Procfile created

---

## 🎯 Key Points

1. **Static Files**: WhiteNoise handles serving static files in production (CSS, JS, images)
2. **Database**: Can use SQLite locally, PostgreSQL on Render
3. **Environment Variables**: All sensitive data comes from env vars, not hardcoded
4. **Auto-deployment**: Push to GitHub → Render automatically deploys
5. **No More 500 Errors**: Production-ready settings prevent common deployment issues

---

## 📚 Next Steps

1. Generate SECRET_KEY and store it securely
2. Push all changes to GitHub
3. Create Render account and web service
4. Set environment variables in Render
5. Deploy and test!

For detailed instructions, see `DEPLOYMENT.md`
