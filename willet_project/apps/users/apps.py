from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"   # chemin Python vers l'app
    label = "users"       # <- app_label utilisé par Django
