from pathlib import Path
import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q+)z$cqsz5(88fey%kz0efs-m2+)s#+3q-s5%nu(dqnhs@zy8x'

# Enable debug locally so Django serves static files during development.
# In production, this should be False. We read from env, default to True for local dev convenience if not set.
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS = ['.vercel.app', 'kyonkat-pet-service.vercel.app', '127.0.0.1', 'localhost']
ALLOWED_HOSTS = [
    "kyoncat-pet-service.onrender.com",
    "localhost",
    "127.0.0.1",
    ".elasticbeanstalk.com",  # Allow all AWS EB subdomains
    "*", # Allow all for simplicity in this user context, or restrict if they provide domain
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'customer',
    'portal',
    'website',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kyonkat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'kyonkat.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Database Configuration with Debugging
import sys

# Print all env vars to logs (keys only for security) to verify they are loaded
print("DEBUG: Loaded Environment Variables Keys:", list(os.environ.keys()), file=sys.stderr)

db_from_env = dj_database_url.config(conn_max_age=600)
if db_from_env:
    DATABASES['default'].update(db_from_env)
    print("DEBUG: Database config updated from environment.", file=sys.stderr)
else:
    print("DEBUG: No DATABASE_URL or POSTGRES_URL found. Using default SQLite.", file=sys.stderr)
    # Fallback to checking specific Vercel keys if default config() misses them
    if 'POSTGRES_URL' in os.environ:
         DATABASES['default'] = dj_database_url.parse(os.environ.get('POSTGRES_URL'))
         print("DEBUG: Database config updated from POSTGRES_URL manually.", file=sys.stderr)




# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

X_FRAME_OPTIONS = 'SAMEORIGIN'

CSRF_TRUSTED_ORIGINS = [
    'http://kyonkatgroomers.com/', 
    'http://www.kyonkatgroomers.com/', 
    'http://13.234.116.103/',
    'http://kyonkatapp-env.eba-4fptapqs.ap-south-1.elasticbeanstalk.com',
    'https://kyonkatapp-env.eba-4fptapqs.ap-south-1.elasticbeanstalk.com'
]
USE_X_FORWARDED_HOST = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False
