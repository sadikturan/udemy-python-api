from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, TokenVerifySerializer
from .serializer import SignUpSerializer, LoginSerializer
from .tokens import get_tokens_for_user
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

@extend_schema(
    request=TokenObtainPairSerializer,
    responses=TokenObtainPairSerializer,
    tags=['Users']
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema(
    request=TokenRefreshSerializer,
    responses=TokenObtainPairSerializer,
    tags=['Users']
)
class CustomTokenRefreshView(TokenRefreshView):
    pass

@extend_schema(
    request=TokenVerifySerializer,
    responses=None,
    tags=['Users']
)
class CustomTokenVerifyView(TokenVerifyView):
    pass

@extend_schema(
    summary="Kullanıcı oluştur",
    tags=['Users']
)
class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

@extend_schema(
    request=LoginSerializer,
    summary="Uygulamaya giriş",
    tags=['Users']
)
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = get_tokens_for_user(user)
            logger.info(f"User logged in:{user.username} (id={user.id})")

            response = {
                "message": "Login successfull",
                "token": tokens
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message":"Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
