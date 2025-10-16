from django.urls import path
from .views import CategoryListAV

urlpatterns = [
    path('', CategoryListAV.as_view(), name="categories"),
    path('<int:pk>', CategoryListAV.as_view(), name="category_details"),
]
