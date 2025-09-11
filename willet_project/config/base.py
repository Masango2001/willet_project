 
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# Chargement des variables d'environnement depuis le fichier .env
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Adapter selon la profondeur de base.py
load_dotenv(dotenv_path=BASE_DIR / '.env')

# Clé secrète (doit être définie dans .env)
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-secret-key')

# Mode debug par défaut à False
DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 'yes']

# Liste des hôtes autorisés, séparés par des virgules dans .env
allowed_hosts_env = os.getenv('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',')] if allowed_hosts_env else []

# Applications installées
INSTALLED_APPS = [
    # Apps Django par défaut
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Librairies tierces
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',  # Pour gestion blacklist JWT
    'corsheaders',

    # Applications locales
    'apps.users',
    'apps.wallets',
    'apps.transactions',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Doit être avant CommonMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL root configuration
ROOT_URLCONF = 'willet_project.urls'  # Vérifier que ce module existe bien

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Ajouter les chemins vers des dossiers templates personnalisés si besoin
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

# WSGI application
WSGI_APPLICATION = 'willet_project.wsgi.application'

# Base de données (SQLite par défaut, modifiable selon environnement)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / os.getenv('SQLITE_DB_NAME', 'db.sqlite3'),
    }
}

# Utilisateur personnalisé
AUTH_USER_MODEL = 'users.CustomerUser'

# Configuration Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Internationalisation
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Fichiers statiques
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuration CORS (exemple : autoriser tout en dev, restreindre en prod)
CORS_ALLOW_ALL_ORIGINS = True  # À ajuster en production

# Configuration Bitcoin RPC (variables sensibles à définir dans .env)
BITCOIN_RPC_USER = os.getenv('BITCOIN_RPC_USER','masango')
BITCOIN_RPC_PASSWORD = os.getenv('BITCOIN_RPC_PASSWORD','masango2')
BITCOIN_RPC_URL = os.getenv('BITCOIN_RPC_URL')
BITCOIN_RPC_HOST = os.getenv('BITCOIN_RPC_HOST','127.0.0.1')
BITCOIN_RPC_PORT = os.getenv('BITCOIN_RPC_PORT','8332')

# Configuration JWT Simple
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}
