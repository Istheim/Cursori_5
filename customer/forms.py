from builtins import *

from django import forms
from django.contrib.auth.forms import UserChangeForm

from customer.models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'comment')

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)

        for filed_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UpdateCustomerForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'comment')

    def __init__(self, *args, **kwargs):
        super(UpdateCustomerForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True

        for filed_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'