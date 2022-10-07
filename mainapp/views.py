from django.views.generic import TemplateView
from datetime import datetime

class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsPageView(TemplateView):
    template_name = "mainapp/news.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['news_title'] = 'Новость'
        context['description'] = 'Предварительное описание новости'
        context['news_data'] = datetime.now()
        context['range'] = range(5)

        return context


class LoginPageView(TemplateView):
    template_name = "mainapp/login.html"


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class CoursesListPageView(TemplateView):
    template_name = "mainapp/courses_list.html"


class NewsWithPaginatorView(NewsPageView):

    def get_context_data(self, page, **kwargs):
        context = super().get_context_data(page=page, **kwargs)
        context['page_num'] = page
        return context