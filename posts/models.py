from django.db import models
from django.urls import reverse

from users.models import CustomUser


class Post(models.Model):
    user_post = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    content = models.TextField(null=True, blank=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"Post: {self.user_post}, {self.title}"

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()


class Comment(models.Model):
    user_comment = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    content = models.CharField(max_length=256)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"Comment: {self.user_comment}, {self.post}"
