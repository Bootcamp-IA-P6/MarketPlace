from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, require_GET
from .models import Product, UserProfile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout




import logging # Adding by Mar
logger = logging.getLogger(__name__)


def main_page(request):
    products = Product.objects.filter(bought_by__isnull=True)
    return render(request, 'main.html', {'products': products})

def login_view(request):  # Modify by Mar
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                logger.info(f"User {username} logged in successfully")  # <--- LOGGING
                return redirect('main_page')
            else:
                logger.warning(f"Failed login attempt for username: {username}")  # <--- LOGGING
        else:
            logger.warning("Invalid login form submitted")  # <--- LOGGING
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


@require_GET
def logout_view(request): # Adding by Mar
    logout(request)
    return redirect("/login/")


@login_required
def acquire_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.seller == request.user:
        return redirect('main_page')
    profile = request.user.userprofile
    profile.products.add(product)
    product.bought_by.add(request.user.userprofile)
    product.save()
    return redirect('user_profile')


@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    purchased_products = profile.products.all()
    selling_products = request.user.products_venda.all()
    
    context = {
        'profile': profile,
        'purchased_products': purchased_products,
        'selling_products': selling_products,
    }
    return render(request, 'users/profile.html', context)


@login_required
def upgrade_to_seller(request):
    profile = request.user.userprofile
    profile.is_premium = True
    profile.save()
    return redirect('user_profile')

@login_required
def create_product(request):
    if not request.user.userprofile.is_premium:
        return redirect('user_profile')
    
    if request.method == 'POST':
        Product.objects.create(
            seller=request.user,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            price=request.POST.get('price')
        )
        return redirect('main_page')
    return render(request, 'products/create_product.html')
