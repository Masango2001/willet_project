from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/users/', include('apps.users.urls')),
    path('api/wallet/', include('apps.wallet.urls')),
]