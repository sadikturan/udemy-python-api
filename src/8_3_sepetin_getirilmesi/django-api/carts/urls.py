from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartDetailview.as_view(), name='cart_detail'),
    path('add/', views.AddToCartView.as_view(), name='cart_add'),
]
