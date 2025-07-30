from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    address = models.CharField(max_length=100, unique=True)  # Adresse BTC
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0.0)  # Solde en BTC
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wallet de {self.user.username} - {self.address}"


class TransactionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    txid = models.CharField(max_length=64, unique=True)  # Identifiant de la transaction BTC
    amount = models.DecimalField(max_digits=20, decimal_places=8)  # Montant de la transaction
    date = models.DateTimeField(auto_now_add=True)  # Date de l'enregistrement
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'En attente'),
            ('confirmed', 'Confirmée')
        ],
        default='pending'
    )
    recipient_address = models.CharField(max_length=100)  # Adresse du destinataire

    def __str__(self):
        return f"{self.user.username} - {self.txid}"
