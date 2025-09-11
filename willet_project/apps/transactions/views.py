# views.py
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from bitcoinrpc.authproxy import JSONRPCException

from .models import Transaction, TransactionInput, TransactionOutput
from apps.wallets.models import UTXO
from .serializers import TransactionSerializer
from bitcoin.bitcoinrpc import get_rpc_connection  # Importation de la fonction

# --- Vue pour lister et créer des transactions ---
class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Création d'une transaction Bitcoin :
        - Vérifie le solde disponible dans le UTXO
        - Appelle Bitcoin Core pour créer et envoyer la transaction
        - Marque le UTXO comme dépensé
        - Crée les inputs/outputs en base
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        sender_utxo = validated_data['sender_utxo']
        recipient_address = validated_data['recipient_address']
        amount = validated_data['amount']

        # Vérification que le UTXO n'est pas déjà dépensé
        if sender_utxo.spent:
            return Response({"error": "UTXO déjà dépensé"}, status=status.HTTP_400_BAD_REQUEST)

        # Vérification du solde disponible
        if sender_utxo.amount < amount:
            return Response({"error": "Solde insuffisant"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rpc_connection = get_rpc_connection()

            # --- Préparer la transaction ---
            raw_tx = rpc_connection.createrawtransaction(
                [{"txid": sender_utxo.txid, "vout": sender_utxo.output_index}],
                {recipient_address: amount / 1e8}  # Conversion satoshis -> BTC
            )

            # --- Signer la transaction ---
            signed_tx = rpc_connection.signrawtransactionwithwallet(raw_tx)

            if not signed_tx.get("complete", False):
                return Response({"error": "Impossible de signer la transaction"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # --- Diffuser la transaction ---
            txid = rpc_connection.sendrawtransaction(signed_tx["hex"])

        except JSONRPCException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # --- Mettre à jour l'UTXO (dépensé) ---
        sender_utxo.spent = True
        sender_utxo.save()

        # --- Créer l'objet Transaction dans la DB ---
        transaction = Transaction.objects.create(
            sender_utxo=sender_utxo,
            recipient_address=recipient_address,
            amount=amount,
            status="pending"
        )

        # --- Créer l'input lié ---
        TransactionInput.objects.create(transaction=transaction, utxo=sender_utxo)

        # --- Créer l'output vers le destinataire ---
        TransactionOutput.objects.create(transaction=transaction, address=recipient_address, amount=amount)

        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)


# --- Vue pour récupérer une transaction ---
class TransactionRetrieveView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        Récupère une transaction dans la base
        + met à jour son statut en vérifiant sur Bitcoin Core.
        """
        transaction = self.get_object()
        serializer = self.get_serializer(transaction)

        try:
            rpc_connection = get_rpc_connection()

            # Vérifie l'état de la transaction sur le réseau Bitcoin
            tx_info = rpc_connection.gettransaction(transaction.sender_utxo.txid)
            confirmations = tx_info.get("confirmations", 0)

            if confirmations > 0 and transaction.status != "confirmed":
                transaction.status = "confirmed"
                transaction.save()

        except JSONRPCException:
            # Si la transaction n'existe pas encore sur le réseau, on ignore
            pass

        return Response(serializer.data)