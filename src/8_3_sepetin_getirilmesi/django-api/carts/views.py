from django.shortcuts import render
from rest_framework import generics, permissions, status
from . import serializers
from .models import Cart, CartItem
from products.models import Product
from rest_framework.response import Response

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


