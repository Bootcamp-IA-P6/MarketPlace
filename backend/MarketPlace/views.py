from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, UserProfile

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/products.html', {'products': products})

@login_required
def acquire_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile.products.add(product)
    return redirect('user_profile')

@login_required
def user_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'users/profile.html', {'products': profile.products.all()})
