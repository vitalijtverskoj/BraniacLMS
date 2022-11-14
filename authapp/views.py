import os.path

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView

from authapp import forms

from authapp.models import CustomUser
from authapp.forms import CustomUserCreationForm, CustomUserChangeForm


class CustomLoginView(LoginView):
    def form_valid(self, form):
        ret = super().form_valid(form)
        message = _("Login success!<br>Hi, %(username)s") % {
            "username": self.request.user.get_full_name()
            if self.request.user.get_full_name()
            else self.request.user.get_username()
        }
        messages.add_message(self.request, messages.INFO, mark_safe(message))
        return ret

    def form_invalid(self, form):
        for _unused, msg in form.error_messages.items():
            messages.add_message(
                self.request,
                messages.WARNING,
                mark_safe(f"Something goes worng:<br>{msg}"),
            )
        return self.render_to_response(self.get_context_data(form=form))


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, _("See you later!"))
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    model = get_user_model()
    # model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("mainapp:main")


# class RegisterView(TemplateView):
#     template_name = 'authapp/register.html'
#
#     def post (self, request, *args, **kwargs):
#         try:
#             if all(
#                 (
#                     request.POST.get('username'),
#                     request.POST.get('email'),
#                     request.POST.get('password1'),
#                     request.POST.get('password1')
#                     == request.POST.get('password2'),
#
#                 )
#             ):
#                 new_user = authapp.models.User.objects.create(
#                     username=request.POST.get('username'),
#                     first_name=request.POST.get('first_name'),
#                     last_name=request.POST.get('last_name'),
#                     age=request.POST.get('age')
#                     if request.POST.get('age')
#                     else 0,
#                     avatar=request.FILES.get('avatar'),
#                     email=request.POST.get('email')
#                 )
#                 new_user.set_password(request.POST.get('password1'))
#                 new_user.save()
#                 messages.add_message(request, messages.INFO, 'Регистрация прошла успешно')
#                 return HttpResponseRedirect(reverse('authapp:login'))
#         except Exception as exp:
#             messages.add_message(
#                 request,
#                 messages.WARNING,
#                 f'Что-то пошло не так {exp}',
#             )
#             return HttpResponseRedirect(reverse('authapp:register'))


class ProfileEditView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserChangeForm

    def test_func(self):
        return True if self.request.user.pk == self.kwargs.get("pk") else False

    def get_success_url(self):
        return reverse_lazy("authapp:profile_edit", args=[self.request.user.pk])

# class EditView(LoginRequiredMixin, TemplateView):
#     template_name = 'authapp/edit.html'
#     login_url = 'authapp:login'
#
#     def post(self, request, *args, **kwargs):
#         try:
#             if request.POST.get('username'):
#                 request.user.username = request.POST.get('username')
#             if request.POST.get('first_name'):
#                 request.user.first_name = request.POST.get('first_name')
#             if request.POST.get('last_name'):
#                 request.user.last_name = request.POST.get('last_name')
#             if request.POST.get('age'):
#                 request.user.age = request.POST.get('age')
#             if request.POST.get('email'):
#                 request.user.email = request.POST.get('email')
#             if request.FILES.get('avatar'):
#                 if request.user.avatar and os.path.exists(request.user.avatar.path):
#                     os.remove(request.user.avatar.path)
#                 request.user.avatar = request.FILES.get('avatar')
#             request.user.save()
#             messages.add_message(request, messages.INFO, 'Изменения сохранены')
#         except Exception as exp:
#             messages.add_message(
#                 request,
#                 messages.WARNING,
#                 f'Что-то пошло не так {exp}',
#             )
#             return HttpResponseRedirect(reverse('authapp:edit'))
