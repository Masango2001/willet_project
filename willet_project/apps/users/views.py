from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import CustomerUser
from .serializers import CustomerUserSerializer, LoginSerializer
from bitcoin.bitcoinrpc import get_rpc_connection  # ✅ on importe la fonction de connexion
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class CustomerUserListCreateView(generics.ListCreateAPIView):
    """
    Vue pour lister tous les utilisateurs et créer un nouvel utilisateur,
    en générant une adresse Bitcoin pour le nouvel utilisateur.
    """
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ✅ Connexion via bitcoinrpc.py
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

class CustomerUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue pour récupérer, mettre à jour ou supprimer un utilisateur spécifique,
    avec vérification du solde de l'adresse Bitcoin.
    """
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # ✅ Connexion via bitcoinrpc.py
        rpc_connection = get_rpc_connection()

        # Vérification du solde de l'adresse Bitcoin avant mise à jour
        try:
            solde = rpc_connection.getreceivedbyaddress(instance.crypto_address)
            print(f"Solde de l'adresse {instance.crypto_address}: {solde} BTC")
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Mise à jour de l'utilisateur
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class LoginView(generics.GenericAPIView):
    """
    Vue pour connecter un utilisateur et générer un jeton JWT.
    """
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Authentification de l'utilisateur
        user = authenticate(username=serializer.validated_data['username'], 
                            password=serializer.validated_data['password'])

        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Génération du jeton
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)