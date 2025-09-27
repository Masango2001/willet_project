from django.urls import path
from .views import WalletListCreateView, WalletRetrieveUpdateDestroyView, WalletUTXOListView

urlpatterns = [
    # Lister tous les wallets et créer un nouveau wallet Bitcoin
    path('', WalletListCreateView.as_view(), name='wallet-list-create'),

    # Récupérer, mettre à jour ou supprimer un wallet spécifique
    path('<int:pk>/', WalletRetrieveUpdateDestroyView.as_view(), name='wallet-retrieve-update-destroy'),

    # Lister les UTXOs d'un wallet spécifique
    path('utxos/', WalletUTXOListView.as_view(), name='wallet-utxo-list'),
]
