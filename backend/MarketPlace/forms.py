from django import forms
from .models import MarketPlace, Product

class MarketPlaceForm(forms.ModelForm):
    class Meta:
        model = MarketPlace
        fields = ['email', 'password', 'role']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'marketplace']
