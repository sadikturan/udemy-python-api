from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', include('products.urls')),
    path('api/categories/', include('categories.urls')),
    path('api/comments/', include('comments.urls')),
    path('api/users/', include('users.urls')),
    path('api/carts/', include('carts.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/addresses/', include('addresses.urls')),
    path('api/coupons/', include('coupons.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
