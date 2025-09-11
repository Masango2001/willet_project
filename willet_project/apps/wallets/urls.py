from django.urls import path
from .views import WalletListCreateView, WalletRetrieveUpdateDestroyView, WalletUTXOListView

urlpatterns = [
    path('wallets/', WalletListCreateView.as_view(), name='wallet-list-create'),  # Lister et créer des portefeuilles
    path('wallets/<int:pk>/', WalletRetrieveUpdateDestroyView.as_view(), name='wallet-retrieve-update-destroy'),  # Récupérer, mettre à jour ou supprimer un portefeuille
    path('wallets/<int:wallet_id>/utxos/', WalletUTXOListView.as_view(), name='wallet-utxo-list'),  # Lister les UTXOs d'un portefeuille spécifique
]