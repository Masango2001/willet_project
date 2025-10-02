# apps/wallets/admin.py
from django.contrib import admin
from .models import Wallet, Address, UTXO

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'user', 'current_address', 'private_key', 
        'onchain_balance', 'lightning_balance', 'total_balance', 
        'is_default', 'created_at', 'updated_at'
    )
    readonly_fields = (
        'onchain_balance', 'total_balance', 'get_unused_address', 
        'created_at', 'updated_at'
    )
    search_fields = ('name', 'user__email', 'current_address')
    list_filter = ('is_default', 'created_at', 'updated_at')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet', 'address', 'index', 'used', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('address', 'wallet__name')
    list_filter = ('used', 'created_at')


@admin.register(UTXO)
class UTXOAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'txid', 'vout', 'wallet', 'amount', 
        'confirmations', 'spent', 'script_pub_key', 'created_at'
    )
    readonly_fields = ('created_at',)
    search_fields = ('txid', 'wallet__name')
    list_filter = ('spent', 'confirmations', 'created_at')
