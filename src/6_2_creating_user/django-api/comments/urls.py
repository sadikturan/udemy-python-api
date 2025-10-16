from django.urls import path
from .views import CommentListView, CommentDetailsView, CommentDeleteView

urlpatterns = [
    path('<int:pk>', CommentDetailsView.as_view(), name="comment_details"),
    path('<int:pk>/product', CommentListView.as_view(), name="comments_by_product"),
    path('<int:pk>/delete', CommentDeleteView.as_view(), name="comment_delete"),
]

# comments/1/product
