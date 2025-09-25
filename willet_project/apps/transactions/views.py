# views.py
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from bitcoinrpc.authproxy import JSONRPCException

from .models import Transaction, TransactionInput, TransactionOutput
from apps.wallets.models import UTXO
from .serializers import TransactionSerializer
from bitcoin.bitcoinrpc import get_rpc_connection  # Fonction RPC Bitcoin


# --- Vue pour lister et créer des transactions ---
class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Création d'une transaction Bitcoin :
        - Vérifie solde du UTXO
        - Crée + signe + envoie la transaction via Bitcoin Core
        - Calcule les frais et le change
        - Met à jour UTXO + enregistre transaction/inputs/outputs
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

        # Vérification du solde
        if sender_utxo.amount < amount:
            return Response({"error": "Solde insuffisant"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rpc_connection = get_rpc_connection()

            # --- Préparer la sortie principale ---
            outputs = {recipient_address: amount / 1e8}  # en BTC

            # --- Calcul du change (si montant restant > 0) ---
            change_amount = sender_utxo.amount - amount
            if change_amount > 0:
                # Renvoyer le change à l'adresse propriétaire du UTXO
                outputs[sender_utxo.address] = change_amount / 1e8

            # --- Créer la transaction brute ---
            raw_tx = rpc_connection.createrawtransaction(
                [{"txid": sender_utxo.txid, "vout": sender_utxo.output_index}],
                outputs
            )

            # --- Signer la transaction ---
            signed_tx = rpc_connection.signrawtransactionwithwallet(raw_tx)
            if not signed_tx.get("complete", False):
                return Response({"error": "Impossible de signer la transaction"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # --- Diffuser la transaction ---
            txid = rpc_connection.sendrawtransaction(signed_tx["hex"])

            # --- Récupérer info pour les frais ---
            tx_info = rpc_connection.decoderawtransaction(signed_tx["hex"])
            vsize = tx_info.get("vsize", 200)  # taille estimée
            feerate = rpc_connection.estimatesmartfee(6)["feerate"]  # BTC/kB
            fee = int(vsize * feerate * 1e5)  # conversion → satoshis

        except JSONRPCException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # --- Mettre à jour l'UTXO source ---
        sender_utxo.spent = True
        sender_utxo.save()

        # --- Créer l'objet Transaction ---
        transaction = Transaction.objects.create(
            sender_utxo=sender_utxo,
            recipient_address=recipient_address,
            amount=amount,
            fee=fee,
            txid=txid,
            status="pending"
        )

        # --- Inputs ---
        TransactionInput.objects.create(transaction=transaction, utxo=sender_utxo)

        # --- Output destinataire ---
        TransactionOutput.objects.create(transaction=transaction, address=recipient_address, amount=amount)

        # --- Output change (si applicable) ---
        if change_amount > 0:
            TransactionOutput.objects.create(transaction=transaction, address=sender_utxo.address, amount=change_amount)

        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)


# --- Vue pour récupérer une transaction ---
class TransactionRetrieveView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        Récupère une transaction en base
        + met à jour son statut via Bitcoin Core.
        """
        transaction = self.get_object()
        serializer = self.get_serializer(transaction)

        try:
            rpc_connection = get_rpc_connection()
            tx_info = rpc_connection.gettransaction(transaction.txid)
            confirmations = tx_info.get("confirmations", 0)

            if confirmations > 0 and transaction.status != "confirmed":
                transaction.status = "confirmed"
                transaction.save()

        except JSONRPCException:
            # Si la transaction n’existe pas encore sur le réseau
            pass

        return Response(serializer.data)
