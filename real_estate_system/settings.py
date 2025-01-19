from pathlib import Path
from decouple import config

# === المسار الأساسي للمشروع ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === المفتاح السري (احتفظ به سريًا في الإنتاج) ===
SECRET_KEY = config('DJANGO_SECRET_KEY', default='your-secret-key')

# === وضع التصحيح (Debug) ===
DEBUG = config('DJANGO_DEBUG', default=True, cast=bool)

# === السماح بالمضيفات (Allowed Hosts) ===
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

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
    'brokers',  # تطبيق الوساطة العقارية
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
        'NAME': config('POSTGRES_DB', default='real_estate_management'),
        'USER': config('POSTGRES_USER', default='postgres'),
        'PASSWORD': config('POSTGRES_PASSWORD', default='your_password'),
        'HOST': config('POSTGRES_HOST', default='localhost'),
        'PORT': config('POSTGRES_PORT', default='5432'),
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

# === إعدادات التخزين المؤقت (Cache) ===
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# === إعدادات تسجيل الأخطاء (Logging) ===
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
            'filename': BASE_DIR / 'debug.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    },
}
