from django.contrib import admin
from .models import Wallet, UTXO

class UTXOInline(admin.TabularInline):
    model = UTXO
    extra = 0  # Nombre d'UTXOs vides à afficher

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'public_key', 'balance')
    search_fields = ('user__username', 'public_key')
    inlines = [UTXOInline]  # Inclut les UTXOs associés à un portefeuille

@admin.register(UTXO)
class UTXOAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'txid', 'output_index', 'amount', 'spent')
    search_fields = ('txid', 'wallet__user__username')
    list_filter = ('spent',)