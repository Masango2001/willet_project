from django.urls import path
from .views.balance import BalanceView
from .views.send import SendBitcoinView
from .views.history import TransactionHistoryView

app_name = "wallet"  # Facultatif mais utile pour les namespaces

urlpatterns = [
    path('balance/', BalanceView.as_view(), name='balance'),
    path('send/', SendBitcoinView.as_view(), name='send'),
    path('history/', TransactionHistoryView.as_view(), name='history'),
]
