from rest_framework import serializers
from .models import Transaction, TransactionInput, TransactionOutput

class TransactionOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionOutput
        fields = ['id', 'address', 'amount']

class TransactionInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionInput
        fields = ['id', 'utxo']

class TransactionSerializer(serializers.ModelSerializer):
    inputs = TransactionInputSerializer(many=True, required=False)
    outputs = TransactionOutputSerializer(many=True, required=False)

    class Meta:
        model = Transaction
        fields = ['id', 'sender_utxo', 'recipient_address', 'amount', 'timestamp', 'status', 'inputs', 'outputs']

    def create(self, validated_data):
        inputs_data = validated_data.pop('inputs', [])
        outputs_data = validated_data.pop('outputs', [])
        
        transaction = Transaction.objects.create(**validated_data)
        
        for input_data in inputs_data:
            TransactionInput.objects.create(transaction=transaction, **input_data)
        
        for output_data in outputs_data:
            TransactionOutput.objects.create(transaction=transaction, **output_data)
        
        return transaction

    def update(self, instance, validated_data):
        inputs_data = validated_data.pop('inputs', [])
        outputs_data = validated_data.pop('outputs', [])

        # Update fields of the transaction itself
        instance.sender_utxo = validated_data.get('sender_utxo', instance.sender_utxo)
        instance.recipient_address = validated_data.get('recipient_address', instance.recipient_address)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        # Handle inputs
        for input_data in inputs_data:
            TransactionInput.objects.update_or_create(
                transaction=instance,
                utxo=input_data.get('utxo'),
                defaults=input_data
            )

        # Handle outputs
        for output_data in outputs_data:
            TransactionOutput.objects.update_or_create(
                transaction=instance,
                address=output_data.get('address'),
                defaults=output_data
            )

        return instance