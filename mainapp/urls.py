from django.urls import path

from .views import *

urlpatterns = [
    path('', MainPageVies.as_view()),
    path('login/', LoginPageVies.as_view()),
    path('doc_site/', DocSitePageVies.as_view()),
    path('contacts/', ContactsPageVies.as_view()),
    path('news/', NewsPageVies.as_view()),
    path('courses_list/', CoursesListPageVies.as_view())
]