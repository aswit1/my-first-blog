from django import forms
from .models import Poll, Pollv2, PollQ


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        exclude = ('published_date', 'created_date', 'author', 'vote1', 'vote2', 'vote3', 'vote4',)


class Pollv2Form(forms.ModelForm):
    class Meta:
        model = Pollv2
        fields = ('title', 'description',)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = PollQ
        fields = ('description',)