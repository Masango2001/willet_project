from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from apps.wallets.models import Wallet, Address
from .models import CustomerUser
from django.contrib.auth import authenticate
from .serializers import CustomerUserSerializer, LoginSerializer
import secrets
from bitcoinlib.wallets import Wallet as BTCWallet


class CustomerUserCreateView(generics.CreateAPIView):
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Génération d'une clé privée aléatoire (64 caractères hex)
        private_key = secrets.token_hex(32)

        # ⚡ Création du wallet Django d'abord pour générer le name automatiquement
        default_wallet = Wallet.objects.create(
            user=user,
            private_key=private_key,  # sera auto-chiffrée dans save()
            lightning_balance=0.0,
            is_default=True
        )

        btc_wallet_name = default_wallet.name  # le nom généré automatiquement par Django

        # Création du wallet Testnet dans Bitcoinlib
        try:
            btc_wallet = BTCWallet.create(
                name=btc_wallet_name,
                keys=private_key,
                network='testnet'
            )
        except Exception as e:
            default_wallet.delete()  # rollback wallet Django
            user.delete()            # rollback user
            return Response(
                {"error": f"Bitcoinlib wallet creation failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Récupération de la première adresse Bitcoin
        first_key = btc_wallet.get_key()
        default_wallet.current_address = first_key.address
        default_wallet.save()

        # Création de l'objet Address pour suivre les adresses
        Address.objects.create(
            wallet=default_wallet,
            address=first_key.address,
            index=0,
            used=False
        )

        # Génération du token JWT
        refresh = RefreshToken.for_user(user)

        return Response({
            "user": CustomerUserSerializer(user).data,
            "default_wallet": {
                "id": default_wallet.id,
                "name": default_wallet.name,  # wallet-<uuid>
                "current_address": default_wallet.current_address,
                "onchain_balance": str(default_wallet.onchain_balance()),
                "lightning_balance": str(default_wallet.lightning_balance),
            },
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class CustomerUserListView(generics.ListAPIView):
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerUserSerializer
    permission_classes = [permissions.IsAuthenticated]

class CustomerUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerUserSerializer
    permission_classes = [permissions.IsAuthenticated]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(email=serializer.validated_data['email'], 
                            password=serializer.validated_data['password'])

        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
