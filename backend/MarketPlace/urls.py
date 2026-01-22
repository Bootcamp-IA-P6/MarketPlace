from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .models import Product

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
    
]
