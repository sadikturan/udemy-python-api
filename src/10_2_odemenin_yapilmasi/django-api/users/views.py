from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializer import SignUpSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from .tokens import get_tokens_for_user

User = get_user_model()

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

class LoginView(APIView):

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = get_tokens_for_user(user)

            response = {
                "message": "Login successfull",
                "token": tokens
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message":"Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
