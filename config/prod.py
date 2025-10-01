 
 
from .base import *  # Importer toute la configuration commune

# Mode production : désactiver le debug
DEBUG = False

# Liste des hôtes/domaines autorisés en production
ALLOWED_HOSTS = ['wiltte.com', 'www.wiltte.com']

# Configuration base de données PostgreSQL (variables d’environnement claires)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_variable('DB_NAME'),         # Nom base de données
        'USER': get_env_variable('DB_USER'),         # Utilisateur PostgreSQL
        'PASSWORD': get_env_variable('DB_PASSWORD'), # Mot de passe utilisateur
        'HOST': get_env_variable('DB_HOST'),         # Adresse serveur PostgreSQL
        'PORT': get_env_variable('DB_PORT'),         # Port PostgreSQL (souvent 5432)
    }
}

# Sécurité renforcée en production

# Redirige toutes les requêtes HTTP vers HTTPS
SECURE_SSL_REDIRECT = True

# Cookies sécurisés : envoyés uniquement via HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Protection contre les attaques XSS côté navigateur
SECURE_BROWSER_XSS_FILTER = True

# Autres options recommandées en prod (optionnel mais conseillé)
SECURE_HSTS_SECONDS = 3600          # HTTP Strict Transport Security (HSTS)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True

