from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('categories/', include('categories.urls')),
    path('comments/', include('comments.urls')),
    path('users/', include('users.urls')),
]
