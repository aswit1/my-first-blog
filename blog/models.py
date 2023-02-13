from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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