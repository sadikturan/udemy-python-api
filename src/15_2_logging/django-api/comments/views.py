from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError, PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from core.paginations import LargeResultsSetPagination, StandardResultsSetPagination
from .models import Comment
from .serializers import CommentSerializer
from .filters import CommentFilter

@extend_schema(
    summary="Yorumları Listele (Admin)",
    description="Tüm kullanıcı yorumlarını listelemek için kullanılır. Admin yetkisi gerektirir. Filtreleme ve sayfalama desteklenir.",
    tags=["Comments"],
    responses=CommentSerializer(many=True)
)
class AdminCommentList(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]
    pagination_class = LargeResultsSetPagination
    queryset = Comment.objects.all().order_by('-update')
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentFilter

@extend_schema_view(
    get=extend_schema(
        summary="Yorum Detayı (Admin)",
        description="Yorumun detaylarını getirir. Yalnızca admin erişimine açıktır.",
        responses=CommentSerializer,
        tags=["Comments"]
    ),
    put=extend_schema(
        summary="Yorum Güncelle (Admin)",
        description="Yorumu günceller. Yalnızca admin erişimine açıktır.",
        request=CommentSerializer,
        responses=CommentSerializer,
        tags=["Comments"]
    ),
    patch=extend_schema(
        summary="Yorum Güncelle (Admin)",
        description="Kullanıcının kendi yaptığı yorumu kısmen güncellemesini sağlar.",
        request=CommentSerializer,
        responses=CommentSerializer,
        tags=["Comments"]
    ),
    delete=extend_schema(
        summary="Yorum Sil (Admin)",
        description="Yorumu siler. Yalnızca admin erişimine açıktır.",
        tags=["Comments"]
    )
)
class AdminCommentRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]

@extend_schema(
    summary="Ürün Yorumlarını Listele",
    description="Belirli bir ürüne ait tüm yorumları listeler.",
    tags=["Comments"],
    responses=CommentSerializer(many=True)
)
class CommentList(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        return Comment.objects.filter(product_id=product_id)

@extend_schema(
    summary="Ürün Yorumu Oluştur",
    description="Belirli bir ürüne, giriş yapmış kullanıcı tarafından yorum eklenmesini sağlar. Her kullanıcı bir ürüne yalnızca bir yorum yapabilir.",
    tags=["Comments"],
    request=CommentSerializer,
    responses={
        201: CommentSerializer,
        400: {"type": "object", "properties": {"message": {"type": "string"}}}
    }
)
class CommentCreate(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs.get("product_id")
        user = self.request.user

        existing_comment = Comment.objects.filter(product_id=product_id, user=user)
        if existing_comment.exists():
            raise ValidationError({"message":"You have already commented on this product."})

        serializer.save(product_id=product_id,user=user)

@extend_schema_view(
    get=extend_schema(
        summary="Yorum Detayı",
        description="Kullanıcının kendi yaptığı bir yorumu detaylı olarak görüntülemesini sağlar.",
        responses=CommentSerializer,
        tags=["Comments"]
    ),
    put=extend_schema(
        summary="Yorum Güncelle",
        description="Kullanıcının kendi yaptığı yorumu güncellemesini sağlar.",
        request=CommentSerializer,
        responses=CommentSerializer,
        tags=["Comments"]
    ),
    patch=extend_schema(
        summary="Yorum Güncelle (PATCH)",
        description="Kullanıcının kendi yaptığı yorumu kısmen güncellemesini sağlar.",
        request=CommentSerializer,
        responses=CommentSerializer,
        tags=["Comments"]
    ),
    delete=extend_schema(
        summary="Yorum Sil",
        description="Kullanıcının kendi yaptığı yorumu silmesini sağlar.",
        tags=["Comments"]
    )
)
class CommentRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()

        if obj.user != self.request.user:
            raise PermissionDenied("You dont have permission to edit this comment.")
        return obj
    
    




    


  

