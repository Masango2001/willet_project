# willet_project/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuration Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Willet Project API",
        default_version='v1',
        description="Documentation de l'API Mini Wallet : utilisateurs, wallets, transactions",
        terms_of_service="http://127.0.0.1:8000/api/",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/wallets/', include('apps.wallets.urls')),
    path('api/transactions/', include('apps.transactions.urls')),

    # Routes Swagger / ReDoc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', 
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
