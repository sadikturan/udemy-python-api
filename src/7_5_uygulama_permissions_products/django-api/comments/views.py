from . import serializers
from .models import Comment
from rest_framework import generics

class CommentListCreateView(generics.ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CommentCreateSerializer
        return serializers.CommentSerializer

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        if product_id:
            return Comment.objects.filter(product_id=product_id)
        return Comment.objects.all()
    
class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset =  Comment.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PUT","PATCH"]:
            return serializers.CommentUpdateSerializer
        return serializers.CommentSerializer
    

