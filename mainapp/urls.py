from django.urls import path
from django.views.decorators.cache import cache_page

from mainapp import views
from mainapp.apps import MainappConfig



app_name = MainappConfig.name

urlpatterns = [
    path("", views.MainPageView.as_view(), name='main_page'),
    path("login/", views.LoginPageView.as_view(), name='login'),
    path("contacts/", views.ContactsPageView.as_view(), name='contacts'),
    path("doc_site/", views.DocSitePageView.as_view(), name='doc_site'),

    # Courses
    path("courses_list/", cache_page(3600)(views.CoursesListView.as_view()), name='courses'),
    path("courses_list/<int:pk>/", views.CoursesDetailView.as_view(), name='courses_detail'),

    # News
    path("news/", views.NewsListView.as_view(), name='news'),
    path("news/create/", views.NewsCreateView.as_view(), name="news_create"),
    path("news/<int:pk>/detail", views.NewsDetailView.as_view(), name="news_detail"),
    path("news/<int:pk>/update", views.NewsUpdateView.as_view(), name="news_update"),
    path("news/<int:pk>/delete", views.NewsDeleteView.as_view(), name="news_delete"),


    # Logs
    path('logs/', views.LogView.as_view(), name='logs_list'),
    path('logs/download/', views.LogDownloadView.as_view(), name='logs_download'),
]
