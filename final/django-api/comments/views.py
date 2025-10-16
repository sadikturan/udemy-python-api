from . import serializers
from .models import Comment
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from core.permissions import IsOwnerOrReadOnly
from core.pagination import LargeResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CommentFilter
from drf_spectacular.utils import extend_schema_view, extend_schema

@extend_schema_view(
    get=extend_schema(
        summary="Yorumları Listele",
        description=(
            "Tüm yorumları listeler. "
            "Filtreleme desteği mevcuttur (örneğin: `?product=<id>`)."
        ),
        responses=serializers.CommentSerializer(many=True),
        tags=["Comment"],
    ),
    post=extend_schema(
        summary="Yeni Yorum Oluştur",
        description="Giriş yapmış kullanıcı tarafından yeni bir yorum oluşturur.",
        request=serializers.CommentCreateSerializer,
        responses=serializers.CommentSerializer,
        tags=["Comment"],
    ),
)
class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LargeResultsSetPagination
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentFilter

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CommentCreateSerializer
        return serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema_view(
    get=extend_schema(
        summary="Yorum Detayı",
        description="Belirtilen ID'ye sahip yorumun detayını döner.",
        responses=serializers.CommentSerializer,
        tags=["Comment"],
    ),
    put=extend_schema(
        summary="Yorumu Güncelle (PUT)",
        description="Yorumun tamamını günceller (tüm alanlar zorunlu). Sadece sahibi güncelleyebilir.",
        request=serializers.CommentUpdateSerializer,
        responses=serializers.CommentSerializer,
        tags=["Comment"],
    ),
    patch=extend_schema(
        summary="Yorumu Güncelle (PATCH)",
        description="Yorumun bir veya birkaç alanını kısmi olarak günceller. Sadece sahibi güncelleyebilir.",
        request=serializers.CommentUpdateSerializer,
        responses=serializers.CommentSerializer,
        tags=["Comment"],
    ),
    delete=extend_schema(
        summary="Yorumu Sil",
        description="Yorumu siler. Sadece yorumu oluşturan kullanıcı silebilir.",
        responses={204: {"message": "Comment deleted"}},
        tags=["Comment"],
    ),
)
class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all() 
    permission_classes= [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ["PUT","PATCH"]:
            return serializers.CommentUpdateSerializer
        return serializers.CommentSerializer
    

    

