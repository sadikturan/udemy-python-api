from django.conf import settings
import iyzipay
import json
from rest_framework.exceptions import ValidationError

options = {
    'api_key': settings.IYZICO_API_KEY,
    'secret_key': settings.IYZICO_SECRET_KEY,
    'base_url': settings.IYZICO_BASE_URL,
}

def create_payment(user, order, card_data):
    payment_card = {
        'cardHolderName': card_data.get("card_name"),
        'cardNumber': card_data.get("card_number"),
        'expireMonth': card_data.get("expiry_month"),
        'expireYear': card_data.get("expiry_year"),
        'cvc': card_data.get("cvc"),
        'registerCard': '0'
    }

    buyer = {
        'id': str(user.id),
        'name': user.first_name or order.delivery_address.full_name.split()[0],
        'surname': user.last_name or order.delivery_address.full_name.split()[1],
        'gsmNumber': order.delivery_address.phone,
        'email': user.email,
        'identityNumber': '74300864791',
        'lastLoginDate': str(user.last_login or ''),
        'registrationDate': str(user.date_joined or ''),
        'registrationAddress': order.delivery_address.address_line,
        'ip': '85.34.78.112',
        'city': order.delivery_address.city.name,
        'country': 'Turkey',
        'zipCode': order.delivery_address.postal_code
    }

    shipping_address = {
        'contactName': order.delivery_address.full_name,
        'city': order.delivery_address.city.name,
        'country': 'Turkey',
        'address': f"{order.delivery_address.address_line}, {order.delivery_address.district or ''}, {order.delivery_address.street}",
        'zipCode': order.delivery_address.postal_code
    }

    billing_address = {
        'contactName': order.billing_address.full_name,
        'city': order.billing_address.city.name,
        'country': 'Turkey',
        'address': f"{order.billing_address.address_line}, {order.billing_address.district or ''}, {order.billing_address.street}",
        'zipCode': order.billing_address.postal_code
    }

    basket_items = []
    basket_total = 0

    for item in order.items.select_related('product','product__category'):
        price_total = item.price * item.quantity
        basket_total += price_total
        basket_items.append({
            'id': str(item.product.id),
            'name': item.product.name,
            'category1': getattr(item.product.category,'name','Category'),
            'itemType': 'PHYSICAL',
            'price': str(item.price)
        })

    price = str(round(basket_total, 2))
    paid_price = str(round(order.order_total,2))

    request = {
        'locale': 'tr',
        'conversationId': str(order.id),
        'price': price,
        'paidPrice': paid_price,
        'currency': 'TRY',
        'installment': '1',
        'basketId': f"ORDER-{order.id}",
        'paymentChannel': 'WEB',
        'paymentGroup': 'PRODUCT',
        'paymentCard': payment_card,
        'buyer': buyer,
        'shippingAddress': shipping_address,
        'billingAddress': billing_address,
        'basketItems': basket_items
    }

    payment = iyzipay.Payment().create(request, options)
    result = json.loads(payment.read().decode('utf-8'))

    if result["status"] != "success":
        error_code = result.get("errorCode")
        error_message  = result.get("errorMessage",'Payment failed')
        error_description = iyzico_error_messages(error_code, error_message)

        raise ValidationError(error_description)

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