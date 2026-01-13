from django import forms
from .models import MarketPlace

class MarketPlaceForm(forms.ModelForm):
    class Meta:
        model = MarketPlace
        fields = ['user', 'email', 'password', 'role']