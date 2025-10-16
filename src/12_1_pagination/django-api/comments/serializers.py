from rest_framework import serializers
from .models import Comment
from users.serializer import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    # user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'rating','description','active','created','update','product','user']
        extra_kwargs = {
            'product': {'read_only': True}
        }

    def get_user(self, obj):
        return obj.user.username if obj.user else None

