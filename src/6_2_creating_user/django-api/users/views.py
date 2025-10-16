from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializer import SignUpSerializer

User =get_user_model()

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
