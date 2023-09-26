from django.urls import path
from django.views.decorators.cache import cache_page

from django.urls import path

from mailing.views import CreateMessage, DetailMessage, ListMessages, UpdateMessage, DeleteMessage, DeleteSendingView, \
    ListSending, CreateSending, DetailSending, UpdateSendingView, DisableSendingView, LogView, manual_sending

app_name = 'mailing'

urlpatterns = [
    path('create_message/', CreateMessage.as_view(), name='create_message'),
    path('detail_message/<int:pk>/', DetailMessage.as_view(), name='detail_message'),
    path('list_message/', ListMessages.as_view(), name='list_message'),
    path('update_message/<int:pk>/', UpdateMessage.as_view(), name='update_message'),
    path('delete_message/<int:pk>/', DeleteMessage.as_view(), name='delete_message'),

    path('delete_sending/<int:pk>/', DeleteSendingView.as_view(), name='delete_sending'),
    path('list_sending/', ListSending.as_view(), name='list_sending'),
    path('create_sending/', CreateSending.as_view(), name='create_sending'),
    path('update_sending/<int:pk>/', UpdateSendingView.as_view(), name='update_sending'),
    path('disable_sending/<int:pk>/', DisableSendingView.as_view(), name='disable_sending'),
    path('log/', LogView.as_view(), name='log'),
    path('sending<int:pk>/send', manual_sending, name="manual_sending"),
]