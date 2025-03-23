from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, FormView, DetailView
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib import messages as message
from .models import Shipment, ShipmentItem
from .forms import ShipmentForm, ShipmentItemForm
from inventory.models import Product

class ShipmentCreateView(CreateView):
    model = Shipment
    form_class = ShipmentForm
    template_name = 'shipments/create_shipment.html'
    success_url = reverse_lazy('shipments:shipment_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Add New Shipment"
        context["btn_name"] = "Add Shipment"
        return context
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        message.success(self.request, "Shipment created successfully.")
        return super().form_valid(form)
    
class ShipmentListView(ListView):
    model = Shipment
    template_name = 'shipments/shipment_list.html'
    context_object_name = 'shipments'

class ShipmentDeleteView(DeleteView):
    model = Shipment
    template_name = "shipments/confirm.html"
    success_url = reverse_lazy("shipments:shipment_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shipment_name"] = self.object.factory_name if self.object else ''
        return context

class ShipmentItemCreateView(FormView):
    template_name = 'shipments/create_shipment.html'  
    form_class = ShipmentItemForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Add New Shipment Item"
        context["btn_name"] = "Add Item"
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        shipment_id = self.kwargs.get("shipment_id")
        kwargs["shipment"] = get_object_or_404(Shipment, id=shipment_id)
        return kwargs
    
    def form_valid(self, form):
        shipment = self.get_form_kwargs()["shipment"]
        form.instance.shipment = shipment
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))   
    
    success_url = reverse_lazy("shipments:shipment_list")

class ShipmentDetailView(DetailView):
    model = Shipment
    template_name = 'shipments/shipment_detail.html'
    context_object_name = 'shipment'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shipment_items'] = self.object.shipment_items.all()
        return context

class ShipmentUpdateView(UpdateView):
    model = ShipmentItem
    form_class = ShipmentItemForm
    template_name = 'shipments/create_shipment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Update Shipment Item"
        context["btn_name"] = "Update"
        return context
    
    def get_success_url(self):
        return reverse_lazy('shipments:shipment_detail', kwargs={'pk': self.object.shipment.id})

class ShipmentApproveView(UpdateView):
    model = Shipment
    fields = []
    template_name = 'shipments/shipment_detail.html'
    
    def post(self, request, *args, **kwargs):
        shipment = get_object_or_404(Shipment, pk=self.kwargs.get('pk'))
        if request.user.role == "manager" and shipment.status == 'Pending':
            shipment.status = 'Approved'
            shipment.approved_by = request.user
            shipment.save()
            for shipment_item in shipment.shipment_items.all(): 
                product = shipment_item.product
                product.quantity += shipment_item.quantity 
                product.save()
            message.success(request, "Shipment approved successfully, and product quantities updated.")
        else:
            message.error(request, "You cannot approve this shipment.")
        return redirect('shipments:shipment_list')



