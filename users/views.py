from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, update_session_auth_hash
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View

from users.models import CustomUser
from posts.models import Post
from users.forms import RegistrationUserForm, LoginForm, UserChangeForm
from posts.forms import CommentForm


class UserListView(ListView):
    model = CustomUser
    context_object_name = 'users'
    template_name = 'users/users_list.html'


class UserCreateView(CreateView):
    form_class = RegistrationUserForm
    success_url = reverse_lazy('login')
    template_name = 'users/create_user.html'
    extra_context = {'title': 'Registration'}


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('info_users')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', context={'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


class UserDetailView(DetailView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'users/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        return context


class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = UserChangeForm
    template_name = 'users/edit_user.html'
    success_url = reverse_lazy('info_users')
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        if form.has_changed():
            user = form.save(commit=False)
            old_password = form.cleaned_data.get('old_password')
            new_password1 = form.cleaned_data.get('new_password1')

            if old_password and new_password1:
                user.set_password(new_password1)
                update_session_auth_hash(self.request, user)

            user.save()
            return redirect(self.get_success_url())
        else:
            messages.info(self.request, "No changes detected.")
            return redirect(self.request.path_info)

    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'pk': self.request.user.pk})


class FollowingUserView(View):

    def post(self, request, pk):
        user_to_follow = get_object_or_404(CustomUser, pk=pk)
        if request.user.is_authenticated:
            if request.user in user_to_follow.followers.all():
                user_to_follow.followers.remove(request.user)
            else:
                user_to_follow.followers.add(request.user)
        return redirect('user_detail', pk=pk)


class WatchFollowingView(ListView):
    model = CustomUser
    context_object_name = 'following'
    template_name = 'users/my_following.html'

    def get_queryset(self):
        user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        return user.following.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        return context


class WatchFollowersView(ListView):
    model = CustomUser
    context_object_name = 'followers'
    template_name = 'users/my_followers.html'

    def get_queryset(self):
        user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        return user.followers.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        return context


class FollowingPostListView(ListView):
    model = Post
    template_name = 'posts/following_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = self.request.user
        following = user.following.all()
        return Post.objects.filter(user_post__in=following).select_related('user_post').\
            prefetch_related('likes', 'comments', 'comments__user_comment').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm
        return context
