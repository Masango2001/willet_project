# apps/transactions/models.py
from django.db import models
from django.conf import settings
from apps.wallets.models import Wallet, UTXO, Address
from decimal import Decimal

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('broadcasted', 'Broadcasted'),
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    txid = models.CharField(max_length=255, unique=True, blank=True, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    to_address = models.CharField(max_length=255)
    fee = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.0'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Tx {self.txid} ({self.amount} BTC) status={self.status}"

class TransactionInput(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="inputs")
    utxo = models.ForeignKey(UTXO, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=8)

    def __str__(self):
        return f"Input {self.utxo.txid}:{self.utxo.vout} ({self.amount} BTC)"

class TransactionOutput(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="outputs")
    address = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=8)

    def __str__(self):
        return f"Output {self.address} ({self.amount} BTC)"
