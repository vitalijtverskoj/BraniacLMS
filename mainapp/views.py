import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.core.cache import cache
from django.http import FileResponse, JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from mainapp import forms as mainapp_forms
from mainapp import models as mainapp_models
from mainapp import tasks as mainapp_tasks
from django.views import View
# from datetime import datetime


logger = logging.getLogger(__name__)


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsPageView(TemplateView):
    template_name = "mainapp/news.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['news'] = mainapp_models.News.objects.all()[:5]
        return context


# class NewsPageDetailView(TemplateView):
#     template_name = "mainapp/news_detail.html"
#
#     def get_context_data(self, pk=None,**kwargs):
#         context = super().get_context_data(pk=pk, **kwargs)
#         context["news_object"] = get_object_or_404(News, pk=pk)
#         return context


class LoginPageView(TemplateView):
    template_name = "mainapp/../authapp/templates/authapp/login.html"


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"

    def get_context_data(self, **kwargs):
        context = super(ContactsPageView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["form"] = mainapp_forms.MailFeedbackForm(
                user=self.request.user
            )
        return context

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            cache_lock_flag = cache.get(
                f"mail_feedback_lock_{self.request.user.pk}"
            )
            if not cache_lock_flag:
                cache.set(
                    f"mail_feedback_lock_{self.request.user.pk}",
                    "lock",
                    timeout=300,
                )
                messages.add_message(
                    self.request, messages.INFO, _("Message sended")
                )
                mainapp_tasks.send_feedback_mail.delay(
                    {
                        "user_id": self.request.POST.get("user_id"),
                        "message": self.request.POST.get("message"),
                    }
                )
            else:
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    _("You can send only one message per 5 minutes"),
                )
        return HttpResponseRedirect(reverse_lazy("mainapp:contacts"))


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class CoursesListPageView(TemplateView):
    template_name = "mainapp/courses_list.html"

    def get_context_data(self, **kwargs):
        context = super(CoursesListPageView, self).get_context_data(**kwargs)
        context["objects"] = mainapp_models.Course.objects.all()[:7]
        return context


# class CoursesDetailView(TemplateView):
#     template_name = "mainapp/courses_detail.html"
#
#     def get_context_data(self, pk=None, **kwargs):
#         context = super(CoursesDetailView, self).get_context_data(**kwargs)
#         context["course_object"] = get_object_or_404(mod.Course, pk=pk)
#         context["lessons"] = mod.Lesson.objects.filter(course=context["course_object"])
#         context["teachers"] = mod.CourseTeachers.objects.filter(course=context["course_object"])
#         return context


class NewsWithPaginatorView(NewsPageView):

    def get_context_data(self, page, **kwargs):
        context = super().get_context_data(page=page, **kwargs)
        context['page_num'] = page
        return context


class LogView(UserPassesTestMixin, TemplateView):
    template_name = 'mainapp/logs.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        log_lines = []
        with open(settings.BASE_DIR / 'log/main_log.log') as log_file:
            for i, line in enumerate(log_file):
                if i == 1000:
                    break
                log_lines.insert(0, line)
            context_data['logs'] = log_lines
        return context_data


class LogDownloadView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, "rb"))
