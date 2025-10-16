from django.urls import path
from .views import admin_list_products, admin_product_details, catalog_product_details, admin_create_product, admin_edit_product, admin_delete_product, CatalogProductList, ProductImageUpload

urlpatterns = [
    path('', CatalogProductList.as_view(), name="catalog_list_products"),
    path('<int:pk>/', catalog_product_details, name="catalog_product_details"),
    path('admin/', admin_list_products, name="admin_list_products"),
    path('admin/<int:pk>/', admin_product_details, name="admin_product_details"),
    path('admin/create/', admin_create_product, name="admin_create_product"),
    path('admin/<int:pk>/edit/', admin_edit_product, name="admin_edit_product"),
    path('admin/<int:pk>/upload-image', ProductImageUpload.as_view(), name="admin_product_image_upload"),
    path('admin/<int:pk>/delete/', admin_delete_product, name="admin_delete_product"),
]
