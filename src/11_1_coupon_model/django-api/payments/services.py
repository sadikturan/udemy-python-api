from django.conf import settings
from rest_framework.exceptions import ValidationError
from decimal import Decimal
from products.services import decrease_product_stock
import json
import iyzipay

options = {
    'api_key': settings.IYZICO_API_KEY,
    'secret_key': settings.IYZICO_SECRET_KEY,
    'base_url': settings.IYZICO_BASE_URL,
}

def create_payment(user, order, card_data):

    if order.total_price <= 0:
        raise ValidationError({'error': 'Order total must be greater than zero.'})
    
    basket_items = []
    basket_total = Decimal('0.00')
    
    for item in order.items.all():
        item_price = Decimal(item.price * item.quantity).quantize(Decimal('0.01'))
        basket_total += item_price

        basket_items.append(
            {
                'id': str(item.id),
                'name': item.product.name,
                'category1': item.product.category.name if item.product.category else "",
                'itemType': 'PHYSICAL',
                'price': str(item_price)
            }
        )

    order_total = Decimal(order.total_price).quantize(Decimal('0.01'))
    if basket_total != order_total:
        raise ValidationError(f'Basket total ({basket_total}) does not match order total ({order_total})')
    
    payment_card = {
        'cardHolderName': card_data['cardHolderName'],
        'cardNumber': card_data['cardNumber'],
        'expireMonth': card_data['expireMonth'],
        'expireYear': card_data['expireYear'],
        'cvc': card_data['cvc'],
        'registerCard': '0'
    }   

    buyer = {
        'id': str(user.id),
        'name': user.first_name,
        'surname': user.last_name,
        'gsmNumber': user.phone if hasattr(user,"phone") else "",
        'email': user.email,
        'identityNumber': '74300864791',
        'registrationAddress': order.delivery_address.address_line if order.delivery_address else "",
        'ip': '85.34.78.112',
        'city': order.delivery_address.city.name if order.delivery_address and order.delivery_address.city else "",
        'country': 'Turkey',
    }

    billingAddress = {
        'contactName': order.billing_address.full_name if order.billing_address else "",
        'city': order.billing_address.city.name if order.billing_address and order.billing_address.city else "",
        'country': 'Turkey',
        'address': order.billing_address.address_line if order.billing_address else "",
        'zipCode': order.billing_address.postal_code if order.billing_address else "",
    }

    deliveryAddress = {
        'contactName': order.delivery_address.full_name if order.delivery_address else "",
        'city': order.delivery_address.city.name if order.delivery_address and order.delivery_address.city else "",
        'country': 'Turkey',
        'address': order.delivery_address.address_line if order.delivery_address else "",
        'zipCode': order.delivery_address.postal_code if order.delivery_address else "",
    }


    request = {
        'locale': 'tr',
        'conversationId': str(order.id),
        'price': str(order.total_price),
        'paidPrice': str(order.total_price),
        'currency': 'TRY',
        'installment': '1',
        'basketId': str(order.id),
        'paymentChannel': 'WEB',
        'paymentGroup': 'PRODUCT',
        'paymentCard': payment_card,
        'buyer': buyer,
        'shippingAddress': deliveryAddress,
        'billingAddress': billingAddress,
        'basketItems': basket_items
    }

    payment = iyzipay.Payment().create(request, options)
    result = json.loads(payment.read().decode('utf-8'))

    if result['status'] != 'success':
        error_code = result.get('errorCode')
        error_message = result.get('errorMessage', 'Payment failed')
        error_description = iyzico_error_messages(error_code, error_message)

        raise ValidationError(error_description)
    
    for item in order.items.all():
        decrease_product_stock(item.product, item.quantity)

    return result

def iyzico_error_messages(error_code, default_message):
    errors = {
        '10101': 'Geçersiz kart numarası. Lütfen kart bilgilerinizi kontrol ediniz.',
        '10102': 'Kartınızın son kullanma tarihi hatalı.',
        '10103': 'Kart CVV kodu hatalı.',
        '10104': 'Bu kart kullanılamıyor, bankanızla iletişime geçiniz.',
        '10105': 'Kartınızda yeterli bakiye bulunmamaktadır.',
        '10106': 'Kartınız internet alışverişine kapalı. Bankanızdan açtırabilirsiniz.',
        '10201': 'İşlem sırasında teknik bir hata oluştu. Lütfen tekrar deneyiniz.',
    }

    return errors.get(error_code, default_message)