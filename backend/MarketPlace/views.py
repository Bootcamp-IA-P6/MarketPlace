from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Favorite, Order, UserProfile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Location
import uuid
from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def main_page(request):
    products = Product.objects.filter(is_sold=False)
    return render(request, 'main.html', {'products': products})

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
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def acquire_product(request, product_id):
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
    except ValidationError as e:
        return render(request, "error.html", {"message": str(e)})

    product.is_sold = True
    product.save()

    return render(request, "successful.html", {"product": product})





@login_required
def user_profile(request):
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
    return redirect('user_profile')


from .models import Location

@login_required
def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity') or 1

        location_id = request.POST.get('location')
        location_obj = Location.objects.get(id=location_id)

        image_file = request.FILES.get('image')
        image = ""

        if image_file:
            try:
                file_ext = image_file.name.split('.')[-1]
                file_name = f"{uuid.uuid4()}.{file_ext}"
                file_content = image_file.read()
                supabase.storage.from_("products_images").upload(
                    path=f"public/{file_name}",
                    file=file_content,
                    file_options={"content-type": image_file.content_type}
                )
                image = supabase.storage.from_("products_images").get_public_url(f"public/{file_name}")
                print("FILES:", request.FILES) 
                print("IMAGE:", image)
            except Exception as e:
                print(f"Error: {e}")

        Product.objects.create(
            seller=request.user.profile,
            name=name,
            description=description,
            price=float(price),
            quantity=int(quantity),
            location=location_obj,
            image=image,
            is_sold=False,
        )

        return redirect('user_profile')

    locations = Location.objects.all()
    return render(request, 'create_product.html', {'locations': locations} )



@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


