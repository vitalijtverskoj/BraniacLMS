from authapp.apps import AuthappConfig
from django.urls import path
from authapp.views import CustomLoginView, RegisterView, CustomLogoutView, ProfileEditView

app_name = AuthappConfig.name

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile_edit/<int:pk>/', ProfileEditView.as_view(), name='profile_edit'),
]