from django.shortcuts import render
from .models import Cart, CartItem
from products.models import Product
from .services import add_product_to_cart, get_cart_item_or_404, update_cart_item_quantity
from .serializers import CartItemSerializer, CartSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import NotFound, ValidationError

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            product_id = request.data.get('product_id')
            quantity = request.data.get('quantity', 1)
            add_product_to_cart(request.user, product_id, quantity)
        except ValidationError as e:
            return Response({'error': str(e.detail[0])}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message':'Product added to cart.'}, status=status.HTTP_200_OK)
    
class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart
    
class UpdateCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):       
        
        quantity = request.data.get('quantity')

        if quantity is None:
            return Response({'error':'Quantity is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            quantity = int(quantity)
        except ValueError:
            return Response({'error': 'Quantity must be a integer'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item = get_cart_item_or_404(pk, request.user)
        updated_item = update_cart_item_quantity(cart_item, quantity)

        if updated_item is None:
            return Response({'message':'Cart item deleted'}, status=status.HTTP_200_OK)
        
        return Response({'message':'Cart item updated.'}, status=status.HTTP_200_OK)
            
        
class DeleteCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            cart_item = CartItem.objects.get(pk=pk, cart__user=request.user)
            cart_item.delete()
            return Response({'message':'Cart item deleted.'}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            raise NotFound('Cart item not found.')
