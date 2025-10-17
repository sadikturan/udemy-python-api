from django.urls import path
from . import views

urlpatterns = [
    path('', views.CommentListCreateView.as_view(), name='comment_list'),
    path('<int:product_id>/product', views.CommentListCreateView.as_view(), name='product_comment_list'),
    path('<int:pk>', views.CommentRetrieveUpdateDestroyView.as_view(), name='comment_update'),
]
