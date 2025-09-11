import os
from dotenv import load_dotenv

load_dotenv()  

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        raise Exception(f"La variable d'environnement {var_name} est manquante.")
