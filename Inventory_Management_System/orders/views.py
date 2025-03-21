from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, FormView, DetailView
from django.urls import reverse_lazy
from django.db.models import F
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm
from inventory.models import Product
from accounts.models import User


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/create_order.html'
    success_url = reverse_lazy('orders:order_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class OrderItemCreateView(FormView):
    template_name = 'orders/create_order.html'
    form_class = OrderItemForm

    def form_valid(self, form):
        order_item = form.save(commit=False)
        order_item.order = get_object_or_404(Order, id=self.kwargs['order_id'])
        order_item.save()
        return redirect('orders:order_detail', pk=order_item.order.id)




class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self.object.order_items.all()
        return context


class OrderUpdateView(UpdateView):
    model = OrderItem
    form_class = OrderItemForm
    template_name = 'orders/create_order.html'
    
    
    def get_success_url(self):
        return reverse_lazy('orders:order_detail', kwargs={'pk': self.object.order.id})


class OrderApproveView(UpdateView):
    model = Order
    fields = [] 
    template_name = 'orders/order_detail.html'

    def post(self, request):
        order = self.get_object()
        if request.user.role == 'manager' and order.status == 'Pending':
            order.order_items.update(product__quantity=F('product__quantity') - F('quantity'))
            order.update(status='Approved', approved_by=request.user)

        return redirect('orders:order_list')


class OrderDeleteView(DeleteView):
    model = Order
    template_name = "orders/confirm.html"
    success_url = reverse_lazy("orders:order_list")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ordername"] = self.object.supermarket_name if self.object else ''
        return context


@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, supermarket_name_id):
    order = get_object_or_404(Order, supermarket_name_id=supermarket_name_id)
    order_items = order.order_items.all()
    return render(request, 'orders/order_details.html', {'order': order, 'order_items': order_items})


@login_required
def approve_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user.role == 'manager' and order.status == 'Pending':
        order.status = 'Approved'
        order.approved_by = request.user
        order.save()
        
        for item in order.order_items.all():
            product = item.product
            product.quantity = F('quantity') - item.quantity
            product.save()

    return redirect('orders:order_list')
