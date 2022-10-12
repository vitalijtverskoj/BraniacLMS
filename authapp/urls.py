from authapp.apps import AuthappConfig
from django.urls import path
from authapp.views import LoginView, RegisterView, LogoutView, EditView

app_name = AuthappConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('login/', RegisterView.as_view(), name='login'),
    path('login/', LogoutView.as_view(), name='login'),
    path('login/', EditView.as_view(), name='login'),
]