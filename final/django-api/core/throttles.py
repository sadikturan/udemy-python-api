from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class MinUserRateThrottle(UserRateThrottle):
    scope = "min_user_request"

class MaxUserRateThrottle(UserRateThrottle):
    scope = "max_user_request"

class MinAnonRateThrottle(AnonRateThrottle):
    scope = "min_anon_request"

class MaxAnonRateThrottle(AnonRateThrottle):
    scope = "max_anon_request"