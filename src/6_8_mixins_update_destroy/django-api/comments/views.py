from . import serializers
from .models import Comment
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins
from django.shortcuts import get_object_or_404

class CommentListCreateView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CommentCreateSerializer
        return serializers.CommentSerializer

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        if product_id:
            return Comment.objects.filter(product_id=product_id)
        return Comment.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request,  *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    
class CommentRetrieveUpdateDestroyView(generics.GenericAPIView, 
                        mixins.RetrieveModelMixin, 
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    
    queryset =  Comment.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PUT","PATCH"]:
            return serializers.CommentUpdateSerializer
        return serializers.CommentSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    



