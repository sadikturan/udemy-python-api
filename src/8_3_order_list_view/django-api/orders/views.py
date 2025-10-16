from django.shortcuts import render
from carts.models import Cart, CartItem
from .models import Order, OrderItem
from .serializers import OrderSerializer
from rest_framework.views import APIView
from rest_framework import permissions, status, generics
from rest_framework.response import Response

class CreateOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = Cart.objects.get(user=user)
        cart_items = cart.items.all()

        if not cart_items:
            return Response({'error': 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.create(user=user)

        for item in cart_items:
            OrderItem.objects.create(
                order = order,
                product = item.product,
                quantity = item.quantity,
                price = item.product.price
            )

        order.calculate_total()

        cart.items.all().delete()

        return Response({'message':'Order created successfully.','order_id':order.id}, status=status.HTTP_201_CREATED)


class CreateListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user).order_by('-created')
    
class CreateDetailsView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user)