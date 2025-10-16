from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import AddressListSerializer
from .services import get_user_addresses

class AddressListView(generics.ListAPIView):
    serializer_class = AddressListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_user_addresses(self.request.user)
