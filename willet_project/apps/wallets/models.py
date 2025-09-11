from decimal import Decimal
from django.db import models
from django.conf import settings

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    public_key = models.CharField(max_length=255)
    private_key = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.00'))

    def __str__(self):
        return f"Wallet of {self.user.username}"

    def get_balance(self):
        total_balance = self.utxos.filter(spent=False).aggregate(models.Sum('amount'))['amount__sum'] or 0
        return total_balance


class UTXO(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='utxos')
    txid = models.CharField(max_length=100)
    output_index = models.IntegerField()
    amount = models.PositiveIntegerField()  # en satoshis
    spent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.amount} sats | Spent: {self.spent} | TXID: {self.txid}"