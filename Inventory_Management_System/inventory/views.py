from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from orders.models import Order
from django.db.models import Count, F
from .forms import ProductForm
from django.urls import reverse_lazy
from django.contrib import messages
import pandas as pd 
import plotly.express as px
import plotly.offline as pyo
from accounts.models import User

def search_product(request):
    query = request.GET.get("query")
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)
    return render(request,"inventory/inventory.html",context={"products":products,"query":query})

def home_page(request):
    return render(request,"inventory/inventory.html")

class List_all_products(LoginRequiredMixin,ListView):
    model = Product
    template_name = 'inventory/inventory.html'
    context_object_name = 'products'


class Update_product(LoginRequiredMixin,UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/add_product.html'
    success_url = reverse_lazy('inventory')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Update Product"
        context["btn_name"] = "Update_product"
        return context

class create_product(LoginRequiredMixin,CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/add_product.html'
    success_url = reverse_lazy('inventory')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Add Product"
        context["btn_name"] = "Add_product"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Product created successfully!")
        return response

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].widget.attrs.update({'autofocus': 'autofocus'})
        return form

class Dashboard(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, "accounts/dashboard.html")
    def post(self, request, query_name):
        if query_name == 'product':
            products = Product.objects.values("name", "quantity")
            df = pd.DataFrame(list(products))
            fig = px.bar(df, y="quantity", x="name", title="Product Quantity", text="quantity")
            fig.update_layout(paper_bgcolor="yellow", plot_bgcolor="yellow")
            image = pyo.plot(fig, output_type="div")
            return render(request, "accounts/dashboard.html", {"img": image })
        elif query_name == 'shipment':
            pass
        elif query_name == 'order':
            result = Order.objects.values('supermarket_name').annotate(appearance_count=Count('supermarket_name')).order_by('-appearance_count')
            df = pd.DataFrame(list(result))
            print(df)
            fig = px.bar(df, y='appearance_count', x='supermarket_name', title='Supermarket Orders')
            fig.update_layout(paper_bgcolor="yellow", plot_bgcolor="yellow")
            image = pyo.plot(fig, output_type="div")
            return render(request, "accounts/dashboard.html", {"img": image })
        else:
            pass
        return render(request, "accounts/dashboard.html")

def approved_info(request):
    orders = Order.objects.select_related("approved_by").values(
        approved_by_name=F("approved_by__username"), superMarket_name=F("supermarket_name")
    )
    return render(request, "accounts/dashboard.html", {"orders": orders})
