from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('change-password/', views.ChangePassword.as_view(), name='change_password'),
    path('update/', views.UserUpdateView.as_view(), name='user_update'),
]
