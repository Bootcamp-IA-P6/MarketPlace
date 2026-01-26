from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Favorite, Order, UserProfile, ShoppingCart
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Location
import uuid
from supabase import create_client
import os
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
import stripe
from .models import Product
from .models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import json


stripe.api_key = settings.STRIPE_SECRET_KEY

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def main_page(request):
    products = Product.objects.filter(is_available=True, is_sold=False)

    cart_products = []
    if request.user.is_authenticated:
        cart_products = list(
            request.user.profile.shopping_cart.values_list("product_id", flat=True)
        )

    return render(
        request,
        "main.html",
        {
            "products": products,
            "cart_products": cart_products,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
        }
    )


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
        return render(request, "error/error.html", {"message": str(e)})

    product.is_sold = True
    product.is_available = False
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
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
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




def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main_page")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


def create_checkout_session(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not product.is_available or product.is_sold:
        return JsonResponse({"error": "Product no longer available"}, status=400)

    if request.user.is_authenticated and product.seller == request.user.profile:
        return JsonResponse({"error": "You cannot buy your own product"}, status=400)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "unit_amount": int(product.price * 100),
                    "product_data": {"name": product.name},
                },
                "quantity": 1,
            }
        ],
        success_url=f"http://127.0.0.1:8000/successful/{product.id}",
        cancel_url="http://127.0.0.1:8000/profile",
    )

    return JsonResponse({"id": session.id})





def create_upgrade_session(request):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "unit_amount": 3000,
                    "product_data": {
                        "name": "Premium Seller Upgrade",
                    },
                },
                "quantity": 1,
            }
        ],
        metadata={
            "user_id": request.user.id,
        },
        success_url="http://127.0.0.1:8000/successful/",
        cancel_url="http://127.0.0.1:8000/profile",
    )

    return JsonResponse({"id": session.id})

@login_required
def successful(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    Order.objects.create(
        buyer=request.user.profile,
        seller=product.seller,
        product=product,
        quantity=1,
        total_price=product.price,
    )

    product.is_sold = True
    product.save()

    return render(request, "successful.html", {"product": product})


@login_required
def upgrade_success(request): 
    profile = UserProfile.objects.get(user=request.user)
    profile.is_premium = True 
    profile.save() 
    return render(request, "upgrade_success.html")


from django.conf import settings 
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not product.is_available or product.is_sold:
        return render(request, "product_unavailable.html")

    return render(request, "product_detail.html", {
        "product": product,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    })



@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.seller != request.user.profile:
        return render(request, "error/error.html", {"message": "You don't have permission to delete this product."})

    if product.image:
        try:
            file_path = product.image.split("/public/")[-1]
            supabase.storage.from_("products_images").remove([f"public/{file_path}"])
        except Exception as e:
            print("Error deleting image from Supabase:", e)


    product.delete()

    return redirect("user_profile")



@login_required
def toggle_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    profile = request.user.profile

    if profile.favorites.filter(id=product.id).exists():
        profile.favorites.remove(product)
        return JsonResponse({"success": True, "action": "removed"})
    else:
        profile.favorites.add(product)
        return JsonResponse({"success": True, "action": "added"})



@login_required
def favorites(request):
    profile = request.user.profile
    favorite_products = profile.favorites.filter(is_available=True)


    return render(request, "favorites.html", {"favorite_products": favorite_products})


@login_required
def shopping_cart(request):
    profile = request.user.profile
    shopping_cart_products = profile.shopping_cart.select_related("product").filter(
        product__is_available=True,
        product__is_sold=False
    )

    return render(
        request,
        "shopping_cart.html",
        {"shopping_cart_products": shopping_cart_products}
    )



@login_required
def toggle_shopping_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    profile = request.user.profile

    cart_item = ShoppingCart.objects.filter(
        user=profile,
        product=product
    ).first()

    if cart_item:
        cart_item.delete()
        return JsonResponse({"success": True, "action": "removed"})
    else:
        ShoppingCart.objects.create(
            user=profile,
            product=product
        )
        return JsonResponse({"success": True, "action": "added"})


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id) 

    cart_products = []
    if request.user.is_authenticated:
        cart_products = list(
            request.user.profile.shopping_cart.values_list("product_id", flat=True)
        )

    return render(request, "product_detail.html", {
        "product": product,
        "cart_products": cart_products,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
    })


@csrf_exempt
@login_required
def create_multi_checkout(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    data = json.loads(request.body)
    product_ids = data.get("products", [])

    line_items = []

    for pid in product_ids:
        product = Product.objects.get(id=pid)
        line_items.append({
            "price_data": {
                "currency": "eur",
                "product_data": {"name": product.name},
                "unit_amount": int(product.price * 100),
            },
            "quantity": 1,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url="http://127.0.0.1:8000/multi-success/",
        cancel_url="http://127.0.0.1:8000/shopping-cart/",
    )

    return JsonResponse({"checkout_url": session.url})



@login_required
def multi_success(request):
    return render(request, "multi_success.html")


# Vistas de preview para testing de errores (solo en desarrollo)
def preview_400(request):
    """Vista para preview del error 400"""
    return render(request, 'error/400.html', status=400)

def preview_403(request):
    """Vista para preview del error 403"""
    return render(request, 'error/403.html', status=403)

def preview_404(request):
    """Vista para preview del error 404"""
    return render(request, 'error/404.html', status=404)

def preview_500(request):
    """Vista para preview del error 500"""
    return render(request, 'error/500.html', status=500)


