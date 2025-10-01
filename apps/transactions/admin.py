from django.contrib import admin
from .models import Transaction, TransactionInput, TransactionOutput

class TransactionInputInline(admin.TabularInline):
    model = TransactionInput
    extra = 0  # Nombre d'inputs vides à afficher

class TransactionOutputInline(admin.TabularInline):
    model = TransactionOutput
    extra = 0  # Nombre d'outputs vides à afficher

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender_utxo', 'recipient_address', 'amount', 'status', 'timestamp')
    search_fields = ('recipient_address', 'status')
    list_filter = ('status',)
    inlines = [TransactionInputInline, TransactionOutputInline]  # Inclusion des inputs et outputs

@admin.register(TransactionInput)
class TransactionInputAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'utxo')
    search_fields = ('utxo__txid',)  # Recherche par txid du UTXO

@admin.register(TransactionOutput)
class TransactionOutputAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'address', 'amount')
    search_fields = ('address',)