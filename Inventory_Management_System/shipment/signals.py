from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import Shipment
from inventory.models import Product

@receiver(pre_save, sender=Shipment)
def update_inventory_on_delivery(sender, instance, **kwargs):
    """ Signal to update inventory when a shipment is delivered. """

    # Fetch the previous instance from the database
    try:
        previous_instance = Shipment.objects.get(id=instance.id)
    except Shipment.DoesNotExist:
        previous_instance = None

    # Check if the status is changing to "Delivered"
    if previous_instance and previous_instance.status != "Delivered" and instance.status == "Delivered":
        for item in instance.shipment_items.all():
            product_name = item.product.name  # Get product name
            
            # Check if product already exists in inventory
            product, created = Product.objects.get_or_create(
                name__iexact=product_name,
                defaults={'quantity': 0}  # Default quantity if new
            )

            # Update quantity if product exists
            product.quantity += item.quantity  # Increase quantity from shipment
            product.save()
