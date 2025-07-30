from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.wallet.services.bitcoinrpc import BitcoinRPC
from ..models import TransactionHistory, Wallet

class SendBitcoinView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        recipient_address = request.data.get('recipient_address')
        amount = request.data.get('amount')

        if not recipient_address or not amount:
            return Response(
                {"error": "L'adresse du destinataire et le montant sont requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            amount = float(amount)
            if amount <= 0:
                return Response(
                    {"error": "Le montant doit être supérieur à zéro."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {"error": "Le montant doit être un nombre valide."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            wallet = Wallet.objects.get(user=request.user)
        except Wallet.DoesNotExist:
            return Response(
                {"error": "Aucun portefeuille associé à cet utilisateur."},
                status=status.HTTP_404_NOT_FOUND
            )

        rpc = BitcoinRPC()

        try:
            txid = rpc.send_bitcoin(wallet.address, recipient_address, amount)
        except Exception as e:
            return Response(
                {"error": f"Erreur lors de l’envoi : {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        TransactionHistory.objects.create(
            user=request.user,
            txid=txid,
            amount=amount,
            recipient_address=recipient_address,
            status='pending'
        )

        return Response({"txid": txid}, status=status.HTTP_201_CREATED)
