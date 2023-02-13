from django import forms
from .models import Post, PostComment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)


class AlexPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'blog_post',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['text']

