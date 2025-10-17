from django.urls import path
from . import views

urlpatterns = [
    path('', views.CommentListView.as_view(), name='comment_list'),
]
