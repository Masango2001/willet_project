import os
from pathlib import Path
from utils.env_loader import get_env_variable

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = get_env_variable('SECRET_KEY')

# DEBUG récupéré depuis .env, par défaut False si non défini
DEBUG = get_env_variable('DEBUG').lower() == 'true' if 'DEBUG' in os.environ else False

# ALLOWED_HOSTS depuis .env, séparés par des virgules, ou liste vide par défaut
ALLOWED_HOSTS = get_env_variable('ALLOWED_HOSTS').split(',') if 'ALLOWED_HOSTS' in os.environ else []

INSTALLED_APPS = [
    'django.contrib.admin',          
    'django.contrib.auth',           
    'django.contrib.contenttypes',   
    'django.contrib.sessions',       
    'django.contrib.messages',       
    'django.contrib.staticfiles',    

    'rest_framework',                
    'rest_framework_simplejwt',     
    'corsheaders',                   

    'users',
    'wallet',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'willet_config.urls'

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

# Base SQLite dont le nom est défini dans .env (SQLITE_DB_NAME), ou db.sqlite3 par défaut
sqlite_name = get_env_variable('SQLITE_DB_NAME') if 'SQLITE_DB_NAME' in os.environ else 'db.sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / sqlite_name,
    }
}

AUTH_USER_MODEL = 'users.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
