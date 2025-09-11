from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Wallet, UTXO
from .serializers import WalletSerializer, UTXOSerializer
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from bitcoinrpc.authproxy import JSONRPCException
from bitcoin.bitcoinrpc import get_rpc_connection  # Importation depuis bitcoin/bitcoinrpc

class WalletListCreateView(generics.ListCreateAPIView):
    """
    Vue pour lister tous les portefeuilles et créer un nouveau portefeuille.
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Génération des clés
        wallet = Wallet()
        self.generate_keys(wallet)  # Appel à la méthode pour générer les clés
        wallet.user = request.user  # Associer le portefeuille à l'utilisateur

        # Créer une nouvelle adresse Bitcoin via RPC
        try:
            rpc_connection = get_rpc_connection()  # Obtenir la connexion RPC
            bitcoin_address = rpc_connection.getnewaddress()  # Crée une nouvelle adresse
            wallet.public_key = bitcoin_address  # Associe l'adresse à la clé publique
        except JSONRPCException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Enregistrer le portefeuille
        wallet.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def generate_keys(self, wallet):
        """Générer une paire de clés RSA et les associer au portefeuille."""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()

        wallet.private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL
        ).decode('utf-8')

        wallet.public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

class WalletRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue pour récupérer, mettre à jour ou supprimer un portefeuille spécifique.
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class WalletUTXOListView(generics.ListAPIView):
    """
    Vue pour lister tous les UTXOs d'un portefeuille spécifique.
    """
    serializer_class = UTXOSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        wallet_id = self.kwargs['wallet_id']
        wallet = Wallet.objects.get(id=wallet_id)

        # Récupération des UTXOs via RPC
        try:
            rpc_connection = get_rpc_connection()  # Obtenir la connexion RPC
            utxos = rpc_connection.listunspent(0, 9999999, [wallet.public_key])  # Récupérer les UTXOs de l'adresse
            return utxos  # Vous devrez peut-être les convertir en un format approprié
        except JSONRPCException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)