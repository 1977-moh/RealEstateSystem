from pathlib import Path
import os
from decouple import config


# === المسار الأساسي للمشروع ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === المفتاح السري (احتفظ به سريًا في الإنتاج) ===
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-secret-key')

# === وضع التصحيح (Debug) ===
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# === السماح بالمضيفات (Allowed Hosts) ===

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# === التطبيقات المثبتة (Installed Apps) ===
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # تطبيقات الطرف الثالث
    'rest_framework',

    # التطبيقات الخاصة بالمشروع
    'clients',
    'properties',
    'employees',
    'campaigns',
    'leads',
    'payments',
    'home',
]

# === الميدلوير (Middleware) ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# === روابط المسارات (URL Configuration) ===
ROOT_URLCONF = 'real_estate_system.urls'

# === إعدادات القوالب (Templates) ===
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # تخصيص مسار للقوالب
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

# === إعداد التطبيق WSGI ===
WSGI_APPLICATION = 'real_estate_system.wsgi.application'

# === إعدادات قاعدة البيانات ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'real_estate_management'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'your_password'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

# === التحقق من كلمات المرور ===
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === إعدادات اللغة والمنطقة الزمنية ===
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# === إعدادات الملفات الثابتة (Static Files) ===
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# === إعداد ملفات الوسائط (Media Files) ===
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# === النوع الافتراضي للحقل الأساسي ===
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === إعدادات إضافية لتطبيق الحملات ===
CAMPAIGN_DATA_DIR = BASE_DIR / 'campaign_data'
CAMPAIGN_PLATFORMS = ["Facebook", "Google", "TikTok", "Instagram", "LinkedIn"]

# === إعدادات الأمان في الإنتاج ===
if not DEBUG:
    SECURE_HSTS_SECONDS = 3600
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
SECURE_HSTS_SECONDS = 3600
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
