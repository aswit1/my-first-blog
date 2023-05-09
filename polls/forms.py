from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import ModelChoiceField

from .models import Poll, Pollv2, PollQ


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        exclude = ('published_date', 'created_date', 'author', 'vote1', 'vote2', 'vote3', 'vote4',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))


class Pollv2Form(forms.ModelForm):
    class Meta:
        model = Pollv2
        fields = ('title', 'description',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))

class QuestionForm(forms.ModelForm):
    class Meta:
        model = PollQ
        fields = ('description',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))


class Pollv3Form(forms.Form):

    def __init__(self, *args, **kwargs):
        poll = kwargs.pop('poll')
        super().__init__(*args, **kwargs)
        poll_options = PollQ.objects.filter(poll=poll)
        self.fields['my_vote'] = ModelChoiceField(queryset=poll_options,widget=forms.RadioSelect)

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
