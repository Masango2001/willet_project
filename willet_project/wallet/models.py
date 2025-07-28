from django.db import models
from django.contrib.auth import get_user_model

class TransactionHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    txid = models.CharField(max_length=64, unique=True)  # Identifiant de la transaction
    amount = models.DecimalField(max_digits=20, decimal_places=8)  # Montant en BTC
    date = models.DateTimeField(auto_now_add=True)  # Date de la transaction
    status = models.CharField(max_length=20, choices=[('pending', 'En attente'), ('confirmed', 'Confirmé')])
    recipient_address = models.CharField(max_length=100)  # Adresse du destinataire

    def __str__(self):
        return f"{self.user.username} - {self.txid}"