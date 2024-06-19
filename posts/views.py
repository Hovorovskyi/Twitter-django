from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from .models import Post, Comment
from .forms import CreatePostForm, CommentForm
from users.models import CustomUser


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/all_posts.html'

    def get_queryset(self):
        query = super().get_queryset()
        return query.select_related('user_post').prefetch_related('likes', 'comments', 'comments__user_comment').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class PostCreateView(CreateView):
    form_class = CreatePostForm
    template_name = 'posts/create_post.html'
    extra_context = {'title': 'Create new post'}

    def form_valid(self, form):
        form.instance.user_post = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('posts_by_user', kwargs={'id': self.request.user.id})


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        query = super().get_queryset()
        return query.select_related('user_post').prefetch_related('likes', 'comments', 'comments__user_comment').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['current_user'] = self.request.user
        return context


class CommentCreateView(CreateView):
    form_class = CommentForm
    template_name = 'posts/post_detail.html'

    def form_valid(self, form):
        post_id = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_id)
        comment = form.save(commit=False)
        comment.post = post
        comment.user_comment = self.request.user
        comment.save()
        return redirect('post_detail', pk=post_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs['pk']
        context['post'] = get_object_or_404(Post, pk=post_id)
        context['form'] = self.get_form()
        return context


class PostsByUserListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'users/posts_by_user.html'

    def get_queryset(self):
        posts = Post.objects.filter(user_post__id=self.kwargs['id']).select_related('user_post').\
            prefetch_related('likes', 'comments', 'comments__user_comment').order_by('-created_at')
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(CustomUser, pk=self.kwargs['id'])
        context['current_user'] = self.request.user
        context['form'] = CommentForm()
        return context


def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


class PostUpdateView(UpdateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'posts/edit_post.html'
    extra_context = {'title': 'Update post'}

    def get_queryset(self):
        return super().get_queryset().filter(user_post=self.request.user)


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    template_name = 'posts/delete_post.html'

    def get_queryset(self):
        return super().get_queryset().filter(user_post=self.request.user)
