from django.urls import path
from .views import product_list, product_details, product_create

urlpatterns = [
    path('', product_list, name='product_list'),
    path('<int:pk>', product_details, name='product_details'),
    path('create/', product_create, name='product_create'),
]
