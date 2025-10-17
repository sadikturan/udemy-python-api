from . import serializers
from .models import Comment
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from core.permissions import IsOwnerOrReadOnly
from core.pagination import LargeResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CommentFilter

class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LargeResultsSetPagination
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentFilter

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CommentCreateSerializer
        return serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all() 
    permission_classes= [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ["PUT","PATCH"]:
            return serializers.CommentUpdateSerializer
        return serializers.CommentSerializer
    

    

