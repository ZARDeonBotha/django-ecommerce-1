from django import forms
from .models import Review, Product, Store

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']  # Remove 'store'

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name']
