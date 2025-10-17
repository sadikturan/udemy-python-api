from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path('admin', views.admin_product_list, name='admin_product_list'),
    path('<int:pk>', views.product_details, name='product_details'),
    path('admin/<int:pk>', views.admin_product_details, name='admin_product_details'),
    path('admin/<int:product_id>/upload-image', views.ProductImageUpload.as_view(), name='admin_product_upload'),
    path('create/', views.product_create, name='product_create'),
    path('update/<int:pk>/', views.update_product, name='update_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
]
