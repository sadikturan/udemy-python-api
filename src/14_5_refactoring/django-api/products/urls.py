from django.urls import path
from .views import CatalogProductDetailView, CatalogProductList, ProductImages, ProductImageDelete, AdminDeleteProduct, AdminProductListView, AdminProductDetailView, AdminCreateProductView, AdminEditProductView

urlpatterns = [
    path('', CatalogProductList.as_view(), name="catalog_list_products"),
    path('<int:pk>/', CatalogProductDetailView.as_view(), name="catalog_product_details"),
    path('admin/', AdminProductListView.as_view(), name="admin_list_products"),
    path('admin/<int:pk>/', AdminProductDetailView.as_view(), name="admin_product_details"),
    path('admin/create/', AdminCreateProductView.as_view(), name="admin_create_product"),
    path('admin/<int:pk>/edit/', AdminEditProductView.as_view(), name="admin_edit_product"),
    path('admin/<int:pk>/images', ProductImages.as_view(), name="admin_product_image_upload"),
    path('admin/product-images/<int:pk>', ProductImageDelete.as_view(), name="admin_product_image_delete"),
    path('admin/<int:pk>/delete/', AdminDeleteProduct.as_view(), name="admin_delete_product"),
]
