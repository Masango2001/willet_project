from django.urls import path
from .views import (
    WalletCreate,
    WalletDetail,
    WalletBalance,
    GenerateNewAddressView,
    SyncUTXOView,
)

urlpatterns = [
    path('create/', WalletCreate.as_view(), name='wallet-create'),
    path('detail/', WalletDetail.as_view(), name='wallet-detail'),
    path('balance/', WalletBalance.as_view(), name='wallet-balance'),
    path('new-address/', GenerateNewAddressView.as_view(), name='wallet-new-address'),
    path('sync-utxo/', SyncUTXOView.as_view(), name='sync-utxo'),
]
