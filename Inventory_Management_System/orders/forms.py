from django import forms
from .models import Order, OrderItem
from inventory.models import Product
import re

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['supermarket_name']
        widgets = {
            'supermarket_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        supermarket_name = cleaned_data.get('supermarket_name')
        if not supermarket_name:
            self.add_error('supermarket_name', 'This field is required.')
        if not re.match(r'^[A-Za-z\s]+$', supermarket_name):
            self.add_error("supermarket_name", "Supermarket name must contain only letters and spaces.")

        return cleaned_data


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(quantity__gt=0)
        self.fields['product'].choices = [(product.id, product.name) for product in self.fields['product'].queryset]

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get("quantity")
        if quantity is not None and quantity < 1:
            self.add_error("quantity", "Quantity must be at least 1")
        return cleaned_data
