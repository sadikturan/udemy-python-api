from django.urls import path
from .views import CommentList, CommentCreate, CommentEdit, CommentDelete

urlpatterns = [
    path('product/<int:pk>', CommentList.as_view(), name="comment_list"),
    path('<int:pk>/create/', CommentCreate.as_view(), name="comment_create"),
    path('<int:pk>/edit/', CommentEdit.as_view(), name="comment_edit"),
    path('<int:pk>/delete/', CommentDelete.as_view(), name="comment_delete"),
]

# comments/product/1    => product comment list
# comments/1/create     => create comment
# comments/1/edit       => comment edit
# comments/1/delete     => comment delete
