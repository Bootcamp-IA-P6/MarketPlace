import logging 
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Favorite, Order, UserProfile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.contrib import messages


logger = logging.getLogger(__name__)

def main_page(request):
    products = Product.objects.filter(is_sold=False)
    
    
    logger.info(f"Main page loaded. Displaying {products.count()} products.")
    
    return render(request, 'main.html', {'products': products})

def login_view(request):
   
    logger.debug(f"Accessing login view. Method: {request.method}")

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
               
                logger.info(f"User logged in successfully: {username}")
                return redirect('main_page')
            else:
               
                logger.warning(f"Failed login attempt (Invalid credentials) for user: {username}")
                form = AuthenticationForm()
        else:
             
             logger.warning("Failed login attempt: Invalid form data provided.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def acquire_product(request, product_id):
    
    logger.info(f"Transaction started: User {request.user.username} attempting to buy Product ID {product_id}")

    product = get_object_or_404(Product, id=product_id)
    profile = request.user.profile

    try:
        Order.objects.create(
            buyer=profile,
            seller=product.seller,
            product=product,
            quantity=1,
            total_price=product.price,
        )
        
        logger.info(f"Order created successfully for Product ID {product_id}")

    except ValidationError as e:
        
        logger.warning(f"Transaction failed validation for Product ID {product_id}: {str(e)}")
        return render(request, "error.html", {"message": str(e)})

    product.is_sold = True
    product.save()

    
    logger.info(f"Product ID {product_id} marked as SOLD.")

    return render(request, "successful.html", {"product": product})

@login_required
def user_profile(request):
    
    logger.debug(f"Rendering profile page for user: {request.user.username}")

    profile = request.user.profile
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

@login_required
def upgrade_to_seller(request):
    profile = request.user.profile
    profile.is_premium = True
    profile.save()

    
    logger.info(f"User upgraded to SELLER status: {request.user.username}")

    return redirect('user_profile')

@login_required
def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity') or 1
        image = request.POST.get('image')

        
        logger.info(f"User {request.user.username} creating product: {name}")

        Product.objects.create(
            seller=request.user.profile,
            name=name,
            description=description,
            price=price,
            quantity=int(quantity),
            image=image
        )
        
       
        logger.info(f"Product created successfully: {name}")

        return redirect('user_profile')

    return render(request, 'create_product.html')