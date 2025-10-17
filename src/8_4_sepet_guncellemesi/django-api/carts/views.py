from django.shortcuts import render
from rest_framework import generics, permissions, status
from . import serializers
from .models import Cart, CartItem
from products.models import Product
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

class AddToCartView(generics.GenericAPIView):
    serializer_class = serializers.AddToCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data.get("product_id")
        quantity = serializer.validated_data.get("quantity", 1)

        cart, cartCreated = Cart.objects.get_or_create(user = request.user)
        product = Product.objects.get(id=product_id)

        cart_item, itemCreated = CartItem.objects.get_or_create(cart=cart,product=product)

        if not itemCreated:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)

        cart_item.save()

        return Response({"message": "Product added to cart."}, status=status.HTTP_200_OK)
    
class CartDetailview(generics.RetrieveAPIView):
    serializer_class = serializers.CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

class UpdateCartItemView(generics.GenericAPIView):
    serializer_class = serializers.CartItemUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, cart_item):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quantity= serializer.validated_data.get("quantity")

        if quantity is None:
            return Response({"error": "quantity is required"})
        
        try:
            cart_item = CartItem.objects.get(pk=cart_item, cart__user = request.user)
        except CartItem.DoesNotExist:
            raise NotFound({"error": "Cart item not found"})
        
        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        cart = Cart.objects.get(user=request.user)
        serializer = serializers.CartSerializer(cart)

        return Response(serializer.data, status=status.HTTP_200_OK)

