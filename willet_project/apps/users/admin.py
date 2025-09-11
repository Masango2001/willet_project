from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomerUser

class CustomerUserAdmin(UserAdmin):
    model = CustomerUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'crypto_address', 'is_staff', 'is_active', 'created_at', 'updated_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'crypto_address')
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)

admin.site.register(CustomerUser, CustomerUserAdmin)