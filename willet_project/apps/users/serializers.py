from rest_framework import serializers
from .models import CustomerUser

class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['id', 'username', 'email', 'password', 'crypto_address', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True},  # Masquer le mot de passe lors de la récupération
            'crypto_address': {'required': False}  # Optionnel lors de la création
        }

    def create(self, validated_data):
        user = CustomerUser(
            username=validated_data['username'],
            email=validated_data['email'],
            crypto_address=validated_data.get('crypto_address', ''),
        )
        user.set_password(validated_data['password'])  # Hashage du mot de passe
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.crypto_address = validated_data.get('crypto_address', instance.crypto_address)

        # Mise à jour du mot de passe si fourni
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)