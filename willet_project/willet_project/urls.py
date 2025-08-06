from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls', namespace='users')),     # si `app_name = 'users'`
    path('api/wallet/', include('apps.wallet.urls', namespace='wallet')),  # ici aussi
]
