from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied

class CommentList(generics.ListAPIView):
    serializer_class = CommentSerializer

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

class CommentEdit(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()

        if obj.user != self.request.user:
            raise PermissionDenied("You dont have permission to edit this comment.")
        return obj

    
class CommentDelete(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()

        if obj.user != self.request.user:
            raise PermissionDenied("You dont have permission to delete this comment.")
        return obj


  

