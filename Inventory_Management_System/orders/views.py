from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, FormView
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm
from accounts.models import User
from inventory.models import Product

# ----- CLASS-BASED VIEWS -----

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/create_order.html'
    success_url = reverse_lazy('orders:order_list')
    login_url = 'login'  # Redirect to login if not authenticated
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Add Order"
        context["btn_name"] = "Add Order"
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UpdateView):  # Update for status now    
    model = Order
    form_class = OrderForm
    template_name = 'orders/update_order.html'
    success_url = reverse_lazy('orders:order_list')
    login_url = 'login'
    redirect_field_name = 'next'


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    login_url = 'login'
    redirect_field_name = 'next'


class OrderDeleteView(LoginRequiredMixin, DeleteView): 
    model = Order
    template_name = "orders/confirm.html"
    success_url = reverse_lazy("orders:create_order")
    login_url = 'login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ordername"] = self.object.supermarket_name if self.object else ''
        return context


class OrderItemCreateView(LoginRequiredMixin, FormView):
    template_name = 'orders/create_order.html'
    form_class = OrderItemForm
    login_url = 'login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Add Item"
        context["btn_name"] = "Add"
        return context

    def form_valid(self, form):
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        order_item = form.save(commit=False)
        order_item.order = order
        order_item.save()
        return redirect('orders:order_list')

# ----- FUNCTION-BASED VIEWS -----

@login_required(login_url='login')
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required(login_url='login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.order_items.all()
    return render(request, 'orders/order_detail.html', {'order': order, 'order_items': order_items})


@login_required(login_url='login')
def add_order_item(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        item_form = OrderItemForm(request.POST)
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.order = order
            item.save()
            return redirect('orders:order_list', order_id=order.id)
    else:
        item_form = OrderItemForm()
    return render(request, 'orders/add_order_item.html', {'item_form': item_form, 'order': order})


@login_required(login_url='login')
def approve_order(request, order_id):
    if request.user.role == 'manager':
        order = get_object_or_404(Order, id=order_id)
        order.status = 'Approved'
        order.approved_by = request.user
        order.save()
    return redirect('orders:order_list', order_id=order.id)
