# apps/wallets/serializers.py
from rest_framework import serializers
from .models import Wallet, UTXO

class WalletSerializer(serializers.ModelSerializer):
    total_balance = serializers.DecimalField(max_digits=20, decimal_places=8, read_only=True)

    class Meta:
        model = Wallet
        fields = [
            'id', 'user', 'name', 'current_address',
            'onchain_balance', 'lightning_balance', 'total_balance', 'is_default',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'onchain_balance', 'lightning_balance', 'created_at', 'updated_at']
class UTXOSerializer(serializers.ModelSerializer):
    class Meta:
        model = UTXO
        fields = ['id', 'wallet', 'txid', 'vout', 'amount', 'confirmations', 'script_pub_key', 'spent', 'created_at']
        read_only_fields = ['id', 'created_at']
