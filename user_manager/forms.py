from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import DateInput, DateField, SelectDateWidget

from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gender', 'birthday', 'phone_number', 'text_updates', 'email_updates']
        widgets = {'birthday': DateInput(attrs={'type': 'date'})}



class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']