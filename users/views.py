from builtins import *

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm, UserBlockedForm
from users.models import User
from users.services import get_users, generate_code


class RegisterUser(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    extra_context = {
        'title': 'Регистрация'
    }

    def get_success_url(self):
        return reverse('users:confirm_code', kwargs={'email': self.object.email})

    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save(commit=False)
            code = generate_code()
            new_user.verify_code = code
            new_user.save()
            send_mail(
                subject='Вы зарегистрировались',
                message=code,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[new_user.email]
            )

        return super().form_valid(form)


def confirm_code(request, email):
    error_message = None

    if request.method == 'POST':
        verify_code = request.POST.get('verify_code')
        user = User.objects.get(email=email)
        if user.verify_code == verify_code:
            user.is_active = True
            user.save()
            return redirect(reverse('users:login'))
        else:
            error_message = 'Неверный код!'

    context = {'title': 'Подтверждение почты', 'error_message': error_message}

    return render(request, 'users/confirm_code.html', context)


class DeleteUserView(DeleteView):
    model = User
    success_url = reverse_lazy('users:login')


class ListUsersView(ListView):
    model = User
    template_name = 'users/list_users.html'
    extra_context = {
        'title': 'Список пользователей сервиса'
    }

    def get_queryset(self):
        return get_users()


class ProfileUser(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    extra_context = {
        'title': 'Профиль'
    }

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
        return redirect(self.success_url)

    def get_object(self, queryset=None):
        return User.objects.get(id=self.request.user.pk)

    def form_valid(self, form):
        messages.set_level(self.request, messages.SUCCESS)
        messages.error(self.request, 'Данные изменены')
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class BlockUser(PermissionRequiredMixin, UpdateView):
    permission_required = 'user.can_block_user'
    model = User
    form_class = UserBlockedForm
    template_name = 'users/block_user.html'
    extra_context = {
        'title': 'Блокировка пользователя'
    }

    def post(self, request, *args, **kwargs):
        if self.request.method == 'POST':
            user_object = User.objects.get(id=kwargs['pk'])
            user_object.is_active = False
            user_object.save()
            return HttpResponseRedirect(reverse('users:list_users'))


class BlockUser(PermissionRequiredMixin, UpdateView):
    permission_required = 'user.can_block_user'
    model = User
    form_class = UserBlockedForm
    template_name = 'users/block_user.html'
    extra_context = {
        'title': 'Блокировка пользователя'
    }

    def post(self, request, *args, **kwargs):
        if self.request.method == 'POST':
            user_object = User.objects.get(id=kwargs['pk'])
            user_object.is_active = False
            user_object.save()
            return HttpResponseRedirect(reverse('users:list_users'))
