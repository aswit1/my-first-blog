from django import forms
from django.forms import TextInput, CharField

from .models import Post, PostComment, Direct_Message, Reply_Message


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

class Direct_MessageForm(forms.ModelForm):
    class Meta:
        model = Direct_Message
        fields = ['text', 'recipient']

class Reply_MessageForm(forms.ModelForm):
    class Meta:
        model = Direct_Message
        fields = ['text']
        # widgets = {'text': TextInput(attrs={'type': 'text'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = ''
        self.fields['text'].widget.attrs['rows'] = 1
        # self.helper.add_input(Submit('submit', 'Save'))

