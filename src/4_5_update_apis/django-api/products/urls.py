from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:pk>', views.product_details, name='product_details'),
    path('create/', views.product_create, name='product_create'),
    path('update/<int:pk>/', views.update_product, name='update_product'),
]
