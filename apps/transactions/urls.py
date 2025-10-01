from django.urls import path
from .views import TransactionListCreateView, TransactionRetrieveView

urlpatterns = [
    # Liste toutes les transactions ou création d'une nouvelle
    path('', TransactionListCreateView.as_view(), name='transaction-list-create'),

    # Récupérer une transaction précise par son ID
    path('<int:pk>/', TransactionRetrieveView.as_view(), name='transaction-detail'),
]
