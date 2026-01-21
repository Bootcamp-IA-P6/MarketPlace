from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views

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
]

# URLs para preview de errores (solo en desarrollo)
if settings.DEBUG:
    urlpatterns += [
        path('preview/404/', views.preview_404, name='preview_404'),
        path('preview/500/', views.preview_500, name='preview_500'),
        path('preview/403/', views.preview_403, name='preview_403'),
        path('preview/400/', views.preview_400, name='preview_400'),
    ]
