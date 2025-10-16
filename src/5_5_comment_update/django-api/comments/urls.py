from django.urls import path
from .views import CommentListView, CommentDetailsView

urlpatterns = [
    path('<int:pk>', CommentDetailsView.as_view(), name="comment_details"),
    path('<int:pk>/product', CommentListView.as_view(), name="comments_by_product"),
]

# comments/1/product
