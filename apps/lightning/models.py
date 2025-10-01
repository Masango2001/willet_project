from django.db import models
from apps.wallets.models import Wallet

class LightningInvoice(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="invoices")
    invoice = models.TextField(unique=True)
    amount_sats = models.BigIntegerField()
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Invoice {self.invoice[:15]}... ({'Paid' if self.paid else 'Pending'})"

class LightningPayment(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="payments")
    invoice = models.ForeignKey(LightningInvoice, on_delete=models.CASCADE)
    amount_sats = models.BigIntegerField()
    status = models.CharField(
        max_length=50,
        choices=[('pending','Pending'),('failed','Failed'),('confirmed','Confirmed')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
