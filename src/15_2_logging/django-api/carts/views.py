from rest_framework import generics, permissions, status, mixins
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Cart, CartItem
from .serializers import AddToCartSerializer, CartSerializer, CartItemUpdateSerializer, EmptySerializer
from .services import add_product_to_cart, get_cart_item_or_404, update_cart_item_quantity

@extend_schema_view(
    post=extend_schema(
        summary="Sepete Ürün Ekle",
        description="Kullanıcının sepetine ürün ekler.",
        tags=["Carts"],
        request=AddToCartSerializer
    )
)
class AddToCartView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddToCartSerializer

    def post(self, request, *args, **kwargs):
        try:
            product_id = request.data.get('product_id')
            quantity = request.data.get('quantity', 1)
            add_product_to_cart(request.user, product_id, quantity)
        except ValidationError as e:
            return Response({'error': str(e.detail[0])}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Product added to cart.'}, status=status.HTTP_200_OK)


@extend_schema(
    summary="Sepet Detayı",
    description="Kullanıcının mevcut sepetini döner.",
    tags=["Carts"]
)
class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

@extend_schema_view(
    put=extend_schema(
        summary="Sepet Ürün Güncelle",
        description="Kullanıcının sepetindeki ürünün adedini günceller.",
        tags=["Carts"],
        request=CartItemUpdateSerializer
    )
)
class UpdateCartItemView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartItemUpdateSerializer

    def put(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quantity = request.data.get('quantity')

        if quantity is None:
            return Response({'error': 'Quantity is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
        except ValueError:
            return Response({'error': 'Quantity must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item = get_cart_item_or_404(pk, request.user)
        updated_item = update_cart_item_quantity(cart_item, quantity)

        if updated_item is None:
            return Response({'message': 'Cart item deleted'}, status=status.HTTP_200_OK)

        return Response({'message': 'Cart item updated.'}, status=status.HTTP_200_OK)


@extend_schema_view(
    delete=extend_schema(
        summary="Sepet Ürünü Sil",
        description="Kullanıcının sepetinden ürünü siler.",
        tags=["Carts"]
    )
)
class DeleteCartItemView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmptySerializer
    
    def delete(self, request, pk):
        try:
            cart_item = CartItem.objects.get(pk=pk, cart__user=request.user)
            cart_item.delete()
            return Response({'message': 'Cart item deleted.'}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            raise NotFound('Cart item not found.')