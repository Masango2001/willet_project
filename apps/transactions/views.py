import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from decimal import Decimal

from .models import Transaction, TransactionInput, TransactionOutput
from .serializers import TransactionSerializer
from apps.wallets.models import Wallet, UTXO
from .utils import sync_wallet

from bitcoinlib.wallets import Wallet as BTCWallet
from bitcoinlib.services.services import Service


class SendTransactionView(APIView):
    """
    Envoie des BTC depuis un wallet vers une adresse.
    Sélectionne automatiquement les UTXO nécessaires.
    Peut envoyer tout le solde disponible avec send_max=True.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wallet_id = request.data.get("wallet_id")
        to_address = request.data.get("to_address")
        amount = request.data.get("amount")
        send_max = request.data.get("send_max", False)

        wallet = get_object_or_404(Wallet, id=wallet_id, user=request.user)

        # Récupération des UTXO confirmés et non dépensés
        utxos = wallet.utxos.filter(confirmations__gt=0, spent=False).order_by('created_at')
        if not utxos.exists():
            return Response({"error": "Aucun UTXO disponible pour ce wallet."}, status=400)

        # Calcul du solde disponible
        total_available = sum([u.amount for u in utxos])
        dust_limit = Decimal("0.00000546")

        if send_max:
            amount = total_available - Decimal("0.00001")  # laisser un petit buffer pour frais
        else:
            amount = Decimal(amount)
            if amount < dust_limit:
                return Response({"error": f"Montant trop petit, min {dust_limit} BTC"}, status=400)
            if amount > total_available:
                return Response({"error": f"Montant supérieur au solde disponible ({total_available} BTC)"}, status=400)

        try:
            btc_wallet = BTCWallet(wallet.name)
            print(f"\n🚀 Création de la transaction pour {amount} BTC...")

            # bitcoinlib se charge de choisir automatiquement les UTXO nécessaires
            tx = btc_wallet.send_to(to_address, int(amount * Decimal("1e8")))
            print(f"✅ Transaction créée avec TXID : {tx.txid}")

            # Création locale dans la base
            transaction = Transaction.objects.create(
                wallet=wallet,
                txid=tx.txid,
                amount=amount,
                to_address=to_address,
                fee=Decimal(tx.fee) / Decimal("1e8"),
                status="broadcasted"
            )

            # Marquer les UTXO utilisés
            for inp in tx.inputs:
                txid_hex = getattr(inp, "txid", None) or getattr(inp, "txid_as_bytes", None)
                if isinstance(txid_hex, bytes):
                    txid_hex = txid_hex.hex()
                vout = getattr(inp, "output_n", None)
                if isinstance(vout, bytes):
                    vout = int.from_bytes(vout, 'little')
                utxo = UTXO.objects.filter(txid=txid_hex, vout=vout).first()
                if utxo:
                    TransactionInput.objects.create(
                        transaction=transaction,
                        utxo=utxo,
                        amount=Decimal(inp.value) / Decimal("1e8")
                    )
                    utxo.spent = True
                    utxo.save()

            # Outputs
            for out in tx.outputs:
                TransactionOutput.objects.create(
                    transaction=transaction,
                    address=out.address,
                    amount=Decimal(out.value) / Decimal("1e8")
                )

            print(f"🧾 TX HEX : {tx.raw_hex()}")

            # Diffusion sur Testnet
            service = Service(network="testnet")
            try:
                broadcast_result = service.sendrawtransaction(tx.raw_hex())
                print(f"✅ Diffusée avec succès : {broadcast_result}" if broadcast_result else "⚠️ Broadcast échoué")
            except Exception as be:
                print(f"⚠️ Échec du broadcast : {be}")

            # Synchronisation des UTXO et solde
            sync_wallet(wallet)
            updated_balance = wallet.onchain_balance()
            print(f"💰 Nouveau solde onchain : {updated_balance} BTC")

            # Attente de confirmation (optionnel)
            confirmations = 0
            waited = 0
            max_wait_time = 180
            while confirmations == 0 and waited < max_wait_time:
                try:
                    tx_info = service.gettransaction(tx.txid)
                    if isinstance(tx_info, dict):
                        confirmations = tx_info.get("confirmations", 0)
                        print(f"⛓️ Confirmations : {confirmations}")
                except Exception as e:
                    print(f"⏱️ En attente... ({e})")
                time.sleep(10)
                waited += 10

            if confirmations > 0:
                transaction.status = "confirmed"
                transaction.save()
                print(f"🎉 Transaction confirmée avec {confirmations} confirmations !")
            else:
                print("⚠️ Aucune confirmation reçue dans le délai imparti.")

            return Response({
                "transaction": TransactionSerializer(transaction).data,
                "updated_balance": updated_balance
            }, status=201)

        except Exception as e:
            print(f"❌ Erreur : {e}")
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
