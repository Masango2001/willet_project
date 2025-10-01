# apps/wallets/urls.py
from django.urls import path
from .views import WalletCreate, WalletDetail, WalletBalance

urlpatterns = [
    path('create/', WalletCreate.as_view(), name='wallet-create'),
    path('detail/', WalletDetail.as_view(), name='wallet-detail'),
    path('balance/', WalletBalance.as_view(), name='wallet-balance'),
]
