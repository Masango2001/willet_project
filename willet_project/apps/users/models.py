from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomerUser(AbstractUser):
    crypto_address = models.CharField(max_length=255, blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.username