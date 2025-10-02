from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from .models import Wallet, UTXO
from django.shortcuts import get_object_or_404
from .models import Wallet, Address
from .serializers import WalletSerializer
from bitcoinlib.wallets import Wallet as BTCWallet


# --- Création de wallet ---
class WalletCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wallet = Wallet.objects.create(user=request.user)

        # Création du wallet Bitcoin Testnet
        btc_wallet = BTCWallet.create(
            name=f"user-{request.user.id}-{wallet.id}",
            network='testnet'
        )

        # Récupération de l'adresse et de la clé privée
        key = btc_wallet.get_key()
        wallet.current_address = key.address
        wallet.private_key = key.wif  # sera chiffrée dans save()
        wallet.save()

        # Sauvegarde aussi la première adresse dans Address
        Address.objects.create(
            wallet=wallet,
            address=key.address,
            index=0,
            used=False
        )

        data = WalletSerializer(wallet).data
        data['onchain_balance'] = str(wallet.onchain_balance())
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

        if wallet_id:
            wallet = get_object_or_404(Wallet, id=wallet_id, user=request.user)
        else:
            wallet = get_object_or_404(Wallet, user=request.user, is_default=True)

        try:
            btc_wallet = BTCWallet(wallet.name)
            btc_wallet.utxos_update()
        except Exception as e:
            return Response({"error": f"Bitcoinlib wallet sync failed: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        onchain_balance = wallet.onchain_balance()

        return Response({
            "wallet": wallet.name,
            "current_address": wallet.current_address,
            "onchain_balance": str(onchain_balance),
            "lightning_balance": str(wallet.lightning_balance),
            "total_balance": str(wallet.total_balance()),
        })


# --- Génération d'une nouvelle adresse ---
class GenerateNewAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wallet_id = request.data.get("wallet_id")
        if not wallet_id:
            return Response({"error": "wallet_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        wallet = get_object_or_404(Wallet, id=wallet_id, user=request.user)

        try:
            btc_wallet = BTCWallet(wallet.name)
        except Exception as e:
            return Response(
                {"error": f"Impossible d'ouvrir le wallet Bitcoinlib: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Compte combien d'adresses on a déjà dans notre base
        next_index = wallet.addresses.count()

        try:
            # ⚡ Génère une nouvelle clé via bitcoinlib
            key = btc_wallet.new_key()
            new_address = key.address
        except Exception as e:
            return Response(
                {"error": f"Erreur lors de la génération de l'adresse: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # On enregistre dans notre modèle Django
        Address.objects.create(
            wallet=wallet,
            address=new_address,
            index=next_index,
            used=False
        )

        wallet.current_address = new_address
        wallet.save()

        return Response({
            "wallet_id": wallet.id,
            "new_address": new_address,
            "index": next_index,
            "current_address": wallet.current_address,
        }, status=status.HTTP_201_CREATED)


class SyncUTXOView(APIView):
    """
    Synchronise les UTXO d'un wallet Bitcoin testnet via bitcoinlib
    et les enregistre/actualise dans la base Django.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wallet_id = request.data.get('wallet_id')
        if not wallet_id:
            return Response(
                {"error": "wallet_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifie que le wallet Django appartient bien à l'utilisateur connecté
        wallet = get_object_or_404(Wallet, id=wallet_id, user=request.user)

        try:
            # Ouvre le wallet Bitcoinlib
            btc_wallet = BTCWallet(wallet.name)

            # Mets à jour les UTXOs (⚠️ sans providers)
            btc_wallet.utxos_update()

            # Récupère le solde actuel
            balance = btc_wallet.balance()
        except Exception as e:
            return Response(
                {"error": f"Bitcoinlib sync failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Synchronise les UTXOs dans la DB Django
        synced_utxos = []
        for utxo in btc_wallet.utxos():
            obj, created = UTXO.objects.update_or_create(
                wallet=wallet,
                txid=utxo["txid"],
                vout=utxo["output_n"],
                defaults={
                    'amount': Decimal(utxo["value"]) / Decimal("1e8"),  # satoshis → BTC
                    'confirmations': utxo.get("confirmations", 0),
                    'script_pub_key': utxo.get("script_hex", ""),
                    'spent': utxo.get("spent", False),
                }
            )

            synced_utxos.append({
                "txid": obj.txid,
                "vout": obj.vout,
                "amount": str(obj.amount),
                "confirmations": obj.confirmations,
                "spent": obj.spent,
                "script_pub_key": obj.script_pub_key,
            })

        return Response({
            "wallet": wallet.name,
            "balance": str(balance),
            "utxos_count": len(synced_utxos),
            "utxos": synced_utxos
        }, status=status.HTTP_200_OK)
