# apps/transactions/serializers.py
from rest_framework import serializers
from .models import Transaction, TransactionInput, TransactionOutput

class TransactionInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionInput
        fields = ["utxo", "amount"]

class TransactionOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionOutput
        fields = ["address", "amount"]

class TransactionSerializer(serializers.ModelSerializer):
    inputs = TransactionInputSerializer(many=True, read_only=True)
    outputs = TransactionOutputSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id", "wallet", "txid", "amount", "to_address",
            "fee", "status", "created_at", "updated_at",
            "inputs", "outputs"
        ]
