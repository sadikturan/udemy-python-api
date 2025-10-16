from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer

class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        product_id =  self.kwargs.get("pk")
        serializer.save(product_id=product_id)

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Comment.objects.filter(product_id=pk)
    
class CommentDetailsView(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer



  

