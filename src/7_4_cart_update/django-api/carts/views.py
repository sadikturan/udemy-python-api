from django.shortcuts import render
from .models import Cart, CartItem
from products.models import Product
from .serializers import CartItemSerializer, CartSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import NotFound

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        cart, created = Cart.objects.get_or_create(user = request.user)
        product = Product.objects.get(id=product_id)

        cart_item, created = CartItem.objects.get_or_create(cart = cart, product = product)

        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)

        cart_item.save()

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
        try:
            cart_item = CartItem.objects.get(pk=pk, cart__user=request.user)
        except CartItem.DoesNotExist:
            raise NotFound('Cart item not found.')
        
        quantity = request.data.get('quantity')

        if quantity is not None:
            cart_item.quantity = quantity
            cart_item.save()
            return Response({'message':'Cart item updated.'}, status=status.HTTP_200_OK)
        else: 
            return Response({'error':'Quantity is required'}, status=status.HTTP_400_BAD_REQUEST)
