from django.db import models
from apps.wallets.models import UTXO

class Transaction(models.Model):
    sender_utxo = models.ForeignKey(UTXO, on_delete=models.CASCADE, related_name='used_in_tx')
    recipient_address = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="pending")  # ou "confirmed"

    def __str__(self):
        return f"Transaction of {self.amount} sats to {self.recipient_address}"

class TransactionInput(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='inputs')
    utxo = models.ForeignKey(UTXO, on_delete=models.CASCADE)

    def __str__(self):
        return f"Input from {self.utxo}"

class TransactionOutput(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='outputs')
    address = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"Output to {self.address} of {self.amount} sats"