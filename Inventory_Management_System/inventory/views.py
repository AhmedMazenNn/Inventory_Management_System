from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from .forms import ProductForm
from django.urls import reverse_lazy
from django.contrib import messages


#in home page
def search_product(request):
    query = request.GET.get("query")
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)
    return render(request,"inventory/home.html",context={"products":products,"query":query})



def home_page(request):
    return render(request,"inventory/home.html")

class List_all_products(ListView):
    model = Product
    template_name = 'inventory/home.html'
    context_object_name = 'products'


class Update_product(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/add_product.html'
    success_url = reverse_lazy('home')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Update Product"
        context["btn_name"] = "Update_product"
        return context

class create_product(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/add_product.html'
    success_url = reverse_lazy('home')
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

    



#in add_order page
class Create_order():
    pass
#in add_shipment page
class Create_shipment():
    pass
#in add_order page
class Update_order():
    pass
#in add_shipment page
class Update_shipment():
    pass
#in orders page
class Get_all_orders():
    pass
#in shipments page
class Get_all_shipments():
    pass
#in details page
class Order_detalis():
    pass
class Shipment_detalis():
    pass
# in sinup page
class Create_user():
    pass
#in manager page
class Approve_order():
    pass
class Approve_shipment():
    pass
#in marked_products page
class Show_marked_products():
    pass

class Filter():
    pass
# Create your views here.

