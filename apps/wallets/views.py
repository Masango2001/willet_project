from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from .models import Wallet
from .serializers import WalletSerializer
from bitcoinlib.wallets import Wallet as BTCWallet

# --- Création de wallet ---
class WalletCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wallet = Wallet.objects.create(user=request.user)
        btc_wallet = BTCWallet.create(name=f"user-{request.user.id}-{wallet.id}")
        wallet.current_address = btc_wallet.get_key().address
        wallet.private_key = btc_wallet.get_key().wif  # sera chiffrée automatiquement dans save()
        wallet.save()
        return Response(WalletSerializer(wallet).data, status=status.HTTP_201_CREATED)

# --- Détails / mise à jour / suppression ---
class WalletDetail(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wallet_id = request.data.get('wallet_id')
        if not wallet_id:
            return Response({"error": "wallet_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            wallet = Wallet.objects.get(id=wallet_id, user=request.user)
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(WalletSerializer(wallet).data)

    def put(self, request):
        wallet_id = request.data.get('wallet_id')
        if not wallet_id:
            return Response({"error": "wallet_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            wallet = Wallet.objects.get(id=wallet_id, user=request.user)
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WalletSerializer(wallet, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        wallet_id = request.data.get('wallet_id')
        if not wallet_id:
            return Response({"error": "wallet_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            wallet = Wallet.objects.get(id=wallet_id, user=request.user)
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)
        wallet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --- Consultation du solde ---
class WalletBalance(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wallet_id = request.data.get('wallet_id')
        if not wallet_id:
            return Response({"error": "wallet_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            wallet = Wallet.objects.get(id=wallet_id, user=request.user)
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "wallet": wallet.name,
            "onchain_balance": wallet.onchain_balance,
            "lightning_balance": wallet.lightning_balance,
            "total_balance": wallet.total_balance()
        })
