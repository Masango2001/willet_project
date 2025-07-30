from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.wallet.services.bitcoinrpc import BitcoinRPC
from apps.wallet.models import Wallet

class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            wallet = Wallet.objects.get(user=request.user)
        except Wallet.DoesNotExist:
            return Response(
                {"error": "Portefeuille introuvable pour cet utilisateur."},
                status=status.HTTP_404_NOT_FOUND
            )

        rpc = BitcoinRPC()

        try:
            balance = rpc.get_balance(wallet.address)
        except Exception as e:
            return Response(
                {"error": f"Impossible de récupérer le solde : {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({'balance': balance}, status=status.HTTP_200_OK)
