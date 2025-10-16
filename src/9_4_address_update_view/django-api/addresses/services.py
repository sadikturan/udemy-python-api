from .models import Address

def get_user_addresses(user):
    return Address.objects.filter(user=user)

def set_default_address(address):
    Address.objects.filter(user=address.user, is_default=True).update(is_default=False)
    address.is_default=True
    address.save()

def get_user_addresses(user):
    return Address.objects.filter(user=user)