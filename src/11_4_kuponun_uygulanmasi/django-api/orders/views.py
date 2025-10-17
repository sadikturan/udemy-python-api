from rest_framework import generics,permissions, status
from rest_framework.response import Response
from . import serializers
from carts.services import get_cart_or_create
from .services import create_order_from_cart
from rest_framework.exceptions import ValidationError

class CreateOrderview(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.OrderCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        delivery_address_id = serializer.validated_data.get("delivery_address_id")
        billing_address_id = serializer.validated_data.get("billing_address_id")
        coupon_code = serializer.validated_data.get("coupon_code")

        cart = get_cart_or_create(request.user)

        try:
            order = create_order_from_cart(
                request.user,
                cart,
                delivery_address_id,
                billing_address_id,
                coupon_code
            )
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': 'Unexpected Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({'message': 'Order created', 'order_id': order.id},status=status.HTTP_201_CREATED)



