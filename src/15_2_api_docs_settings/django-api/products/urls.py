from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path('admin', views.admin_product_list, name='admin_product_list'),
    path('<int:pk>', views.product_details, name='product_details'),
    path('admin/<int:pk>', views.admin_product_details, name='admin_product_details'),
    path('admin/<int:pk>/images', views.ProductImages.as_view(), name='admin_product_images'),
    path('admin/images/<int:pk>', views.ProductImageDelete.as_view(), name='admin_product_image_delete'),
    path('admin/create', views.product_create, name='product_create'),
    path('admin/update/<int:pk>', views.update_product, name='update_product'),
    path('admin/delete/<int:pk>', views.DeleteProduct.as_view(), name='delete_product'),
]
