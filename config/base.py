# willet_project/settings/base.py

import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# Chargement des variables d'environnement depuis .env
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=BASE_DIR / '.env')

# --------------------------------------------------
# Clé secrète et Debug
# --------------------------------------------------
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-secret-key')
DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 'yes']

# --------------------------------------------------
# Hôtes autorisés
# --------------------------------------------------
allowed_hosts_env = os.getenv('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',')] if allowed_hosts_env else []

# --------------------------------------------------
# Applications installées
# --------------------------------------------------
INSTALLED_APPS = [
    # Apps Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Librairies tierces
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'drf_yasg',

    # Apps locales
    'apps.users',
    'apps.wallets',
    'apps.transactions',
    'apps.lightning',
]

# --------------------------------------------------
# Middleware
# --------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Avant CommonMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --------------------------------------------------
# URL root
# --------------------------------------------------
ROOT_URLCONF = 'willet_project.urls'

# --------------------------------------------------
# Templates
# --------------------------------------------------
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

# --------------------------------------------------
# WSGI
# --------------------------------------------------
WSGI_APPLICATION = 'willet_project.wsgi.application'

# --------------------------------------------------
# Base de données (SQLite par défaut)
# --------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,
            'check_same_thread': False,  # <- important
        },
    }
}


# --------------------------------------------------
# Utilisateur personnalisé
# --------------------------------------------------
AUTH_USER_MODEL = 'users.CustomerUser'

# --------------------------------------------------
# Django REST Framework
# --------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# --------------------------------------------------
# Internationalisation
# --------------------------------------------------
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --------------------------------------------------
# Fichiers statiques
# --------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# --------------------------------------------------
# CORS
# --------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True  # À limiter en production

# --------------------------------------------------
# Bitcoin RPC (variables sensibles dans .env)
# --------------------------------------------------
BITCOIN_RPC_USER = os.getenv('BITCOIN_RPC_USER', 'masango')
BITCOIN_RPC_PASSWORD = os.getenv('BITCOIN_RPC_PASSWORD', 'masango2')
BITCOIN_RPC_URL = os.getenv('BITCOIN_RPC_URL')
BITCOIN_RPC_HOST = os.getenv('BITCOIN_RPC_HOST', '127.0.0.1')
BITCOIN_RPC_PORT = os.getenv('BITCOIN_RPC_PORT', '18332')

# --------------------------------------------------
# LND gRPC / Lightning
# --------------------------------------------------
LND_GRPC_HOST = os.getenv('LND_GRPC_HOST', '127.0.0.1')
LND_GRPC_PORT = int(os.getenv('LND_GRPC_PORT', 10009))
LND_TLS_CERT_PATH = os.getenv(
    'LND_TLS_CERT_PATH',
    os.path.join(os.getenv('LOCALAPPDATA', ''), 'Lnd', 'tls.cert')
)
LND_MACAROON_PATH = os.getenv(
    'LND_MACAROON_PATH',
    os.path.join(os.getenv('LOCALAPPDATA', ''), 'Lnd', 'data', 'chain', 'bitcoin', 'testnet', 'admin.macaroon')
)



# --------------------------------------------------
# JWT Simple
# --------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# --------------------------------------------------
# Swagger / drf-yasg
# --------------------------------------------------
# Pas besoin d'ajout ici, tout se configure dans urls.py
# Les endpoints Swagger UI et Redoc seront accessibles via urls.py

#Private Key
