from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import Http404

from .models import Product, Favorite, Order, UserProfile
from .error_handlers import (
    handle_exceptions, 
    require_premium, 
    handle_product_not_found, 
    handle_already_sold_product,
    handle_insufficient_permissions
)


@handle_exceptions()
def main_page(request):
    try:
        products = Product.objects.filter(is_sold=False)
        return render(request, 'main.html', {'products': products})
    except Exception as e:
        return render(request, 'error.html', {
            'error_code': 500,
            'message': 'Error al cargar los productos.',
            'detail': 'No se pudieron cargar los productos disponibles.'
        }, status=500)

@handle_exceptions()
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main_page')
            else:
                return render(request, 'error.html', {
                    'error_code': 401,
                    'message': 'Credenciales inválidas.',
                    'detail': 'Usuario o contraseña incorrectos.'
                }, status=401)
        else:
            return render(request, 'error.html', {
                'error_code': 400,
                'message': 'Datos de formulario inválidos.',
                'detail': 'Por favor, verifica los datos ingresados.'
            }, status=400)
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
@handle_exceptions()
def acquire_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return handle_product_not_found(request)
    
    # Verificar si el producto ya está vendido
    if product.is_sold:
        return handle_already_sold_product(request)
    
    # Verificar que el usuario no compre su propio producto
    if product.seller == request.user.profile:
        return render(request, 'error.html', {
            'error_code': 400,
            'message': 'No puedes comprar tu propio producto.',
            'detail': 'No está permitido comprar productos que tú mismo vendes.'
        }, status=400)
    
    # Verificar que el usuario tenga perfil
    if not hasattr(request.user, 'profile'):
        return render(request, 'error.html', {
            'error_code': 400,
            'message': 'Perfil de usuario no encontrado.',
            'detail': 'No se pudo encontrar tu perfil de usuario.'
        }, status=400)

    profile = request.user.profile

    try:
        Order.objects.create(
            buyer=profile,
            seller=product.seller,
            product=product,
            quantity=1,
            total_price=product.price,
        )
        
        product.is_sold = True
        product.save()
        
        return render(request, "successful.html", {"product": product})
        
    except ValidationError as e:
        return render(request, "error.html", {
            'error_code': 400,
            'message': 'Error en la validación de la orden.',
            'detail': str(e)
        }, status=400)





@login_required
@handle_exceptions()
def user_profile(request):
    # Verificar que el usuario tenga perfil
    if not hasattr(request.user, 'profile'):
        return render(request, 'error.html', {
            'error_code': 400,
            'message': 'Perfil de usuario no encontrado.',
            'detail': 'No se pudo encontrar tu perfil de usuario.'
        }, status=400)
    
    profile = request.user.profile
    
    try:
        purchased_products = Product.objects.filter(
            order__buyer=profile
        ).distinct()
        favorite_products = Favorite.objects.filter(
            user=profile
        ).select_related('product')
        selling_products = Product.objects.filter(
            seller=profile,
            is_sold=False
        )
        sold_products = Product.objects.filter(
            seller=profile,
            is_sold=True
        )
        
        return render(request, 'profile.html', {
            'profile': profile,
            'purchased_products': purchased_products,
            'favorite_products': [fav.product for fav in favorite_products],
            'selling_products': selling_products,
            'sold_products': sold_products,
        })
    except Exception as e:
        return render(request, 'error.html', {
            'error_code': 500,
            'message': 'Error al cargar el perfil.',
            'detail': 'No se pudo cargar la información del perfil.'
        }, status=500)




@login_required
@handle_exceptions()
def upgrade_to_seller(request):
    # Verificar que el usuario tenga perfil
    if not hasattr(request.user, 'profile'):
        return render(request, 'error.html', {
            'error_code': 400,
            'message': 'Perfil de usuario no encontrado.',
            'detail': 'No se pudo encontrar tu perfil de usuario.'
        }, status=400)
    
    profile = request.user.profile
    
    # Verificar si ya es premium
    if profile.is_premium:
        return render(request, 'error.html', {
            'error_code': 409,
            'message': 'Ya eres usuario premium.',
            'detail': 'Tu cuenta ya tiene privilegios de vendedor.'
        }, status=409)
    
    profile.is_premium = True
    profile.save()
    messages.success(request, '¡Felicidades! Ahora eres un vendedor premium.')
    return redirect('user_profile')


@login_required
@require_premium
@handle_exceptions()
def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity') or 1
        image = request.POST.get('image')

        # Validaciones básicas
        if not name or not description or not price:
            return render(request, 'error.html', {
                'error_code': 400,
                'message': 'Datos incompletos.',
                'detail': 'Nombre, descripción y precio son campos obligatorios.'
            }, status=400)
        
        try:
            price = float(price)
            quantity = int(quantity)
            
            if price <= 0:
                raise ValueError("El precio debe ser mayor a 0")
            if quantity <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")
                
        except ValueError as e:
            return render(request, 'error.html', {
                'error_code': 400,
                'message': 'Datos numéricos inválidos.',
                'detail': str(e)
            }, status=400)

        try:
            Product.objects.create(
                seller=request.user.profile,
                name=name,
                description=description,
                price=price,
                quantity=quantity,
                image=image
            )
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('user_profile')
            
        except Exception as e:
            return render(request, 'error.html', {
                'error_code': 500,
                'message': 'Error al crear el producto.',
                'detail': 'No se pudo crear el producto. Inténtalo de nuevo.'
            }, status=500)

    return render(request, 'create_product.html')


# Vistas para preview de páginas de error (solo para desarrollo)
def preview_404(request):
    """Vista para previsualizar la página 404 estética"""
    return render(request, '404.html', status=404)

def preview_500(request):
    """Vista para previsualizar la página 500 estética"""
    return render(request, '500.html', status=500)

def preview_403(request):
    """Vista para previsualizar la página 403 estética"""
    return render(request, '403.html', status=403)

def preview_400(request):
    """Vista para previsualizar la página 400 estética"""
    return render(request, '400.html', status=400)


