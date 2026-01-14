from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.product_list, name='product_list'),
    path('acquire/<int:product_id>/', views.acquire_product, name='acquire_product'),
    path('profile/', views.user_profile, name='user_profile'),
]
