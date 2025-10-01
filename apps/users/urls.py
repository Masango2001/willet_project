from django.urls import path
from .views import (
    CustomerUserCreateView,
    CustomerUserListView,
    CustomerUserRetrieveUpdateDestroyView,
    LoginView,
)

urlpatterns = [
    path('create/', CustomerUserCreateView.as_view(), name='customer-create'),  # ✅ juste create/
    path('', CustomerUserListView.as_view(), name='customer-list'),             # liste : GET api/users/
    path('<int:pk>/', CustomerUserRetrieveUpdateDestroyView.as_view(), name='customer-detail'),
    path('login/', LoginView.as_view(), name='login'),
]
