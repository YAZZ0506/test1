from django.conf import settings
from django.contrib.auth.models import User, UserManager
from django.db import models

# Create your models here.


class WeChatUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE)
    email = models.TextField(max_length=50, null=True, blank=True)
    motto = models.CharField(max_length=50, null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    pic = models.CharField(max_length=50, null=True, blank=True)
    user_pic = models.CharField(max_length=50, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.user.username


class Status(models.Model):
    user = models.ForeignKey(WeChatUser, models.CASCADE)
    text = models.CharField(max_length=280, null=True, blank=True)
    pics = models.CharField(max_length=100, null=True, blank=True)
    pub_time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(WeChatUser, through='Like', related_name='liked_statuses', blank=True)
    comments = models.ManyToManyField(WeChatUser, through='Comment', related_name='commented_statuses')

    objects = models.Manager()

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['id']


class Comment(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    user = models.ForeignKey(WeChatUser, on_delete=models.CASCADE)
    text = models.CharField(max_length=280)
    pub_time = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return self.text


class Like(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    user = models.ForeignKey(WeChatUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

