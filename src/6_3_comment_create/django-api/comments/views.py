from . import serializers
from .models import Comment
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CommentListCreateView(APIView):
    
    def get(self, request):
        comments = Comment.objects.all()
        serializer = serializers.CommentSerializer(comments,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
