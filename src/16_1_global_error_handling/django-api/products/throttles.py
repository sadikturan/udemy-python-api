from rest_framework.throttling import UserRateThrottle

class ProductListThrottle(UserRateThrottle):
    scope = "product_list_user"