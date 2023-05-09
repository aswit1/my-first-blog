from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import TextInput, CharField
from django.shortcuts import get_object_or_404

from .models import Post, PostComment, Direct_Message, Conversations


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))


class AlexPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'blog_post',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))


class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))


class Direct_MessageForm(forms.ModelForm):
    class Meta:
        model = Direct_Message
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))


class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversations
        fields = ['recipient']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))


class Reply_MessageForm(forms.ModelForm):
    class Meta:
        model = Direct_Message
        fields = ['text']
        widgets = {'text': TextInput(attrs={'type': 'text','style':'vertical-align:middle;'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = ''
        self.fields['text'].widget.attrs['rows'] = 1
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))

