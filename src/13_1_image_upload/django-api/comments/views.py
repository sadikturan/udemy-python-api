from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError, PermissionDenied
from core.paginations import LargeResultsSetPagination, StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CommentFilter

class AdminCommentList(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]
    pagination_class = LargeResultsSetPagination
    queryset = Comment.objects.all().order_by('-update')
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentFilter

class CommentList(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Comment.objects.filter(product_id=pk)
    
class CommentCreate(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs.get("pk")
        user = self.request.user

        existing_comment = Comment.objects.filter(product_id=product_id, user=user)
        if existing_comment.exists():
            raise ValidationError({"message":"You have already commented on this product."})

        serializer.save(product_id=product_id,user=user)

class CommentEditDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()

        if obj.user != self.request.user:
            raise PermissionDenied("You dont have permission to edit this comment.")
        return obj
    
    
class AdminCommentEditDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]




    


  

