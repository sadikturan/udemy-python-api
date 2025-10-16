from django.urls import path
from .views import CategoryListAV, CategoryDetailsAV

urlpatterns = [
    path('', CategoryListAV.as_view(), name="categories"),
    path('<int:pk>', CategoryDetailsAV.as_view(), name="category_details"),
]
