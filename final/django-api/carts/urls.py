from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartDetailview.as_view(), name='cart_detail'),
    path('add', views.AddToCartView.as_view(), name='cart_add'),
    path('update/<int:cart_item>', views.UpdateCartItemView.as_view(), name='cart_update'),
    path('delete/<int:cart_item>', views.DeleteCartItemView.as_view(), name='cart_delete'),
    path('clear', views.ClearCartView.as_view(), name='cart_clear'),
]
