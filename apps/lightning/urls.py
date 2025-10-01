from django.urls import path
from .views import LightningInvoiceCreate, LightningPayInvoice, LightningInvoiceStatus

urlpatterns = [
    path('invoice/create/', LightningInvoiceCreate.as_view(), name='invoice-create'),
    path('invoice/pay/', LightningPayInvoice.as_view(), name='invoice-pay'),
    path('invoice/status/', LightningInvoiceStatus.as_view(), name='invoice-status'),
]
