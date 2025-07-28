 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..services.rpc_client import BitcoinRPC

class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rpc = BitcoinRPC()
        balance = rpc.get_balance(request.user.bitcoin_address)
        return Response({'balance': balance})