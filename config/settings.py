import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# ✅ تحميل متغيرات البيئة من ملف .env
load_dotenv()

# 📍 نوع البيئة: development أو production
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# 📁 المسار الأساسي
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 المفتاح السري
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise Exception("❌ SECRET_KEY is not set in environment variables.")

# ✅ وضع DEBUG
DEBUG = ENVIRONMENT == "development"

# ✅ السماح بالمضيفين بناءً على البيئة
if DEBUG:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
else:
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

print("🔍 DEBUG =", DEBUG)
print("🔍 ALLOWED_HOSTS =", ALLOWED_HOSTS)

# ✅ التطبيقات المثبتة
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # تطبيقات المشروع
    'stores.apps.StoresConfig',
    'accounts',
    'orders',
    'delivery',
    'news',
    'ads',
    'core',

    # إضافات
    'widget_tweaks',
    'cloudinary',
    'cloudinary_storage',
]

# ✅ الوسطاء
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # لدعم static في الإنتاج
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ✅ إعدادات URLs و WSGI
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# ✅ إعدادات القوالب
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# ✅ إعدادات قاعدة البيانات (توافق مع Render)
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv("DATABASE_URL" if not DEBUG else "DEV_DATABASE_URL")
    )
}

# ✅ إعدادات كلمات المرور
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ✅ اللغة والمنطقة الزمنية
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Asia/Riyadh'
USE_I18N = True
USE_TZ = True

# ✅ المستخدم المخصص
AUTH_USER_MODEL = 'accounts.User'

# ✅ إعادة التوجيه بعد تسجيل الدخول والخروج
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = '/'

# ✅ إعدادات static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ✅ إعدادات media files
if DEBUG:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
else:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'  # احتياطي للإدارة

# ✅ إعدادات Cloudinary
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

# ✅ إعدادات افتراضية للنماذج
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ دعم HTTPS في Render أو أي Reverse Proxy
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
