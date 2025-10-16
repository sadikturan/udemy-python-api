from django.urls import path
from .views import AdminCouponList, AdminCouponDetail

urlpatterns = [
    path('admin/', AdminCouponList.as_view(), name="admin_coupon_list"),
    path('admin/<int:pk>', AdminCouponDetail.as_view(), name="admin_coupon_detail"),


    # path('admin/product/<int:pk>', AdminCommentList.as_view(), name="admin_comment_list_product"),
    # path('admin/<int:pk>/edit/', AdminCommentEdit.as_view(), name="comment_edit"),
    # path('admin/<int:pk>/delete/', AdminCommentDelete.as_view(), name="comment_delete"),
#      path('product/<int:pk>', CommentList.as_view(), name="comment_list"),
#     path('<int:pk>/create/', CommentCreate.as_view(), name="comment_create"),
#     path('<int:pk>/edit/', CommentEdit.as_view(), name="comment_edit"),
#     path('<int:pk>/delete/', CommentDelete.as_view(), name="comment_delete"),
]
