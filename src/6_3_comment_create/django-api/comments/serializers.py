from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["rating", "text", "product"]
        extra_kwargs  = {
            "rating": {
                "error_messages": {
                    "min_value": "Rating 1' den küçük olamaz.",
                    "max_value": "Rating 5' ten büyük olamaz."
                }
            }
        }

    def validate_text(self, value):
        if value and len(value) < 5:
            raise serializers.ValidationError("Yorum için en az 5 karakter girmelisiniz.")
        return value