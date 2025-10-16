from django.urls import path
from .views import SignUpView, LoginView, CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView

urlpatterns = [
    path('signup', SignUpView.as_view(), name="signup"),
    path('login', LoginView.as_view(), name="login"),
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', CustomTokenVerifyView.as_view(), name='token_verify'),
]
