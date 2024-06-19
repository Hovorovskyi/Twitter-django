from django.urls import path

from posts.views import PostListView, PostCreateView, PostDetailView, CommentCreateView, like_post, \
    PostUpdateView, PostDeleteView
from users.views import FollowingPostListView


urlpatterns = [
    path('all_posts/', PostListView.as_view(), name='post_list'),
    path('add-post/', PostCreateView.as_view(), name='add_post'),
    path('post-detail/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('post-detail/<int:pk>/add_comment/', CommentCreateView.as_view(), name='add_comment'),
    path('like-post/<int:pk>', like_post, name='like_post'),
    path('edit-post/<int:pk>', PostUpdateView.as_view(), name='edit_post'),
    path('delete-post/<int:pk>', PostDeleteView.as_view(), name='delete_post'),
    path('following_posts/', FollowingPostListView.as_view(), name='following_posts')
]
