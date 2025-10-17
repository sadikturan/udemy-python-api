from django.urls import path
from . import views

urlpatterns = [
    path('', views.CommentListCreateView.as_view(), name='comment_list_create'),
    path('<int:pk>', views.CommentUpdateView.as_view(), name='comment_update'),
]
