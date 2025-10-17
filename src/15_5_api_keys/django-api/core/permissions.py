from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_api_key.models import APIKey

class HasValidAPIKey(BasePermission):
    header_name = "x-api-key"

    def has_permission(self, request, view):
        key = request.headers.get(self.header_name)

        if not key:
            raise AuthenticationFailed(f"{self.header_name} header bilgisi bulunamadı.")
        
        try:
            api_key_obj = APIKey.objects.get_from_key(key)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed("Geçerli bir API anahtarı sağlanamadı.")
        
        return True
    
class IsAuthenticatedWithAPIKey(HasValidAPIKey):
    def has_permission(self, request, view):
        super().has_permission(request, view)
        
        user = request.user

        if not user or not user.is_authenticated:
             raise AuthenticationFailed("JWT kimlik doğrumalaması başarısız.")
        
        return True
    
class IsAdminWithAPIKey(HasValidAPIKey):
    def has_permission(self, request, view):
        super().has_permission(request, view)
        
        user = request.user

        if not user.is_staff:
             raise AuthenticationFailed("Yalnız admin kullancıları erişebilir.")
        
        return True

class IsAdminOrReadOnly(HasValidAPIKey):
    def has_permission(self, request, view):
        super().has_permission(request, view)

        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
    
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.user
    
