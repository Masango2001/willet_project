 
import os
from .base import *

# Charge les paramètres selon l'environnement
ENVIRONMENT = os.getenv('DJANGO_ENV', 'development')

if ENVIRONMENT == 'production':
    from .production import *
else:
    from .development import *