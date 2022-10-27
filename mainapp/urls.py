from django.urls import path
from django.views.decorators.cache import cache_page

from mainapp.apps import MainappConfig

from .views import *

app_name = MainappConfig.name

urlpatterns = [
    path("", MainPageView.as_view(), name='main'),
    path("login/", LoginPageView.as_view(), name='login'),
    path("contacts/", ContactsPageView.as_view(), name='contacts'),
    path("doc_site/", DocSitePageView.as_view(), name='docs'),

    # Courses
    path("courses_list/", cache_page(3600)(CoursesListPageView.as_view()), name='courses'),
    # path("courses_list/<int:pk>/", CoursesDetailView.as_view(), name='courses_detail'),


    # News
    path("news/", NewsPageView.as_view(), name='news'),
    path("news/<int:page>/", NewsWithPaginatorView.as_view(), name='news_paginator'),
    # path("news/<int:pk>/", NewsPageDetailView.as_view(), name="news_detail"),

    # Logs
    path('logs/', LogView.as_view(), name='logs_list'),
    path('logs/download/', LogDownloadView.as_view(), name='logs_download'),
]
