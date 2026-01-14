from django.contrib import admin
from .models import MarketPlace, Product

@admin.register(MarketPlace)
class MarketPlaceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'password', 'role')
    search_fields = ('user', 'email', 'role')
    list_filter = ('role',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'get_user_name')
    search_fields = ('name', 'description', 'marketplace__user')
    list_filter = ('marketplace',)

    def get_user_name(self, obj):
        return obj.marketplace.user
    
    get_user_name.short_description = 'Seller'

