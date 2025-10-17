from django.shortcuts import render
from rest_framework.views import APIView
from .models import Comment
from . import serializers
from rest_framework.response import Response

class CommentListView(APIView):
    
    def get(self, request):
        comments = Comment.objects.all()
        serializer = serializers.CommentSerializer(comments,many=True)
        return Response(serializer.data)
