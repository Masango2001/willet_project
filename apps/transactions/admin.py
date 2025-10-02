# apps/transactions/admin.py
from django.contrib import admin
from .models import Transaction, TransactionInput, TransactionOutput

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'wallet', 'txid', 'to_address', 'amount', 'fee', 'status', 'created_at', 'updated_at'
    )
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('txid', 'to_address', 'wallet__name', 'wallet__user__email')
    readonly_fields = ('txid', 'created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(TransactionInput)
class TransactionInputAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction', 'utxo', 'amount')
    search_fields = ('transaction__txid', 'utxo__txid')
    readonly_fields = ('amount',)
    ordering = ('-transaction__created_at',)

@admin.register(TransactionOutput)
class TransactionOutputAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction', 'address', 'amount')
    search_fields = ('transaction__txid', 'address')
    readonly_fields = ('amount',)
    ordering = ('-transaction__created_at',)
