from django.db import models
from apps.wallets.models import UTXO


class Transaction(models.Model):
    sender_utxo = models.ForeignKey(
        UTXO, on_delete=models.CASCADE, related_name='used_in_tx',
        null=True, blank=True
    )  # historique : pour traçabilité d’un envoi simple
    recipient_address = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    fee = models.PositiveIntegerField(default=0)  # en satoshis
    txid = models.CharField(max_length=100, blank=True, null=True)  # identifiant blockchain
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="pending")  # pending / confirmed / failed

    def __str__(self):
        return f"Transaction {self.txid or '(pending)'} → {self.recipient_address} ({self.amount} sats, fee {self.fee} sats)"

    def calculate_fee(self):
        """Calcule les frais comme somme(inputs) - somme(outputs)."""
        total_in = sum(inp.utxo.amount for inp in self.inputs.all())
        total_out = sum(out.amount for out in self.outputs.all())
        return max(total_in - total_out, 0)  # jamais négatif

    def save(self, *args, **kwargs):
        if self.pk:  # seulement si déjà créée (et donc inputs/outputs liés)
            self.fee = self.calculate_fee()
        super().save(*args, **kwargs)


class TransactionInput(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='inputs')
    utxo = models.ForeignKey(UTXO, on_delete=models.CASCADE)

    def __str__(self):
        return f"Input from {self.utxo.txid}:{self.utxo.output_index} ({self.utxo.amount} sats)"


class TransactionOutput(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='outputs')
    address = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    spent = models.BooleanField(default=False)

    def __str__(self):
        return f"Output to {self.address} of {self.amount} sats"