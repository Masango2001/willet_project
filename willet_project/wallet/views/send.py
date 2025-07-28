 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..services.rpc_client import BitcoinRPC
from ..models import TransactionHistory

class SendBitcoinView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        recipient_address = request.data.get('recipient_address')
        amount = request.data.get('amount')
        rpc = BitcoinRPC()
        txid = rpc.send_bitcoin(request.user.bitcoin_address, recipient_address, amount)
        TransactionHistory.objects.create(
            user=request.user,
            txid=txid,
            amount=amount,
            recipient_address=recipient_address,
            status='pending'
        )
        return Response({'txid': txid})