# apps/wallets/serializers.py
from rest_framework import serializers
from .models import Wallet, Address, UTXO

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'wallet', 'address', 'index', 'used', 'created_at']
        read_only_fields = ['id', 'wallet', 'address', 'index', 'created_at']

class WalletSerializer(serializers.ModelSerializer):
    total_balance = serializers.SerializerMethodField()
    onchain_balance = serializers.SerializerMethodField()
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = Wallet
        fields = [
            'id', 'user', 'name', 'current_address', 'private_key',
            'onchain_balance', 'lightning_balance', 'total_balance',
            'is_default', 'created_at', 'updated_at', 'addresses'
        ]
        read_only_fields = [
            'id', 'user', 'onchain_balance', 'total_balance', 'created_at', 'updated_at', 'addresses'
        ]

    def get_total_balance(self, obj):
        return obj.total_balance()

    def get_onchain_balance(self, obj):
        return obj.onchain_balance()

class UTXOSerializer(serializers.ModelSerializer):
    class Meta:
        model = UTXO
        fields = ['id', 'wallet', 'txid', 'vout', 'amount', 'confirmations', 'script_pub_key', 'spent', 'created_at']
        read_only_fields = ['id', 'created_at']
