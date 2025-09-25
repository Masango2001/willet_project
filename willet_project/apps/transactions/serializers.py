from rest_framework import serializers
from .models import Transaction, TransactionInput, TransactionOutput

class TransactionOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionOutput
        fields = ['id', 'address', 'amount', 'spent']


class TransactionInputSerializer(serializers.ModelSerializer):
    utxo_amount = serializers.IntegerField(source='utxo.amount', read_only=True)
    utxo_txid = serializers.CharField(source='utxo.txid', read_only=True)
    
    class Meta:
        model = TransactionInput
        fields = ['id', 'utxo', 'utxo_txid', 'utxo_amount']


class TransactionSerializer(serializers.ModelSerializer):
    inputs = TransactionInputSerializer(many=True, required=False)
    outputs = TransactionOutputSerializer(many=True, required=False)
    fee = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id',
            'sender_utxo',
            'recipient_address',
            'amount',
            'fee',
            'txid',
            'status',
            'timestamp',
            'inputs',
            'outputs'
        ]

    def create(self, validated_data):
        inputs_data = validated_data.pop('inputs', [])
        outputs_data = validated_data.pop('outputs', [])

        transaction = Transaction.objects.create(**validated_data)

        for inp in inputs_data:
            TransactionInput.objects.create(transaction=transaction, **inp)
        for out in outputs_data:
            TransactionOutput.objects.create(transaction=transaction, **out)

        # recalculer les frais après création des inputs/outputs
        transaction.fee = transaction.calculate_fee()
        transaction.save()
        return transaction

    def update(self, instance, validated_data):
        # Mettre à jour fields simples
        for attr, value in validated_data.items():
            if attr not in ['inputs', 'outputs']:
                setattr(instance, attr, value)
        instance.save()
        return instance
