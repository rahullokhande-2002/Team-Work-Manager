# Django Render Deployment Guide

## Project Structure
```
Team-Work-Manager/
├── myproject/
│   ├── manage.py
│   ├── db.sqlite3
│   ├── myproject/
│   │   ├── settings.py (UPDATED)
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── core/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── static/
│   │   └── templates/
├── requirements.txt (UPDATED)
├── build.sh (NEW)
├── Procfile (NEW)
├── render.yaml (NEW)
├── .gitignore (NEW)
└── README.md
```

## What Was Updated

### 1. **settings.py** - Production Configuration
✅ **Environment Variables:**
- `SECRET_KEY` - Read from `SECRET_KEY` env variable (with fallback)
- `DEBUG` - Read from `DEBUG` env variable (defaults to False)

✅ **WhiteNoise Middleware:**
- Added `whitenoise.middleware.WhiteNoiseMiddleware` for static file serving
- Configured `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'`

✅ **Static Files:**
- `STATIC_ROOT = BASE_DIR / 'staticfiles'` - Where collected static files go
- `STATIC_URL = '/static/'` - URL prefix for static files
- `STATICFILES_DIRS` - Points to app static directories

✅ **Database Configuration:**
- Checks for `DATABASE_URL` environment variable (Render's PostgreSQL)
- Falls back to SQLite in development
- Ready for production PostgreSQL migration

✅ **Security:**
- `ALLOWED_HOSTS = ['*']` - Accepts all hosts (change if needed for specific domain)

### 2. **requirements.txt** - Production Dependencies
```
asgiref==3.11.1
Django==6.0.3
sqlparse==0.5.5
tzdata==2025.3
gunicorn==22.0.0          # Application server
whitenoise==6.6.0         # Static file serving
psycopg2-binary==2.9.9    # PostgreSQL adapter
```

### 3. **build.sh** - Build Script
```bash
#!/bin/bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```
This script runs automatically on Render during deployment.

### 4. **Procfile** - Process Configuration
```
web: gunicorn myproject.wsgi:application
```
Tells Render to start your app with Gunicorn.

### 5. **render.yaml** - Infrastructure as Code (Optional)
Automated deployment configuration for Render including:
- Service definition
- Build command
- Start command
- Environment variables
- Database setup

### 6. **.gitignore** - Version Control
Excludes from Git:
- `env/`, `venv/` - Virtual environments
- `__pycache__/` - Python cache files
- `db.sqlite3` - Local database
- `staticfiles/` - Collected static files
- `.env` - Environment variables
- IDE files (`.vscode/`, `.idea/`)

---

## Deployment Steps

### Step 1: Generate a New SECRET_KEY
```bash
# Run this in your Python shell to generate a secure key:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 2: Push to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 3: Create Render Account
Visit [https://render.com](https://render.com) and sign up.

### Step 4: Create New Web Service
1. Go to Dashboard → New → Web Service
2. Connect your GitHub repository
3. Set the following:
   - **Name**: `team-work-manager` (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn myproject.wsgi:application`

### Step 5: Set Environment Variables
In Render Dashboard → Environment:
```
DEBUG=False
SECRET_KEY=<paste your generated key>
```

### Step 6: (Optional) Set Up PostgreSQL Database
1. Create a PostgreSQL instance in Render
2. Copy the database URL
3. In Web Service → Environment, add:
```
DATABASE_URL=<paste the URL from Render PostgreSQL>
```

### Step 7: Deploy
Click "Create Web Service" and Render will automatically:
1. Clone your repo
2. Install dependencies
3. Run migrations
4. Collect static files
5. Start the application

---

## Common Commands for Local Development

### Create Virtual Environment
```bash
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Development Server
```bash
cd myproject
python manage.py runserver
```

### Collect Static Files (Test Locally)
```bash
python manage.py collectstatic --noinput
```

### Run Migrations
```bash
python manage.py migrate
```

---

## Troubleshooting

### Static Files Not Loading
1. Run: `python manage.py collectstatic --noinput`
2. Check that `STATIC_ROOT` is set (should be `staticfiles/`)
3. Verify WhiteNoise middleware is in `MIDDLEWARE`

### Database Connection Failed
1. Check `DATABASE_URL` environment variable in Render
2. Ensure migrations ran: `python manage.py migrate`
3. Use PostgreSQL credentials from Render dashboard

### Secret Key Issues
1. Generate new key: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
2. Update in Render environment variables

### Application Won't Start
1. Check Render Logs: Dashboard → Web Service → Logs
2. Ensure `gunicorn` is in requirements.txt
3. Verify Procfile uses correct format: `web: gunicorn myproject.wsgi:application`

---

## Production Checklist

- [x] `DEBUG = False` in production
- [x] `SECRET_KEY` from environment variable
- [x] `ALLOWED_HOSTS` configured
- [x] WhiteNoise middleware added
- [x] Static files collection configured
- [x] Database configured for production
- [x] `.gitignore` excludes sensitive files
- [x] `requirements.txt` has all dependencies
- [x] `build.sh` and `Procfile` created
- [x] Environment variables set in Render

---

## Next Steps

1. **Add a custom domain** (Render → Web Service → Settings)
2. **Set up SSL/HTTPS** (Automatic with Render)
3. **Configure email** (Add Django email settings)
4. **Add monitoring** (Render has built-in logs)
5. **Regular backups** (If using PostgreSQL, enable automated backups)

---

## Quick Deployment Command

For future deployments, just push to GitHub:
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

Render will automatically rebuild and deploy! 🚀
