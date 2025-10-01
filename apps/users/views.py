from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from bitcoin.bitcoinrpc import get_rpc_connection
from .models import CustomerUser
from apps.wallets.models import Wallet
import secrets
from .serializers import CustomerUserSerializer, LoginSerializer

class CustomerUserCreateView(generics.CreateAPIView):
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Génération d'une clé privée (ici un hex aléatoire 64 caractères)
        private_key = secrets.token_hex(32)  

        try:
            rpc = get_rpc_connection()
            new_address = rpc.getnewaddress()
        except Exception as e:
            user.delete()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Création du wallet par défaut AVEC clé privée chiffrée
        default_wallet = Wallet.objects.create(
            user=user,
            current_address=new_address,
            private_key=private_key,  # ⚡ sera auto-chiffrée via save()
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
                "onchain_balance": str(default_wallet.onchain_balance),
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
