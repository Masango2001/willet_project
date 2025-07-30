from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Wallet, TransactionHistory

User = get_user_model()

class WalletSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'address', 'balance', 'created_at']
        read_only_fields = ['id', 'balance', 'created_at']


class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TransactionHistory
        fields = ['id', 'user', 'txid', 'amount', 'date', 'status', 'recipient_address']
        read_only_fields = ['id', 'date', 'status', 'txid']
