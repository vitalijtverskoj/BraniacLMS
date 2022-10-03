from django.urls import path

from .views import *
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path("", MainPageVies.as_view(), name='main'),
    path("login/", LoginPageVies.as_view(), name='login'),
    path("doc_site/", DocSitePageVies.as_view(), name='docs'),
    path("contacts/", ContactsPageVies.as_view(), name='contacts'),
    path("news/", NewsPageVies.as_view(), name='news'),
    path("courses_list/", CoursesListPageVies.as_view(), name='courses'),
]
