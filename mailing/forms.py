from builtins import *

from django import forms

from customer.models import Customer
from mailing.models import Message, Sending


class MessageForm(forms.ModelForm):
    subject = forms.CharField(max_length=50, min_length=4, required=True, help_text='Required: First Name',
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control', 'placeholder': 'Тема'}))
    content = forms.CharField(max_length=200, min_length=4, required=True,
                              widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Контент'}))

    class Meta:
        model = Message
        fields = ('subject', 'content')


class CreateSendingForm(forms.ModelForm):
    class Meta:
        model = Sending
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.all()
        self.fields['message'].queryset = Message.objects.filter(
            user=self.request)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class DisableSendingForm(forms.ModelForm):

    class Meta:
        model = Sending
        fields = ('status_sending',)


class UpdateSendingForm(forms.ModelForm):

    class Meta:
        model = Sending
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UpdateSendingForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['readonly'] = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'