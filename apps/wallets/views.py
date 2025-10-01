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
        # Création du wallet Django (sans onchain_balance)
        wallet = Wallet.objects.create(user=request.user)
        
        # Création du wallet Bitcoin Testnet
        btc_wallet = BTCWallet.create(
            name=f"user-{request.user.id}-{wallet.id}",
            network='testnet'
        )
        
        # Récupération de l'adresse et de la clé WIF
        wallet.current_address = btc_wallet.get_key().address
        wallet.private_key = btc_wallet.get_key().wif  # sera chiffrée dans save()
        wallet.save()
        
        # Retour des données avec solde calculé
        data = WalletSerializer(wallet).data
        data['onchain_balance'] = str(wallet.onchain_balance())  # ⚡ méthode
        data['total_balance'] = str(wallet.total_balance())

        return Response(data, status=status.HTTP_201_CREATED)
    
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

        # Récupération du wallet (par ID ou wallet par défaut)
        if wallet_id:
            try:
                wallet = Wallet.objects.get(id=wallet_id, user=request.user)
            except Wallet.DoesNotExist:
                return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                wallet = Wallet.objects.get(user=request.user, is_default=True)
            except Wallet.DoesNotExist:
                return Response({"error": "No default wallet found"}, status=status.HTTP_404_NOT_FOUND)

        # --- Synchronisation Testnet ---
        try:
            btc_wallet = BTCWallet(wallet.name)  # ouvre le wallet Bitcoin Testnet
            btc_wallet.utxos_update()            # récupère les UTXOs non dépensés Testnet
        except Exception as e:
            return Response({"error": f"Bitcoinlib wallet sync failed: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Calcul du solde onchain dynamiquement depuis les UTXOs
        onchain_balance = wallet.onchain_balance()

        return Response({
            "wallet": wallet.name,
            "current_address": wallet.current_address,
            "onchain_balance": str(onchain_balance),
            "lightning_balance": str(wallet.lightning_balance),
            "total_balance": str(wallet.total_balance()),
        })