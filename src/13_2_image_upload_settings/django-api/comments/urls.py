from django.urls import path
from .views import CommentList, CommentCreate, CommentEditDelete, AdminCommentList, AdminCommentEditDelete

urlpatterns = [
    path('product/<int:pk>', CommentList.as_view(), name="comment_list"),
    path('<int:pk>/create', CommentCreate.as_view(), name="comment_create"),
    path('<int:pk>', CommentEditDelete.as_view(), name="comment_edit_delete"),

    path('admin', AdminCommentList.as_view(), name="admin_comment_list"),
    path('admin/<int:pk>', AdminCommentEditDelete.as_view(), name="comment_edit_delete"),
]
