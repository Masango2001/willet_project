 
from .base import *

# Mode débogage
DEBUG = True

# Hôtes autorisés
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Base de données (peut rester SQLite pour le développement)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}