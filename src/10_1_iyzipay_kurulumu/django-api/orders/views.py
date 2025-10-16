from django.shortcuts import render
from carts.models import Cart, CartItem
from .models import Order, OrderItem
from carts.services import get_cart_or_create
from .services import create_order_from_cart
from .serializers import OrderSerializer, OrderStatusUpdateSerializer
from rest_framework.views import APIView
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

class OrderCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        delivery_address_id = request.data.get('delivery_address_id')
        billing_address_id = request.data.get('billing_address_id')
        card_data = request.data.get('card_data')

        if not delivery_address_id or not billing_address_id:
            return Response({'error': 'Delivery and billing addresses are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not card_data:
            return Response({'error':'Card data is required for payments'}, status=status.HTTP_400_BAD_REQUEST)

        cart = get_cart_or_create(request.user)

        try:
            order, payment_result = create_order_from_cart(request.user, cart, delivery_address_id, billing_address_id, card_data)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Unexpected error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {
                'message':'Order created successfully.',
                'order_id':order.id,
                'payment': payment_result
            }, 
            status=status.HTTP_201_CREATED)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user).order_by('-created')
    
class OrderDetailsView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user)
    

class AdminOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Order.objects.order_by('-created')
    
class AdminOrderDetailsView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]
    
class AdminOrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
