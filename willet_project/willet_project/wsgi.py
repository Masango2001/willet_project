import os
from django.core.wsgi import get_wsgi_application

# Définit la variable d'environnement DJANGO_SETTINGS_MODULE qui indique à Django
# quel fichier de configuration utiliser (ici 'willet_project.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'willet_project.settings')

# Crée et expose l'application WSGI Django (un callable Python que le serveur web utilise)
application = get_wsgi_application()
