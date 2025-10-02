# apps/transactions/urls.py
from django.urls import path
from .views import SendTransactionView, WalletSyncView

urlpatterns = [
    path("send/", SendTransactionView.as_view(), name="send_transaction"),
    path("sync/", WalletSyncView.as_view(), name="wallet_sync"),
]
