 
from .base import *

# Mode production
DEBUG = False

# Hôtes autorisés
ALLOWED_HOSTS = ['wiltte.com', 'www.wiltte.com']

# Base de données (ex. PostgreSQL pour la production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_variable('wallet_NAME'),
        'USER': get_env_variable('wallet_USER'),
        'PASSWORD': get_env_variable('wallet_PASSWORD'),
        'HOST': get_env_variable('wallet_HOST'),
        'PORT': get_env_variable('wallet_PORT'),
    }
}

# Sécurité supplémentaire
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True