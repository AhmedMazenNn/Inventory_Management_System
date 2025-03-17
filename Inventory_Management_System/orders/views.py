from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm
from accounts.models import User
from inventory.models import Product

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
            order = order_form.save(commit=False)
            order.created_by = request.user
            order.save()
            
            for key, value in request.POST.items():
                if key.startswith('product_'):
                    product_id = key.split('_')[1]
                    quantity = value
                    product = Product.objects.get(id=product_id)
                    OrderItem.objects.create(order=order, product=product, quantity=quantity)

            return redirect('orders/order_detail', order_id=order.id)
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
            return redirect('order_detail', order_id=order.id)
    else:
        item_form = OrderItemForm()
    return render(request, 'orders/add_order_item.html', {'item_form': item_form, 'order': order})

@login_required
def approve_order(request, order_id):
    if request.user.is_manager:
        order = get_object_or_404(Order, id=order_id)
        order.status = 'Approved'
        order.approved_by = request.user
        order.save()
    return redirect('order_detail', order_id=order.id)