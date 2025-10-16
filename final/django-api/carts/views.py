from . import serializers
from . import services
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, extend_schema_view
from core.serializers import EmptySerializer

@extend_schema_view(
    post=extend_schema(
        summary="Sepete Ürün Ekle",
        description="Kullanıcının sepetine ürün ekler.",
        tags=["Cart"],
        request=serializers.AddToCartSerializer
    )
)
class AddToCartView(generics.GenericAPIView):
    serializer_class = serializers.AddToCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data.get("product_id")
        quantity = serializer.validated_data.get("quantity", 1)

        try:
            cart = services.add_product_to_cart(user=request.user, product_id=product_id, quantity=quantity)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializers.CartSerializer(cart).data, status=status.HTTP_200_OK)
    
@extend_schema(
    summary="Sepet Detayı",
    description="Kullanıcının mevcut sepetini döner.",
    tags=["Cart"]
)
class CartDetailview(generics.RetrieveAPIView):
    serializer_class = serializers.CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return services.get_cart_or_create(self.request.user)

@extend_schema_view(
    put=extend_schema(
        summary="Sepet Ürün Güncelle",
        description="Kullanıcının sepetindeki ürünün adedini günceller.",
        tags=["Cart"],
        request=serializers.CartItemUpdateSerializer
    )
)
class UpdateCartItemView(generics.GenericAPIView):
    serializer_class = serializers.CartItemUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, cart_item):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quantity = serializer.validated_data.get("quantity")

        if quantity is None:
            return Response({"error": "quantity is required"})
        
        try:
            cart = services.update_cart_item(user=request.user, cart_item_id=cart_item, quantity=quantity)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializers.CartSerializer(cart).data, status=status.HTTP_200_OK)
        
@extend_schema_view(
    delete=extend_schema(
        summary="Sepet Ürünü Sil",
        description="Kullanıcının sepetinden ürünü siler.",
        tags=["Cart"]
    )
)
class DeleteCartItemView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmptySerializer

    def delete(self, request, cart_item):
        try:
            cart = services.delete_cart_item(request.user, cart_item)
        except ValidationError as e:
            return Response({"error": str(e.detail[0])}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializers.CartSerializer(cart).data, status=status.HTTP_200_OK)

@extend_schema_view(
    delete=extend_schema(
        summary="Sepeti Temizle",
        description="Kullanıcının sepetindeki tüm ürünleri siler ve güncel sepeti döner.",
        tags=["Cart"]
    )
)
class ClearCartView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmptySerializer

    def delete(self, request):
        try:
            cart = services.clear_cart(request.user)
        except ValidationError as e:
            return Response({"error": str(e.detail[0])}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializers.CartSerializer(cart).data, status=status.HTTP_200_OK)

