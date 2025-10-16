from .models import Address

def get_user_addresses(user):
    return Address.objects.filter(user=user)