from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Route pour l'interface d'administration Django

    # API Users (utilisateurs)
    path('api/users/', include('apps.users.urls')),  # Inclut les URLs pour la gestion des utilisateurs

    # API Wallets
    path('api/wallets/', include('apps.wallets.urls')),  # Inclut les URLs pour la gestion des portefeuilles

    # API Transactions
    path('api/transactions/', include('apps.transactions.urls')),  # Inclut les URLs pour la gestion des transactions
]