from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
from carts.services import get_cart_or_create
from .services import create_order_from_cart
from .serializers import OrderSerializer, OrderStatusUpdateSerializer, OrderCreateRequestSerializer, OrderCreateResponseSerializer
from core.utils import get_error_message
from .models import Order

@extend_schema(
    summary="Sipariş Oluştur",
    description="Kullanıcının sepetinden bir sipariş oluşturur. Teslimat ve fatura adresleri, kart bilgileri ve (isteğe bağlı) kupon kodu gereklidir.",
    request=OrderCreateRequestSerializer,
    responses={
        201: OrderCreateResponseSerializer,
    },
    tags=["Orders"]
)
class OrderCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderCreateRequestSerializer

    def create(self, request, *args, **kwargs):
        delivery_address_id = request.data.get('delivery_address_id')
        billing_address_id = request.data.get('billing_address_id')
        card_data = request.data.get('card_data')
        coupon_code = request.data.get('coupon_code')

        if not delivery_address_id or not billing_address_id:
            return Response({'error': 'Delivery and billing addresses are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not card_data:
            return Response({'error': 'Card data is required for payments'}, status=status.HTTP_400_BAD_REQUEST)

        cart = get_cart_or_create(request.user)

        try:
            order, payment_result = create_order_from_cart(
                request.user, cart,
                delivery_address_id,
                billing_address_id,
                card_data,
                coupon_code
            )
        except ValidationError as e:
            return Response({'error': get_error_message(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Unexpected error: ' + get_error_message(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {
                'message': 'Order created successfully.',
                'order_id': order.id,
                'payment': payment_result
            },
            status=status.HTTP_201_CREATED
        )

@extend_schema(
    summary="Kullanıcı Siparişlerini Listele",
    description="Giriş yapmış kullanıcının geçmiş siparişlerini listeler.",
    tags=["Orders"],
    responses=OrderSerializer(many=True),
)
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user).order_by('-created')

@extend_schema(
    summary="Sipariş Detayı",
    description="Giriş yapmış kullanıcının belirli bir siparişinin detaylarını getirir.",
    tags=["Orders"],
    responses=OrderSerializer,
)
class OrderDetailsView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user)
    
@extend_schema(
    summary="Tüm Siparişleri Listele (Admin)",
    description="Tüm kullanıcıların siparişlerini sıralı şekilde listeler. Sadece admin erişimine açıktır.",
    tags=["Orders"],
    responses=OrderSerializer(many=True),
)
class AdminOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Order.objects.order_by('-created')
    
@extend_schema(
    summary="Sipariş Detayı (Admin)",
    description="Belirli bir siparişin detay bilgilerini getirir. Sadece admin kullanıcılar erişebilir.",
    tags=["Orders"],
    responses=OrderSerializer,
)
class AdminOrderDetailsView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]

@extend_schema(
    summary="Sipariş Durumu Güncelle (Admin)",
    description="Belirli bir siparişin durumunu günceller. Sadece admin kullanıcılar erişebilir.",
    tags=["Orders"],
    request=OrderStatusUpdateSerializer,
    responses=OrderStatusUpdateSerializer,
)
class AdminOrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
