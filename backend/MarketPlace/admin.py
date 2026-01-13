from django.contrib import admin
from .models import MarketPlace

@admin.register(MarketPlace)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'password', 'role')
    search_fields = ('user', 'email', 'role')
    list_filter = ('role',)