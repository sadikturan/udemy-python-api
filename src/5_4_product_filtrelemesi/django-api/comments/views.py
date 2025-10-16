from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer

class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentListByProductView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Comment.objects.filter(product_id=pk)
    
class CommentDetailsView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer



  

