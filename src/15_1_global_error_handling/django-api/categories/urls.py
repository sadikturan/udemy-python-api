from django.urls import path
from .views import CatalogCategoryList, AdminCategoryListCreateView, CatalogCategoryDetails, AdminCategoryDetailUpdateDeleteView

urlpatterns = [
    path('', CatalogCategoryList.as_view(), name="catalog_category_list"),
    path('<int:pk>/', CatalogCategoryDetails.as_view(), name="catalog_category_details"),
    path('admin/', AdminCategoryListCreateView.as_view(), name="admin_category_list"),
    path('admin/<int:pk>/', AdminCategoryDetailUpdateDeleteView.as_view(), name="admin_category_details"),
]