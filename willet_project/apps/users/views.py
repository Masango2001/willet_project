from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import CustomerUser
from .serializers import CustomerUserSerializer, LoginSerializer
from bitcoin.bitcoinrpc import get_rpc_connection
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# ✅ Vue pour créer un utilisateur (publique)
class CustomerUserCreateView(generics.CreateAPIView):
    """
    Création d'un nouvel utilisateur avec génération d'adresse Bitcoin.
    Accessible par tout le monde.
    """
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerUserSerializer
    permission_classes = [permissions.AllowAny]  # Tout le monde peut créer un compte

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Connexion via bitcoinrpc.py
        rpc_connection = get_rpc_connection()

        # Génération d'une nouvelle adresse Bitcoin
        try:
            nouvelle_adresse = rpc_connection.getnewaddress()
            serializer.validated_data['crypto_address'] = nouvelle_adresse
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Enregistrement de l'utilisateur
        user = serializer.save()

        # Génération d'un jeton JWT après l'enregistrement
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": serializer.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


# ✅ Vue pour lister les utilisateurs (protégée)
class CustomerUserListView(generics.ListAPIView):
    """
    Liste des utilisateurs protégée par authentification.
    """
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerUserSerializer
    permission_classes = [permissions.IsAuthenticated]


# Vue pour récupérer, mettre à jour ou supprimer un utilisateur spécifique
class CustomerUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        rpc_connection = get_rpc_connection()

        try:
            solde = rpc_connection.getreceivedbyaddress(instance.crypto_address)
            print(f"Solde de l'adresse {instance.crypto_address}: {solde} BTC")
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# Vue pour la connexion
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.validated_data['username'], 
                            password=serializer.validated_data['password'])

        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
