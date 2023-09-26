from builtins import *
from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect

# Create your views here.
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from mailing.forms import MessageForm, DisableSendingForm, CreateSendingForm, UpdateSendingForm
from mailing.models import Message, Sending, Log


class CreateMessage(CreateView):
    model = Message
    template_name = 'mailing/create_message.html'
    success_url = 'mailing:list_message'
    form_class = MessageForm
    extra_context = {
        'title': 'Создание письма'
    }

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        form.user = self.request.user
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            return HttpResponseRedirect(reverse(self.success_url))
        return render(request, self.template_name)


class ListMessages(ListView):
    model = Message
    template_name = 'mailing/list_message.html'
    extra_context = {
        'title': 'Список писем'
    }


class DetailMessage(DetailView):
    model = Message
    template_name = 'mailing/detail_message.html'
    extra_context = {
        'title': 'Информация о письме'
    }

    def get_object(self, queryset=None):
        message = get_object_or_404(Message, pk=self.kwargs['pk'])
        return message


class UpdateMessage(PermissionRequiredMixin, UpdateView):
    permission_required = 'mailing.change_message'
    model = Message
    template_name = 'mailing/update_message.html'
    form_class = MessageForm
    extra_context = {
        'title': 'Обновление информации о письме'
    }

    def form_valid(self, form):
        super().form_valid(form)
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('mailing:detail_message', kwargs={'pk': self.kwargs['pk']})


class DeleteMessage(DeleteView):
    model = Message
    extra_context = {
        'title': 'Удаление письма'
    }

    def get_success_url(self):
        return reverse_lazy('mailing:list_sending')


class ListSending(ListView):
    model = Sending
    template_name = 'mailing/list_sending.html'
    extra_context = {
        'title': 'Список рассылок'
    }

    def get_queryset(self):

        if not self.request.user.has_perm('mailing.can_view_sending'):
            return Sending.objects.filter(user=self.request.user)
        else:
            return Sending.objects.all()


class DisableSendingView(PermissionRequiredMixin, UpdateView):
    permission_required = 'mailing.can_disable_sending'
    model = Sending
    form_class = DisableSendingForm
    success_url = reverse_lazy('mailing:list_sending')
    template_name = 'mailing/disable.html'

    def post(self, request, *args, **kwargs):
        if self.request.method == 'POST':
            sending_object = Sending.objects.get(id=kwargs['pk'])
            sending_object.status_sending = Sending.COMPLETED
            sending_object.save()
            return HttpResponseRedirect(reverse('mailing:list_sending'))


class CreateSending(CreateView):
    model = Sending
    template_name = 'mailing/create_sending.html'
    form_class = CreateSendingForm
    success_url = reverse_lazy('mailing:list_sending')
    extra_context = {
        'title': 'Создание рассылки'
    }

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request.user})
        return kwargs


class UpdateSendingView(PermissionRequiredMixin, UpdateView):
    permission_required = 'mailing.change_sending'
    model = Sending
    template_name = 'mailing/update_sending.html'
    form_class = UpdateSendingForm
    extra_context = {
        'title': 'Обновление информации о рассылке'
    }

    def form_valid(self, form):
        if self.request.method == 'POST':
            form = UpdateSendingForm(data=self.request.POST, instance=self.request.user)
            if form.is_valid():
                form.instance = self.object
                form.updated_at = timezone.now()
                form.save()
        else:
            form = UpdateSendingForm(instance=self.request.user)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mailing:list_sending')


class DetailSending(PermissionRequiredMixin, DetailView):
    permission_required = 'mailing.can_view_sending'
    model = Sending
    template_name = 'mailing/detail_sending.html'
    extra_context = {
        'title': 'Информация о рассылке'
    }

    def get_object(self, queryset=None):
        sending = Sending.objects.get(pk=self.kwargs['pk'])
        return sending


class DeleteSendingView(DeleteView):
    model = Sending
    extra_context = {
        'title': 'Удаление рассылки'
    }

    def get_success_url(self):
        return reverse_lazy('mailing:list_sending')


class LogView(ListView):
    model = Log
    template_name = 'mailing/log.html'
    extra_context = {
        'title': 'Статистика по рассылкам'
    }

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = Log.objects.all()
        else:
            queryset = Log.objects.filter(sending__user=user)

        return queryset


def manual_sending(request, pk):
    mailing = get_object_or_404(Sending, pk=pk)
    email_list = [x.email for x in mailing.customer.all()]
    try:
        result = send_mail(
            subject=mailing.message.subject,
            message=mailing.message.content,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email_list,
            fail_silently=False
        )
        if result:
            Log.objects.create(sending=mailing,
                               last_attempt=datetime.now(),
                               status_attempt='success',
                               answer_server='200')
            mailing.status_sending = Sending.COMPLETED
            mailing.save()
    except Exception as error:
        Log.objects.create(sending=mailing,
                           last_attempt=datetime.now(),
                           status_attempt='failure',
                           answer_server=str(error))
    return redirect('sending:list_sending')