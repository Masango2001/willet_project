from django.db import models
from django.conf import settings
import uuid
from decimal import Decimal
from django.db.models import Sum
from .utils import encrypt_private_key, decrypt_private_key  # <-- import

class Wallet(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallets"
    )
    name = models.CharField(max_length=100, unique=True, blank=True)
    current_address = models.CharField(max_length=255, blank=True, null=True)
    private_key = models.TextField(blank=True, null=True)  # sera chiffrée
    lightning_balance = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.0'))
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.user.email})"

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"wallet-{uuid.uuid4()}"
        if self.private_key and not self.private_key.startswith("ENC:"):
            self.private_key = "ENC:" + encrypt_private_key(self.private_key)
        super().save(*args, **kwargs)

    def get_private_key(self):
        if self.private_key and self.private_key.startswith("ENC:"):
            return decrypt_private_key(self.private_key[4:])
        return self.private_key

    def onchain_balance(self):
        """
        Calcule dynamiquement le solde onchain à partir des UTXOs non dépensés.
        """
        total = self.utxos.filter(spent=False).aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.0')
        return total

    def total_balance(self):
        """
        Total = onchain + lightning
        """
        return self.onchain_balance() + (self.lightning_balance or Decimal('0.0'))


class UTXO(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="utxos")
    txid = models.CharField(max_length=255)
    vout = models.IntegerField()
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    confirmations = models.IntegerField(default=0)
    script_pub_key = models.CharField(max_length=255, blank=True, null=True)
    spent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('txid', 'vout')
        ordering = ['-created_at']

    def __str__(self):
        return f"UTXO {self.txid}:{self.vout} ({self.amount} BTC)"
