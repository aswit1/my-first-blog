from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    new_post = models.BooleanField(default=True)
    blog_post = models.BooleanField(default=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def revise(self):
        self.edit_date = timezone.now()
        self.save()
    def __str__(self):
        return self.title


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    published_date = models.DateTimeField(blank=True, null=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def revise(self):
        self.edit_date = timezone.now()
        self.save()
    def __str__(self):
        return self.text


class Conversations(models.Model):
    recipient = models.ManyToManyField(User, related_name='recipient')
    marked_as_new = models.ManyToManyField(User, related_name='marked_as_new')

    def __str__(self):
        return 'conversation'


class Direct_Message(models.Model):
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversations, on_delete=models.CASCADE, blank=True, null=True)
    send_date = models.DateTimeField(blank=True, null=True)

    def send(self):
        self.send_date = timezone.now()
        self.save()

    def __str__(self):
        return self.text