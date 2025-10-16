import logging
from . import serializers
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema_view, extend_schema

logger = logging.getLogger(__name__)

@extend_schema_view(
    post=extend_schema(
        summary="Kullanıcı Kaydı Oluştur",
        description="Yeni bir kullanıcı hesabı oluşturur.",
        request=serializers.RegisterSerializer,
        responses={
            201: serializers.RegisterSerializer,
            400: {"example": {"error": "Geçersiz veri girdiniz."}},
        },
        tags=["User"],
    )
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.RegisterSerializer

@extend_schema_view(
    post=extend_schema(
        summary="Kullanıcı Girişi",
        description=(
            "Kullanıcının kimlik bilgilerini doğrular ve JWT token’ları döner. "
            "Yanıt olarak `access` ve `refresh` token’larını, ayrıca kullanıcı bilgilerini içerir."
        ),
        request=serializers.LoginSerializer,
        responses={
            200: {
                "example": {
                    "id": 1,
                    "username": "ahmet",
                    "email": "ahmet@example.com",
                    "first_name": "Ahmet",
                    "last_name": "Turan",
                    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                }
            },
            400: {"example": {"error": "Kullanıcı adı veya şifre hatalı."}},
        },
        tags=["User"],
    )
)
class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = serializer.validated_data["refresh"]
        access = serializer.validated_data["access"]

        logger.info(f"User logged in: {user.username}")

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "refresh": refresh,
            "access": access
        }, status=status.HTTP_200_OK)

@extend_schema_view(
    put=extend_schema(
        summary="Şifre Değiştir",
        description="Kullanıcı mevcut şifresini doğrulayıp yeni bir şifre belirler.",
        request=serializers.ChangePasswordSerializer,
        responses={
            200: {"example": {"detail": "Şifre başarıyla değiştirildi."}},
            400: {"example": {"old_password": "Eski şifre yanlış"}},
        },
        tags=["User"],
    ),
    patch=extend_schema(
        summary="Şifre Değiştir (Kısmi)",
        description="Kullanıcının şifresini kısmi olarak değiştirir (PUT ile aynı işlev).",
        request=serializers.ChangePasswordSerializer,
        responses={
            200: {"example": {"detail": "Şifre başarıyla değiştirildi."}},
            400: {"example": {"old_password": "Eski şifre yanlış"}},
        },
        tags=["User"],
    ),
)
class ChangePassword(generics.UpdateAPIView):
    serializer_class= serializers.ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data["old_password"]):
                return Response({"old_password": "Eski şifre yanlış"}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data["new_password"])
            user.save()

            return Response({"detail":"Şifre başarıyla değiştirildi."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema_view(
    put=extend_schema(
        summary="Kullanıcı Bilgilerini Güncelle",
        description="Giriş yapmış kullanıcı kendi profil bilgilerini günceller.",
        request=serializers.UserUpdateSerializer,
        responses=serializers.RegisterSerializer,
        tags=["User"],
    ),
    patch=extend_schema(
        summary="Kullanıcı Bilgilerini Kısmi Güncelle",
        description="Kullanıcı bilgilerini kısmen günceller.",
        request=serializers.UserUpdateSerializer,
        responses=serializers.RegisterSerializer,
        tags=["User"],
    ),
)
class UserUpdateView(generics.UpdateAPIView):
    serializer_class = serializers.UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
