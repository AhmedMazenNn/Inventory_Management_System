from django import forms
from .models import Order, OrderItem
from inventory.models import Product

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['supermarket_name']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(quantity__gt=0)  # Only show products in stock