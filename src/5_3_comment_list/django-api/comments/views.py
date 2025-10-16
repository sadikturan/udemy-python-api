from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer
from rest_framework import mixins

class CommentListView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args,**kwargs):
        return self.list(request, *args,**kwargs)

