  
from .base import *  # On importe toute la configuration commune

# Activer le mode debug pour afficher les erreurs détaillées
DEBUG = True

# Liste des hôtes autorisés à accéder à l'application en dev
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Configuration de la base de données pour le dev (SQLite ici)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Moteur SQLite, simple et léger
        'NAME': BASE_DIR / 'db.sqlite3',         # Chemin vers la base SQLite locale
    }
}

