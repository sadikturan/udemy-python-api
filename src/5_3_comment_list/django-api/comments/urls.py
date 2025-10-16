from django.urls import path
from .views import CommentListView

urlpatterns = [
    path('', CommentListView.as_view(), name="comments"),
]

# comments 
# comments/1/product
