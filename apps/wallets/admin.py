# apps/wallets/admin.py
from django.contrib import admin
from .models import Wallet, UTXO

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'current_address', 'private_key', 'onchain_balance', 'lightning_balance', 'is_default', 'created_at', 'updated_at')
    readonly_fields = ('onchain_balance', 'lightning_balance', 'created_at', 'updated_at')

@admin.register(UTXO)
class UTXOAdmin(admin.ModelAdmin):
    list_display = ('txid', 'vout', 'wallet', 'amount', 'confirmations', 'spent', 'created_at')
    readonly_fields = ('created_at',)
