from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('product/buy/<int:product_id>/', views.acquire_product, name='acquire_product'),
    path('product/new/', views.create_product, name='create_product'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/upgrade/', views.upgrade_to_seller, name='upgrade_to_seller'),
    path('admin/', admin.site.urls),

    path("accounts/", include("accounts.urls")),

    path('admin/', admin.site.urls),



  ]
