from django.urls import path

from users.views import UserListView, UserCreateView, UserDetailView, login_view, logout_view, UserUpdateView, \
    FollowingUserView, WatchFollowingView, WatchFollowersView
from posts.views import PostsByUserListView


urlpatterns = [
    path('users/', UserListView.as_view(), name='info_users'),
    path('users/add-user', UserCreateView.as_view(), name='add_user'),
    path('user-detail/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('posts-by-user/<int:id>', PostsByUserListView.as_view(), name='posts_by_user'),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('edit-user/<int:pk>', UserUpdateView.as_view(), name='edit_user'),
    path('follow/<int:pk>', FollowingUserView.as_view(), name='follow_user'),
    path('<int:pk>/followers', WatchFollowersView.as_view(), name='user_followers'),
    path('<int:pk>/following', WatchFollowingView.as_view(), name='user_following')
]
