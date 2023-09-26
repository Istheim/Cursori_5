from django.urls import path
from django.views.decorators.cache import cache_page

from customer.views import CustomerCreate, ListCustomers, DetailCustomer, UpdateCustomer, DeleteCustomerView

app_name = 'customer'

urlpatterns = [
    path('create_customer/', CustomerCreate.as_view(), name='create_customer'),
    path('list_customers/', ListCustomers.as_view(), name='list_customers'),
    path('detail_customer/<int:pk>/', cache_page(60)(DetailCustomer.as_view()), name='detail_customer'),
    path('update_customer/<int:pk>/', UpdateCustomer.as_view(), name='update_customer'),
    path('delete_customer/<int:pk>/', DeleteCustomerView.as_view(), name='delete_customer'),
]