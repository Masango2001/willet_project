# apps/transactions/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from bitcoinlib.wallets import Wallet as BTCWallet
from decimal import Decimal

from .models import Transaction, TransactionInput, TransactionOutput
from .serializers import TransactionSerializer
from apps.wallets.models import Wallet, UTXO
from .utils import sync_wallet


class SendTransactionView(APIView):
    """
    Envoie des BTC depuis un wallet vers une adresse.
    Crée la transaction locale et synchronise les UTXOs.
    Permet d'envoyer plusieurs fois à la même adresse.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wallet_id = request.data.get("wallet_id")
        to_address = request.data.get("to_address")
        amount = Decimal(request.data.get("amount"))

        wallet = get_object_or_404(Wallet, id=wallet_id, user=request.user)

        try:
            btc_wallet = BTCWallet(wallet.name)

            # Envoi réel sur le réseau (testnet ou mainnet)
            tx = btc_wallet.send_to(to_address, int(amount * Decimal("1e8")))  # satoshis

            # Création de la transaction locale
            transaction = Transaction.objects.create(
                wallet=wallet,
                txid=tx.txid,
                amount=amount,
                to_address=to_address,
                fee=Decimal(tx.fee) / Decimal("1e8"),
                status="broadcasted"
            )

            # Inputs de la transaction
            for inp in tx.inputs:
                # Récupérer txid en hex
                txid_hex = getattr(inp, "txid", None)
                if not txid_hex:
                    txid_bytes = getattr(inp, "txid_as_bytes", None)
                    if txid_bytes:
                        txid_hex = txid_bytes.hex()
                    else:
                        continue  # skip si pas de txid

                # Récupérer vout et convertir si nécessaire
                vout = getattr(inp, "output_n", None)
                if isinstance(vout, bytes):
                    vout = int.from_bytes(vout, byteorder="little")

                utxo = UTXO.objects.filter(txid=txid_hex, vout=vout).first()
                if utxo:
                    TransactionInput.objects.create(
                        transaction=transaction,
                        utxo=utxo,
                        amount=Decimal(inp.value) / Decimal("1e8")
                    )
                    # Marquer l'UTXO comme dépensé
                    utxo.spent = True
                    utxo.save()

            # Outputs de la transaction
            for out in tx.outputs:
                TransactionOutput.objects.create(
                    transaction=transaction,
                    address=out.address,
                    amount=Decimal(out.value) / Decimal("1e8")
                )

            # 🔄 Synchronisation du wallet après envoi
            sync_wallet(wallet)

            return Response(TransactionSerializer(transaction).data, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class WalletSyncView(APIView):
    """
    Synchronise les UTXOs d'un wallet et met à jour le solde onchain.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wallet_id = request.data.get("wallet_id")
        wallet = get_object_or_404(Wallet, id=wallet_id, user=request.user)

        try:
            utxos = sync_wallet(wallet)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        return Response({
            "wallet": wallet.name,
            "onchain_balance": str(wallet.onchain_balance()),
            "total_balance": str(wallet.total_balance()),
            "utxos": [
                {
                    "txid": u.txid,
                    "vout": u.vout,
                    "amount": str(u.amount),
                    "spent": u.spent,
                    "confirmations": u.confirmations,
                    "script_pub_key": u.script_pub_key or ""
                }
                for u in utxos
            ]
        })
