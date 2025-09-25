from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Wallet, UTXO
from .serializers import WalletSerializer, UTXOSerializer
from bitcoinrpc.authproxy import JSONRPCException
from bitcoin.bitcoinrpc import get_rpc_connection


class WalletListCreateView(generics.ListCreateAPIView):
    """
    Vue pour lister tous les portefeuilles et créer un nouveau portefeuille Bitcoin.
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Créer un nouveau wallet pour l'utilisateur
        wallet = Wallet(user=request.user, balance=0)

        # Générer une nouvelle adresse Bitcoin via RPC
        try:
            rpc_connection = get_rpc_connection()
            bitcoin_address = rpc_connection.getnewaddress()  # Nouvelle adresse Bitcoin
            wallet.public_key = bitcoin_address  # Stocker l'adresse dans le champ public_key
        except JSONRPCException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Enregistrer le wallet
        wallet.save()

        # Retourner les données via le serializer
        serializer = self.get_serializer(wallet)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
    Vue pour lister tous les UTXOs d'un portefeuille Bitcoin.
    """
    serializer_class = UTXOSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        wallet_id = self.kwargs['wallet_id']
        wallet = Wallet.objects.get(id=wallet_id)

        try:
            rpc_connection = get_rpc_connection()
            utxos = rpc_connection.listunspent(0, 9999999, [wallet.public_key])

            # Convertir les UTXOs RPC en objets Django temporaires pour le serializer
            utxo_objects = []
            for utxo in utxos:
                utxo_objects.append(UTXO(
                    wallet=wallet,
                    txid=utxo['txid'],
                    output_index=utxo['vout'],
                    amount=int(utxo['amount'] * 1e8),  # convertir en satoshis
                    spent=False
                ))
            return utxo_objects
        except JSONRPCException as e:
            return []
