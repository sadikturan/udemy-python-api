from django.urls import path
from . import views

urlpatterns = [
    path('', views.CommentListCreateView.as_view(), name='comment_list'),
    path('<int:pk>', views.CommentRetrieveUpdateDestroyView.as_view(), name='comment_update'),
]

# comments?product=5&user=2&rating=4
