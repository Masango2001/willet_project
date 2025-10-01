from lndgrpc import LNDClient
from django.utils import timezone
from apps.wallets.models import Wallet
from .models import LightningInvoice, LightningPayment

# Connexion au node LND (Testnet)
lnd = LNDClient(
    lnd_dir="/home/user/.lnd",   # Chemin vers ton node LND
    network="testnet"
)

# --- Créer une invoice ---
def create_invoice(wallet: Wallet, amount_sats: int, memo: str = "") -> LightningInvoice:
    response = lnd.add_invoice(value=amount_sats, memo=memo)
    invoice = LightningInvoice.objects.create(
        wallet=wallet,
        invoice=response.payment_request,
        amount_sats=amount_sats,
        paid=False
    )
    return invoice

# --- Payer une invoice ---
def pay_invoice(wallet: Wallet, invoice_str: str) -> LightningPayment:
    # Envoie la payment via LND
    response = lnd.send_payment(invoice_str)
    # On suppose que l'amount correspond à la valeur de l'invoice
    amount_sats = response.payment_route.total_amt if response.payment_route else 0
    # Récupération ou création de l'objet LightningInvoice
    ln_invoice, _ = LightningInvoice.objects.get_or_create(invoice=invoice_str, defaults={'wallet': wallet, 'amount_sats': amount_sats})
    # Crée la transaction
    payment = LightningPayment.objects.create(
        wallet=wallet,
        invoice=ln_invoice,
        amount_sats=amount_sats,
        status='confirmed' if response.status.name=='SUCCEEDED' else 'failed'
    )
    # Met à jour le solde Lightning du wallet
    if payment.status == 'confirmed':
        wallet.lightning_balance += amount_sats / 1e8  # convert sats → BTC si tu gardes Decimal
        wallet.save(update_fields=['lightning_balance'])
        ln_invoice.paid = True
        ln_invoice.paid_at = timezone.now()
        ln_invoice.save(update_fields=['paid','paid_at'])
    return payment

# --- Vérifier le statut d'une invoice ---
def check_invoice_status(invoice: LightningInvoice) -> LightningInvoice:
    inv = lnd.lookup_invoice(r_hash_str=invoice.invoice)
    if inv.settled:
        invoice.paid = True
        invoice.paid_at = timezone.now()
        invoice.save(update_fields=['paid','paid_at'])
        # Met à jour le wallet balance si ce n'était pas fait
        wallet = invoice.wallet
        wallet.lightning_balance += invoice.amount_sats / 1e8
        wallet.save(update_fields=['lightning_balance'])
    return invoice
