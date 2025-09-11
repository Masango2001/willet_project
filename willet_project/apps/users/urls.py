from django.urls import path
from .views import CustomerUserListCreateView, CustomerUserRetrieveUpdateDestroyView, LoginView

urlpatterns = [
    path('users/', CustomerUserListCreateView.as_view(), name='user-list-create'),  # Inscription
    path('users/<int:pk>/', CustomerUserRetrieveUpdateDestroyView.as_view(), name='user-detail'),  # Détails de l'utilisateur
    path('login/', LoginView.as_view(), name='login'),  # Connexion
]