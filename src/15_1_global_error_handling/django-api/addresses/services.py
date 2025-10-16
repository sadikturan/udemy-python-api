from .models import Address
from rest_framework.exceptions import ValidationError

def get_user_addresses(user):
    return Address.objects.filter(user=user)

def set_default_address(address):
    Address.objects.filter(user=address.user, is_default=True).update(is_default=False)
    address.is_default=True
    address.save()

def get_user_address_or_404(user, address_id):
    try:
        return Address.objects.get(id=address_id, user=user)
    except Address.DoesNotExist:
        raise ValidationError({'error':'Invalid address.'})