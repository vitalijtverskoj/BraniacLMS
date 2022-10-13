import os.path

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
import authapp.models


class CustomLoginView(LoginView):
    template_name = 'authapp/login.html'


class RegisterView(TemplateView):
    template_name = 'authapp/register.html'

    def post (self, request, *args, **kwargs):
        try:
            if all(
                (
                    request.POST.get('username'),
                    request.POST.get('email'),
                    request.POST.get('password1'),
                    request.POST.get('password1')
                    == request.POST.get('password2'),

                )
            ):
                new_user = authapp.models.User.objects.create(
                    username=request.POST.get('username'),
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    age=request.POST.get('age')
                    if request.POST.get('age')
                    else 0,
                    avatar=request.FILES.get('avatar'),
                    email=request.POST.get('email')
                )
                new_user.set_password(request.POST.get('password1'))
                new_user.save()
                messages.add_message(request, messages.INFO, 'Регистрация прошла успешно')
                return HttpResponseRedirect(reverse('authapp:login'))
        except Exception as exp:
            messages.add_message(
                request,
                messages.WARNING,
                f'Что-то пошло не так {exp}',
            )
            return HttpResponseRedirect(reverse('authapp:register'))


class CustomLogoutView(LogoutView):
    pass


class EditView(LoginRequiredMixin, TemplateView):
    template_name = 'authapp/edit.html'
    login_url = 'authapp:login'

    def post(self, request, *args, **kwargs):
        try:
            if request.POST.get('username'):
                request.user.username = request.POST.get('username')
            if request.POST.get('first_name'):
                request.user.first_name = request.POST.get('first_name')
            if request.POST.get('last_name'):
                request.user.last_name = request.POST.get('last_name')
            if request.POST.get('age'):
                request.user.age = request.POST.get('age')
            if request.POST.get('email'):
                request.user.email = request.POST.get('email')
            if request.FILES.get('avatar'):
                if request.user.avatar and os.path.exists(request.user.avatar.path):
                    os.remove(request.user.avatar.path)
                request.user.avatar = request.FILES.get('avatar')
            request.user.save()
            messages.add_message(request, messages.INFO, 'Изменения сохранены')
        except Exception as exp:
            messages.add_message(
                request,
                messages.WARNING,
                f'Что-то пошло не так {exp}',
            )
            return HttpResponseRedirect(reverse('authapp:edit'))

