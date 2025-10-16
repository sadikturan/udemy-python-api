from rest_framework import generics,permissions, status
from rest_framework.response import Response
from . import serializers
from carts.services import get_cart_or_create
from .services import create_order_from_cart
from rest_framework.exceptions import ValidationError
from .models import Order
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

@extend_schema_view(
    post=extend_schema(
        summary="Sipariş Oluştur",
        description=(
            "Kullanıcının sepetindeki ürünlerden yeni bir sipariş oluşturur. "
            "Teslimat adresi, fatura adresi, kart bilgileri ve kupon kodu isteğe bağlı olarak eklenebilir."
        ),
        request=serializers.OrderCreateSerializer,
        responses={
            201: {
                "example": {
                    "message": "Order created",
                    "order_id": 1,
                    "payment_result": {"status": "success", "transaction_id": "XYZ123"},
                }
            },
            400: {"example": {"error": "Invalid data or payment failure"}},
            500: {"example": {"error": "Unexpected Error"}},
        },
        tags=["Order"],
    )
)
class CreateOrderView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.OrderCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        delivery_address_id = serializer.validated_data.get("delivery_address_id")
        billing_address_id = serializer.validated_data.get("billing_address_id")
        card_data = serializer.validated_data.get("card_data")
        coupon_code = serializer.validated_data.get("coupon_code")

        cart = get_cart_or_create(request.user)

        try:
            order, payment_result = create_order_from_cart(
                request.user,
                cart,
                delivery_address_id,
                billing_address_id,
                card_data,
                coupon_code
            )
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': 'Unexpected Error' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(
            {
                'message': 'Order created', 
                'order_id': order.id,
                'payment_result': payment_result
            },
            status=status.HTTP_201_CREATED)

@extend_schema_view(
    get=extend_schema(
        summary="Kullanıcı Siparişlerini Listele",
        description="Giriş yapmış kullanıcının geçmiş tüm siparişlerini listeler.",
        responses=serializers.OrderSerializer(many=True),
        tags=["Order"],
    )
)
class OrderListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user)

@extend_schema_view(
    get=extend_schema(
        summary="Tüm Siparişleri Listele (Admin)",
        description=(
            "Tüm kullanıcıların siparişlerini listeler. "
            "Opsiyonel olarak `?userId=<id>` parametresi ile filtreleme yapılabilir."
        ),
        parameters=[
            OpenApiParameter(
                name='userId',
                description='Belirli bir kullanıcıya ait siparişleri filtreler.',
                required=False,
                type=int,
                location=OpenApiParameter.QUERY
            )
        ],
        responses=serializers.OrderSerializer(many=True),
        tags=["Order"],
    )
)
class AdminOrderListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        user_id = self.request.query_params.get("userId", None)
        if user_id:
            queryset = queryset.filter(user__id = user_id)
        return queryset
    
@extend_schema_view(
    get=extend_schema(
        summary="Sipariş Detayı (Admin)",
        description="Admin tarafından belirtilen siparişin detaylarını döner.",
        responses=serializers.OrderSerializer,
        tags=["Order"],
    ),
    put=extend_schema(
        summary="Siparişi Güncelle (PUT, Admin)",
        description="Siparişin durumunu veya diğer bilgilerini tamamen günceller.",
        request=serializers.OrderStatusUpdateSerializer,
        responses=serializers.OrderSerializer,
        tags=["Order"],
    ),
    patch=extend_schema(
        summary="Siparişi Güncelle (PATCH, Admin)",
        description="Siparişin bazı alanlarını kısmi olarak günceller (örneğin durum).",
        request=serializers.OrderStatusUpdateSerializer,
        responses=serializers.OrderSerializer,
        tags=["Order"],
    ),
)
class AdminOrderDetailView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class= serializers.OrderSerializer
    lookup_url_kwarg= "order_id"

    def get_serializer_class(self):
        if self.request.method in ["PUT","PATCH"]:
            return serializers.OrderStatusUpdateSerializer
        return  serializers.OrderSerializer

@extend_schema_view(
    get=extend_schema(
        summary="Sipariş Detayı (Kullanıcı)",
        description="Giriş yapmış kullanıcının belirli bir siparişinin detaylarını döner.",
        responses=serializers.OrderSerializer,
        tags=["Order"],
    )
)
class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class= serializers.OrderSerializer
    lookup_url_kwarg= "order_id"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
