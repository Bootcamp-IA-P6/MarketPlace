from django.shortcuts import render, get_object_or_404, redirect
from .models import MarketPlace
from .forms import MarketPlaceForm

def lista_marketplaces(request):
    marketplaces = MarketPlace.objects.all()
    return render(request, 'marketplaces/lista_marketplaces.html', {'marketplaces': marketplaces})

def detalle_marketplace(request, marketplace_id):
    marketplace = get_object_or_404(MarketPlace, pk=marketplace_id)
    return render(request, 'marketplaces/detalle_marketplace.html', {'marketplace': marketplace})

def crear_marketplace(request):
    if request.method == 'POST':
        form = MarketPlaceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_marketplaces')
    else:
        form = MarketPlaceForm()
    return render(request, 'marketplaces/crear_marketplace.html', {'form': form})

def editar_marketplace(request, marketplace_id):
    marketplace = get_object_or_404(MarketPlace, pk=marketplace_id)
    if request.method == 'POST':
        form = MarketPlaceForm(request.POST, instance=marketplace)
        if form.is_valid():
            form.save()
            return redirect('detalle_marketplace', marketplace_id=marketplace.id)
    else:
        form = MarketPlaceForm(instance=marketplace)
    return render(request, 'marketplaces/editar_marketplace.html', {'form': form, 'marketplace': marketplace})

def eliminar_marketplace(request, marketplace_id):
    marketplace = get_object_or_404(MarketPlace, pk=marketplace_id)
    if request.method == 'POST':
        marketplace.delete()
        return redirect('lista_marketplaces')
    return render(request, 'marketplaces/eliminar_marketplace.html', {'marketplace': marketplace})