from django.urls import path
from .views import CommentList, CommentCreate, CommentRetrieveUpdateDelete, AdminCommentList, AdminCommentRetrieveUpdateDelete

urlpatterns = [
    path('product/<int:product_id>', CommentList.as_view(), name="comment_list"),
    path('<int:product_id>/create', CommentCreate.as_view(), name="comment_create"),
    path('<int:pk>', CommentRetrieveUpdateDelete.as_view(), name="comment_edit_delete"),
    path('admin', AdminCommentList.as_view(), name="admin_comment_list"),
    path('admin/<int:pk>', AdminCommentRetrieveUpdateDelete.as_view(), name="comment_edit_delete"),
]
