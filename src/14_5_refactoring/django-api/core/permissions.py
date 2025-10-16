from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_api_key.models import APIKey

class HasValidAPIKey(BasePermission):
    def has_valid_api_key(self, request):
        key = request.headers.get('x-api-key')

        if not key:
            raise AuthenticationFailed("x-api-key header'ı bulunamadı.")
        
        try:
            api_key_obj = APIKey.objects.get_from_key(key)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed("Geçerli bir API anahtarı sağlamadınız.")
        
        request.auth = api_key_obj
        return True
    
    def has_permission(self, request, view):
        return self.has_valid_api_key(request)
    
class IsAuthenticatedWithAPIKey(HasValidAPIKey):
    def has_permission(self, request, view):
        self.has_valid_api_key(request)

        user = request.user

        if not user or not user.is_authenticated:
            raise AuthenticationFailed("JWT kimlik doğrulaması başarısız.")
        
        return True
    
class IsAdminWithAPIKey(HasValidAPIKey):
    def has_permission(self, request, view):
        self.has_valid_api_key(request)

        user = request.user

        if not user or not user.is_authenticated:
            raise AuthenticationFailed("JWT kimlik doğrulaması başarısız.")

        if not user.is_staff:
            raise AuthenticationFailed("Yalnızca admin kullanıcılar erişebilir.")
        
        return True