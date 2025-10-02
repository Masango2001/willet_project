from decimal import Decimal
from bitcoinlib.wallets import Wallet as BTCWallet
from apps.wallets.models import UTXO, Wallet

def sync_wallet(wallet: Wallet):
    """
    Synchronise un wallet Django avec le réseau Bitcoin via bitcoinlib.
    """
    btc_wallet = BTCWallet(wallet.name)
    btc_wallet.utxos_update()

    synced_utxos = []
    for utxo in btc_wallet.utxos():
        obj, _ = UTXO.objects.update_or_create(
            wallet=wallet,
            txid=utxo["txid"],
            vout=utxo["output_n"],
            defaults={
                "amount": Decimal(utxo["value"]) / Decimal("1e8"),
                "confirmations": utxo.get("confirmations", 0),
                "script_pub_key": utxo.get("script_hex", ""),
                "spent": utxo.get("spent", False),
            },
        )
        synced_utxos.append(obj)

    # Marquer les adresses utilisées
    for addr in wallet.addresses.all():
        if any(u for u in synced_utxos if u.script_pub_key and addr.address in u.script_pub_key):
            addr.used = True
            addr.save()

    return synced_utxos