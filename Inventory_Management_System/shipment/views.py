from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
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

    def dispatch(self, request, *args, **kwargs):
        shipment_id = self.kwargs.get("shipment_id")
        self.shipment = get_object_or_404(Shipment, id=shipment_id)
        if self.shipment.status in ["Delivered", "Approved"]:
            message.error(request, "You cannot add items to a delivered or approved shipment.")
            # return redirect("shipments:shipment_list")
            return redirect("shipments:shipment_detail",pk=self.shipment.id)
        return super().dispatch(request, *args, **kwargs)
    
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

class ShipmentUpdateView(UserPassesTestMixin,UpdateView):
    model = ShipmentItem
    form_class = ShipmentItemForm
    template_name = 'shipments/create_shipment.html'

    def test_func(self):
        return self.request.user.role == 'manager'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            message.error(self.request,"Only managers can update shipments.")
            return redirect("home")
        return super().handle_no_permission()

    def dispatch(self, request, *args, **kwargs):
        shipment_item = get_object_or_404(ShipmentItem, pk=self.kwargs.get('pk'))
        self.shipment = shipment_item.shipment
        if self.shipment.status in ["Delivered", "Approved"]:
            message.error(request, "You cannot Update items in a delivered or approved shipment.")
            return redirect("shipments:shipment_detail",pk=self.shipment.id)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Update Shipment Item"
        context["btn_name"] = "Update"
        return context
    
    def get_success_url(self):
        return reverse_lazy('shipments:shipment_detail', kwargs={'pk': self.object.shipment.id})

class ShipmentApproveView(UserPassesTestMixin,UpdateView):
    model = Shipment
    fields = []
    template_name = 'shipments/shipment_detail.html'

    def test_func(self):
        return self.request.user.role == 'manager'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            message.error(self.request,"Only managers can approve shipments.")
            return redirect("shipments:shipment_list")
        return super().handle_no_permission()
    
    def post(self, request, *args, **kwargs):
        shipment = get_object_or_404(Shipment, pk=self.kwargs.get('pk'))
        shipment_items = shipment.shipment_items.all()
        print(shipment_items)
        if shipment_items and request.user.role == "manager" and shipment.status == 'Pending':
            shipment.status = 'Approved'
            shipment.approved_by = request.user
            shipment.save()
            message.success(request, "Shipment approved successfully")
        else:
            message.error(request, "You cannot approve empty shipment.")
        return redirect('shipments:shipment_list')


class ShipmentDeliverView(UserPassesTestMixin,UpdateView):
    model = Shipment
    fields = []
    template_name = 'shipments/shipment_detail.html'

    def test_func(self):
        return self.request.user.role == 'manager'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            message.error(self.request,"Only managers can deliver shipments.")
            return redirect("shipments:shipment_list")
        return super().handle_no_permission()
    
    def post(self, request, *args, **kwargs):
        shipment = get_object_or_404(Shipment, pk=self.kwargs.get('pk'))
        if request.user.role == "manager" and shipment.status == 'Approved':
            shipment.status = 'Delivered'
            shipment.approved_by = request.user
            shipment.save()
            message.success(request, "Shipment Delivered successfully")
        else:
            message.error(request, "You cannot Delivered this shipment.")
        return redirect('shipments:shipment_list')




































































# from django.http import HttpResponseForbidden
# from django.shortcuts import get_object_or_404, render
# from .models import Shipment, ShipmentItem
# from .forms import ShipmentForm,ShipmentItemFormSet
# from django.shortcuts import redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages


# @login_required
# def list_shipment(request):
#     shipments = Shipment.objects.all()
#     return render(request, 'shipment/list_of_shipment.html', {
#         'shipments': shipments
#     })

# @login_required
# def shipment_detail(request, pk):
#     shipment = get_object_or_404(Shipment, pk=pk)
#     shipment_items = ShipmentItem.objects.filter(shipment=shipment)
#     return render(request, 'shipment/shipment_details.html', {
#         'shipment': shipment,
#         'shipment_items': shipment_items
#     })

# @login_required
# def create_shipment(request):
#     if request.method == 'POST':
#         shipment_form = ShipmentForm(request.POST)
#         formset = ShipmentItemFormSet(request.POST)
#         if shipment_form.is_valid() and formset.is_valid():
#             shipment = shipment_form.save(commit=False)
#             shipment.created_by = request.user
#             if request.user.role == "manager" and shipment.status == "Approved":
#                 shipment.approved_by = request.user
#             else:
#                 shipment.status = "Pending"
#                 shipment.approved_by = None
#             shipment.save()
#             shipment_items = formset.save(commit=False)
#             for item in shipment_items:
#                 item.shipment = shipment
#                 item.save()
#             messages.success(request, "Shipment created successfully.")
#             return redirect('shipment:shipment_list')
#     else:
#         shipment_form = ShipmentForm()
#         formset = ShipmentItemFormSet()
#     return render(request, 'shipment/create_shipment.html', {
#         'shipment_form': shipment_form,
#         'formset': formset
#     })


# @login_required
# def update_shipment(request, pk):
#     if request.user.role != "manager":
#         messages.warning(request, "You don't have permission to update.")
#         return redirect("shipment:shipment_list")
#     shipment = get_object_or_404(Shipment, pk=pk)
#     if shipment.status != "Delivered":
#         if request.method == 'POST':
#             shipment_form = ShipmentForm(request.POST, instance=shipment)
#             formset = ShipmentItemFormSet(request.POST, instance=shipment)
#             if shipment_form.is_valid() and formset.is_valid():
#                 shipment = shipment_form.save(commit=False)
#                 shipment.created_by = request.user
#                 if request.user.role == "manager" and shipment.status == "Approved":
#                     shipment.approved_by = request.user
#                 shipment.save()
#                 shipment_items = formset.save(commit=False)
#                 for item in shipment_items:
#                     item.shipment = shipment
#                     item.save()
#                 messages.success(request, "Shipment updated successfully.")  
#                 return redirect("shipment:shipment_list")
#         else:
#             shipment_form = ShipmentForm(instance=shipment)
#             formset = ShipmentItemFormSet(instance=shipment)
#     else:
#         messages.warning(request, "You can't update a deliverd shipment.")
#         return redirect("shipment:shipment_list")
#     return render(request, 'shipment/update_shipment.html', {
#         'shipment_form': shipment_form,
#         'formset': formset
#     })
