from django import forms
from django.forms import TextInput, CharField
from django.shortcuts import get_object_or_404

from .models import Post, PostComment, Direct_Message, Conversations


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
        fields = ['text']


class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversations
        fields = ['recipient']

    # def check_existing(self):
    #     this_recipient = self.cleaned_data['recipient']
    #     meep = Conversations.objects.filter(recipient__exact=this_recipient.all)
    #     # meep = get_object_or_404(Conversations, recipient_c=this_recipient.all)
    #     print(this_recipient, "%%%%%%%%%%%%%%%%%%%%")
    #
    #     # if len(Conversations.objects.filter(recipient=this_recipient)) > 0:
    #     #     return True
    #     # else:
    #     #     return False


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

