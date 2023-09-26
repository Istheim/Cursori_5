from django.core.cache import cache

from config.settings import CACHE_ENABLED
from .models import Customer


def get_customers():
    if CACHE_ENABLED:
        key = f'customers_list'
        customers_list = cache.get(key)
        if customers_list is None:
            customers_list = Customer.objects.all()
            cache.set(customers_list, customers_list)
    else:
        customers_list = Customer.objects.all()

    return customers_list