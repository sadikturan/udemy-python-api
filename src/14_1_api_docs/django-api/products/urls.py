from django.urls import path
from .views import admin_list_products, admin_product_details, catalog_product_details, admin_create_product, admin_edit_product, CatalogProductList, ProductImages, ProductImageDelete, AdminDeleteProduct

urlpatterns = [
    path('', CatalogProductList.as_view(), name="catalog_list_products"),
    path('<int:pk>/', catalog_product_details, name="catalog_product_details"),
    path('admin/', admin_list_products, name="admin_list_products"),
    path('admin/<int:pk>/', admin_product_details, name="admin_product_details"),
    path('admin/create/', admin_create_product, name="admin_create_product"),
    path('admin/<int:pk>/edit/', admin_edit_product, name="admin_edit_product"),
    path('admin/<int:pk>/images', ProductImages.as_view(), name="admin_product_image_upload"),
    path('admin/product-images/<int:pk>', ProductImageDelete.as_view(), name="admin_product_image_delete"),
    path('admin/<int:pk>/delete/', AdminDeleteProduct.as_view(), name="admin_delete_product"),
]
