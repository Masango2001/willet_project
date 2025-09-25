# willet_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('api/users/', include('apps.users.urls')),  
    path('api/wallets/', include('apps.wallets.urls')),  
    path('api/transactions/', include('apps.transactions.urls')),  
]
