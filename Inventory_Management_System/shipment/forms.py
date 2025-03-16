from django import forms
from django.forms import inlineformset_factory
from .models import Shipment, ShipmentItem


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['factory_name', 'status']
        widgets = {
            'status': forms.Select(choices=Shipment.STATUS_CHOICES)
        }

class ShipmentItemForm(forms.ModelForm):
    class Meta:
        model = ShipmentItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(),
        }

ShipmentItemFormSet = inlineformset_factory(
    Shipment, ShipmentItem, 
    form=ShipmentItemForm, 
    extra=3, 
    can_delete=True 
)