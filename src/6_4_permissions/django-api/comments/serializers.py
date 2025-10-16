from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'rating','description','active','created','update','product']
        extra_kwargs = {
            'product': {'read_only': True}
        }