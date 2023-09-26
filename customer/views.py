from builtins import *

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from customer.forms import CustomerForm, UpdateCustomerForm
from customer.models import Customer
from customer.services import get_customers

from users.models import User


class CustomerCreate(CreateView):
    model = Customer
    template_name = 'customer/create_customer.html'
    form_class = CustomerForm
    success_url = reverse_lazy('customer:list_customers')
    extra_context = {
        'title': 'Создание клиента'
    }

    def form_valid(self, form):
        form = CustomerForm(data=self.request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.creator = self.get_object()
            customer.save()
            return super().form_valid(form)

    def get_object(self, queryset=None):
        creator = User.objects.get(pk=self.request.user.pk)
        return creator


class ListCustomers(ListView):
    model = Customer
    template_name = 'customer/list_customers.html'
    extra_context = {
        'title': 'Список клиентов'
    }

    def get_queryset(self):
        if self.request.user.has_perm('customer.can_view_customer'):
            return get_customers()
        else:
            return Customer.objects.filter(creator=self.request.user)


class DetailCustomer(DetailView):
    model = Customer
    template_name = 'customer/detail.html'
    extra_context = {
        'title': 'Информация о клиенте'
    }

    def get_object(self, queryset=None):
        return Customer.objects.get(id=self.kwargs['pk'])


class UpdateCustomer(UpdateView):
    model = Customer
    template_name = 'customer/update_customer.html'
    form_class = UpdateCustomerForm
    extra_context = {
        'title': 'Обновление информации о клиенте'
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def form_valid(self, form):
        super().form_valid(form)
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('customer:detail_customer', kwargs={'pk': self.kwargs['pk']})


class DeleteCustomerView(DeleteView):
    model = Customer
    success_url = reverse_lazy('customer:list_customers')
