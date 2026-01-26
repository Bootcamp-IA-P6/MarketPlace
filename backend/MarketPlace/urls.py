from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views
from .models import Product
from django.conf import settings
from django.conf.urls.static import static

# Configuración de manejadores de error personalizados
handler400 = 'MarketPlace.error_views.handler400'
handler403 = 'MarketPlace.error_views.handler403'  
handler404 = 'MarketPlace.error_views.handler404'
handler500 = 'MarketPlace.error_views.handler500'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('product/buy/<int:product_id>/', views.acquire_product, name='acquire_product'),
    path('product/new/', views.create_product, name='create_product'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/upgrade/', views.upgrade_to_seller, name='upgrade_to_seller'),
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main_page'), name='logout'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('register/', views.register_view, name='register'),
    path('create-checkout-session/<int:product_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('create-upgrade-session/', views.create_upgrade_session, name='create_upgrade_session'),
    path('upgrade-success/', views.upgrade_success, name='upgrade_success'),
    path('successful/<int:product_id>/', views.successful, name='successful'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('favorites/', views.favorites, name='favorites'),
    path('toggle-favorites/<int:product_id>/', views.toggle_favorites, name='toggle_favorites'),
    path('shopping-cart/', views.shopping_cart, name='shopping_cart'),
    path('toggle-shopping-cart/<int:product_id>/', views.toggle_shopping_cart, name='toggle_shopping_cart'),
    path("multi-success/", views.multi_success, name="multi_success"),
    path("create-multi-checkout/", views.create_multi_checkout, name="create_multi_checkout"),

    
]

# URLs para preview de errores (solo en desarrollo)
if settings.DEBUG:
    urlpatterns += [
        path('preview/404/', views.preview_404, name='preview_404'),
        path('preview/500/', views.preview_500, name='preview_500'),
        path('preview/403/', views.preview_403, name='preview_403'),
        path('preview/400/', views.preview_400, name='preview_400'),
    ]
