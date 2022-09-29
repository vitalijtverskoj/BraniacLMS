from django.views.generic import TemplateView


class MainPageVies(TemplateView):
    template_name = "mainapp/index.html"


class NewsPageVies(TemplateView):
    template_name = "mainapp/news.html"


class LoginPageVies(TemplateView):
    template_name = "mainapp/login.html"


class ContactsPageVies(TemplateView):
    template_name = "mainapp/contacts.html"


class DocSitePageVies(TemplateView):
    template_name = "mainapp/doc_site.html"


class CoursesListPageVies(TemplateView):
    template_name = "mainapp/courses_list.html"
