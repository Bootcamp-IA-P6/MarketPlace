"""
URL configuration for MarketPlace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
# from .forms import MarketPlaceForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.lista_marketplaces, name='lista_marketplaces'),
    path('detail_marketplace/<int:marketplace_id>/', views.detalle_marketplace, name='detail_marketplace'),
    path('create_marketplace/', views.crear_marketplace, name='create_marketplace'),
    path('edit_marketplace/<int:marketplace_id>/', views.editar_marketplace, name='edit_marketplace'),
    path('delete_marketplace/<int:marketplace_id>/', views.eliminar_marketplace, name='delete_marketplace'),
]
