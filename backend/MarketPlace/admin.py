from django.contrib import admin
from .models import Product, UserProfile

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'get_seller_name')
    search_fields = ('name', 'description', 'seller__user__username')
    list_filter = ('seller__is_premium',)

    def get_seller_name(self, obj):
        return obj.seller.user.username
    
    get_seller_name.short_description = 'Seller'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_premium')
    list_filter = ['is_premium', 'location']
