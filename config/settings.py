import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

# 📍 تحديد البيئة الحالية: development أو production
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# المسار الأساسي للمشروع
BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠️ المفتاح السري
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-default-key")

# ✅ وضع DEBUG حسب البيئة
DEBUG = ENVIRONMENT == "development"

# ✅ المضيفين المسموح بهم حسب البيئة
if ENVIRONMENT == "production":
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "render.com,.onrender.com").split(",")
else:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# التطبيقات المثبتة
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # التطبيقات الخاصة بك
    'stores.apps.StoresConfig',
    'accounts',
    'orders',
    'delivery',
    'news',
    'ads',
    'core',

    # إضافات
    'widget_tweaks',
    'cloudinary_storage',
    'cloudinary',
]

# الوسطاء
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ⬅️ مخصصة لـ static files في الإنتاج
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# إعدادات القوالب
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ✅ قاعدة البيانات حسب البيئة
if ENVIRONMENT == "production":
    DATABASES = {
        'default': dj_database_url.config(default=os.getenv("DATABASE_URL"))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# التحقق من كلمات المرور
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# اللغة والوقت
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Asia/Riyadh'
USE_I18N = True
USE_TZ = True

# المستخدم المخصص
AUTH_USER_MODEL = 'accounts.User'

# إعادة التوجيه بعد تسجيل الدخول والخروج
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = '/'

# static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ✅ إعداد ملفات media حسب البيئة
if ENVIRONMENT == "production":
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# إعدادات Cloudinary (تعمل في كل البيئات لكن يُستخدم فقط في الإنتاج)
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

# إعدادات أخرى
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
