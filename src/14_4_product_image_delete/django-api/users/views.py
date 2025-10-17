from rest_framework import generics, status, permissions
from rest_framework.response import Response
from  rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from . import serializers

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = serializer.validated_data["refresh"]
        access = serializer.validated_data["access"]

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "refresh": refresh,
            "access": access
        }, status=status.HTTP_200_OK)
    
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

class UserUpdateView(generics.UpdateAPIView):
    serializer_class = serializers.UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
