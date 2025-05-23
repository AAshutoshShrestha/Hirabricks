from pathlib import Path
import os
from dotenv import load_dotenv
# admin panel jazmin theme
from .jazminSetup import JAZZMIN_SETTINGS,JAZZMIN_UI_TWEAKS

# Load environment variables from .env file
load_dotenv()



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = ["127.0.0.1", ".vercel.app", ".now.sh","*"]


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'graphene_django',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.admindocs',
    'import_export',
    'Homepage',
    'docs',
    'example',
    'conditions',
    'Resources',
    'Machines',
    'Inventory',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vercel_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join( BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'Homepage.context_processors.base_context',
            ],
            'builtins':[
                'example.templatetags.app_filters',  
                ]
        },
    },
]


WSGI_APPLICATION = 'vercel_app.wsgi.app'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('SUPABASE_DATABASE'),
        'USER': os.environ.get('SUPABASE_USER'),
        'PASSWORD': os.environ.get('SUPABASE_PASSWORD'),
        'HOST': os.environ.get('SUPABASE_HOST'), # Usually something like '<your_project_id>.supabase.co'
        'PORT': os.environ.get('SUPABASE_PORT'),  # Default PostgreSQL port
        'CONN_MAX_AGE': 600,  # Connection timeout in seconds, adjust as needed
        'OPTIONS': {
            'sslmode': 'require',  # Enable SSL mode for security
        },
        'POOL_SIZE': 10,  # Number of connections in the pool, adjust as needed
        'POOL_TIMEOUT': 10,  # Maximum number of seconds to wait for a connection from the pool, adjust as needed
    }
}

# Adjust concurrency settings for import-export
IMPORT_EXPORT_USE_TRANSACTIONS = True
IMPORT_EXPORT_ASYNC_IMPORT = True
IMPORT_EXPORT_ASYNC_EXPORT = True

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_TZ = False

USE_L10N = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGES = (
    ('ne', 'Nepali'),
    ('en', 'English'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

MEDIA_URL = 'var/task/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIAFILE_DIRS =[
    os.path.join( BASE_DIR, 'media')
]


JAZZMIN_SETTINGS = JAZZMIN_SETTINGS
JAZZMIN_UI_TWEAKS = JAZZMIN_UI_TWEAKS