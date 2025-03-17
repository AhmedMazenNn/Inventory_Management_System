from pyexpat.errors import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm
from accounts.models import User
from inventory.models import Product
import json

@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.order_items.all() 
    return render(request, 'orders/order_detail.html', {'order': order, 'order_items': order_items})

@login_required
def create_order(request):
    products = Product.objects.filter(quantity__gt=0)  
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
       
        if order_form.is_valid():
            # Save the order
            order = order_form.save(commit=False)
            order.created_by = request.user
            order.save()

            # Process order items
            order_items_json = request.POST.get('order_items')
            if order_items_json:
                order_items = json.loads(order_items_json)
                for item in order_items:
                    product_id = item['product_id']
                    quantity = item['quantity']
                    product = get_object_or_404(Product, id=product_id)

                    # Check if the quantity will result in stock going below the critical quantity
                    if product.quantity - quantity < product.critical_quantity:
                        # Handle the error (e.g., show a message or roll back the order)
                        order.delete()  # Delete the order if the condition is not met
                        messages.error(request, f"Cannot add {product.name}. The remaining stock will go below the critical quantity.")
                        return redirect('orders:create_order')

                    # Create the order item
                    OrderItem.objects.create(order=order, product=product, quantity=quantity)

                    # Update the product's quantity
                    product.quantity -= quantity
                    product.save()

            return redirect('orders:order_detail', order_id=order.id)
    else:
        order_form = OrderForm()
    return render(request, 'orders/create_order.html', {'order_form': order_form, 'products': products})

@login_required
def add_order_item(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        item_form = OrderItemForm(request.POST)
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.order = order
            item.save()
            return redirect('orders:order_detail', order_id=order.id)
    else:
        item_form = OrderItemForm()
    return render(request, 'orders/add_order_item.html', {'item_form': item_form, 'order': order})

@login_required
def approve_order(request, order_id):
    if request.user.role == 'manager':
        order = get_object_or_404(Order, id=order_id)
        order.status = 'Approved'
        order.approved_by = request.user
        order.save()
    return redirect('orders:order_detail', order_id=order.id)