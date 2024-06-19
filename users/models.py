from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    description = models.TextField(null=True, blank=True)
    user_avatar = models.ImageField(upload_to='users/avatar', null=True, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"User: {self.username}"

    def followers_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()
