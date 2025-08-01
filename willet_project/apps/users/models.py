from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bitcoin_address = models.CharField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.username