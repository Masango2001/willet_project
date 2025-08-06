from django.urls import path
from .views import RegisterView, LoginView, UserProfileView

app_name = 'users'  # Permet le reverse avec namespace : 'users:register', etc.

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),  # JWT requis
]
