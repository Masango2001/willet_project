from rest_framework import serializers
from .models import LightningInvoice, LightningPayment

class LightningInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LightningInvoice
        fields = ['id','wallet','invoice','amount_sats','paid','paid_at']

class LightningPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LightningPayment
        fields = ['id','wallet','invoice','amount_sats','status','created_at','updated_at']
