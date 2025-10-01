from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from apps.wallets.models import Wallet
from .models import CustomerUser
from .serializers import CustomerUserSerializer, LoginSerializer
import secrets
from decimal import Decimal
from bitcoinlib.wallets import Wallet as BTCWallet

class CustomerUserCreateView(generics.CreateAPIView):
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Génération d'une clé privée (hex aléatoire 64 caractères)
        private_key = secrets.token_hex(32)  

        # Création du wallet Testnet dans Bitcoinlib
        btc_wallet_name = f"user-{user.id}-default-wallet"
        try:
            btc_wallet = BTCWallet.create(
                name=btc_wallet_name,
                keys=private_key,
                network='testnet'
            )
        except Exception as e:
            user.delete()
            return Response(
                {"error": f"Bitcoinlib wallet creation failed: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Création du wallet par défaut dans Django (sans onchain_balance !)
        default_wallet = Wallet.objects.create(
            user=user,
            name=btc_wallet_name,
            current_address=btc_wallet.get_key().address,
            private_key=private_key,  # sera auto-chiffrée via save()
            lightning_balance=0.0,
            is_default=True
        )

        # Génération du token JWT
        refresh = RefreshToken.for_user(user)

        return Response({
            "user": CustomerUserSerializer(user).data,
            "default_wallet": {
                "id": default_wallet.id,
                "name": default_wallet.name,
                "current_address": default_wallet.current_address,
                "onchain_balance": str(default_wallet.onchain_balance()),  # ⚡ appeler la méthode
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
