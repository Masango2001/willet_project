import os
from django.core.asgi import get_asgi_application

# Définit la variable d'environnement DJANGO_SETTINGS_MODULE
# pour indiquer à Django quel fichier de configuration utiliser
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'willet_project.settings')

# Crée et expose l'application ASGI Django qui sera utilisée par le serveur ASGI
application = get_asgi_application()
