from rest_framework import generics, permissions
from .models import Address
from . import serializers

class AddressListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)



