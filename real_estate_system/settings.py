import os
from pathlib import Path
from decouple import config
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# === 🏠 المسار الأساسي للمشروع ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === 🌍 إعداد العملة الافتراضية ===
CURRENCY = config("DEFAULT_CURRENCY", default="EGP")

# === 📁 إعداد مجلد السجلات (Logs) ===
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

# === 🔒 المفتاح السري ===
SECRET_KEY = config('DJANGO_SECRET_KEY', default='your-secret-key')

# === 🛠️ وضع التصحيح (Debug Mode) ===
DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)

# === 🌐 السماح بالمضيفات ===
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# === 🏗️ التطبيقات المثبتة ===
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',

    # ✅ تطبيقات الطرف الثالث
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'django_celery_beat',  # ✅ لإدارة الجدولة
    'django_celery_results',  # ✅ لحفظ نتائج المهام

    # ✅ التطبيقات الخاصة بالمشروع
    'employees',
    'brokers',
    'clients',
    'campaigns',
    'properties',
    'dashboard',
    'crm.crm',  # ✅ إضافة CRM
    'leads',
    'payments',
    'offer',
    'accounting',
    'home',
]

# === ⚡ إعداد الميدلوير (Middleware) ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

# === 🌍 إعدادات CORS ===
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default="http://localhost:3000,http://127.0.0.1:8000").split(',')
CORS_ALLOW_CREDENTIALS = True
if not DEBUG:
    CORS_ALLOW_ALL_ORIGINS = False

# === 🔄 روابط المسارات ===
ROOT_URLCONF = 'real_estate_system.urls'

# === 🎨 إعدادات القوالب ===
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'home' / 'templates' / 'home',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# === 🔥 إعداد التطبيق WSGI ===
WSGI_APPLICATION = 'real_estate_system.wsgi.application'

# === 🗄️ إعدادات قاعدة البيانات ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql' if config('USE_POSTGRES', default=False, cast=bool) else 'django.db.backends.sqlite3',
        'NAME': config('POSTGRES_DB') if config('USE_POSTGRES', default=False, cast=bool) else BASE_DIR / "db.sqlite3",
        'USER': config('POSTGRES_USER', default='postgres'),
        'PASSWORD': config('POSTGRES_PASSWORD', default='your_password'),
        'HOST': config('POSTGRES_HOST', default='localhost'),
        'PORT': config('POSTGRES_PORT', default='5432'),
        'CONN_MAX_AGE': 600,
        'ATOMIC_REQUESTS': True,
    }
}

# === ⏳ إعداد Celery للمهام الخلفية ===
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = "UTC"

# === 🔐 إعدادات الأمان ===
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    X_FRAME_OPTIONS = 'DENY'

# === ⚡ إعداد التخزين المؤقت ===
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'TIMEOUT': 300,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# === 📊 تسجيل الأخطاء مع Sentry ===
sentry_sdk.init(
    dsn=config('SENTRY_DSN', default=''),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
    ignore_errors=[
        'django.http.Http404',
        'django.db.utils.OperationalError'
    ],
)

# === 📝 تسجيل السجلات (Logging) ===
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR / 'debug.log',
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR / 'errors.log',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'root': {
        'handlers': ['file', 'error_file', 'mail_admins'],
        'level': 'DEBUG' if DEBUG else 'ERROR',
    },
}
