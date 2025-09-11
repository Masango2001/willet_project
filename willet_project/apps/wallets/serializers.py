from rest_framework import serializers
from .models import Wallet, UTXO

class UTXOSerializer(serializers.ModelSerializer):
    class Meta:
        model = UTXO
        fields = ['id', 'txid', 'output_index', 'amount', 'spent']

class WalletSerializer(serializers.ModelSerializer):
    utxos = UTXOSerializer(many=True, required=False)

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'public_key', 'private_key', 'balance', 'utxos']

    def create(self, validated_data):
        utxos_data = validated_data.pop('utxos', [])
        wallet = Wallet.objects.create(**validated_data)
        
        for utxo_data in utxos_data:
            UTXO.objects.create(wallet=wallet, **utxo_data)
        
        return wallet

    def update(self, instance, validated_data):
        utxos_data = validated_data.pop('utxos', [])

        # Update wallet fields
        instance.public_key = validated_data.get('public_key', instance.public_key)
        instance.private_key = validated_data.get('private_key', instance.private_key)
        instance.balance = validated_data.get('balance', instance.balance)
        instance.save()

        # Handle UTXOs
        for utxo_data in utxos_data:
            UTXO.objects.update_or_create(
                wallet=instance,
                txid=utxo_data.get('txid'),
                output_index=utxo_data.get('output_index'),
                defaults=utxo_data
            )

        return instance