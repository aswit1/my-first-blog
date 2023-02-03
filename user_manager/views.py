from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse

from mysite import settings
from user_manager.forms import CustomUserCreationForm, UserProfileEditForm, UserEditForm
from user_manager.models import UserProfile, Weather
import requests

from user_manager.tasks import get_weather


# Create your views here.
def all_users(request):
    all_existing_users = User.objects.all()
    for each_user in all_existing_users:
        user_profile, created = UserProfile.objects.get_or_create(user=each_user)
    user_profiles = UserProfile.objects.all()
    return render(request, 'user_manager/all_users.html', {'user_profiles': user_profiles})

def this_user(request):
    this_current_user, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'user_manager/this_user.html', {'this_current_user': this_current_user})

def user_profile_edit(request):
    this_user = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        this_form = UserProfileEditForm(request.POST, instance=this_user)
        this_user_form = UserEditForm(request.POST, instance=this_user.user)
        if this_form.is_valid():
            form = this_form.save(commit=False)
            form.save()
        if this_user_form.is_valid():
            user_form = this_user_form.save(commit=False)
            user_form.save()
        return redirect('this_user')
    # user_profile = UserProfile.objects.get_or_create(user=request.user)
    this_form = UserProfileEditForm(instance=this_user)
    this_user_form = UserEditForm(instance=this_user.user)
    return render(request, 'user_manager/user_edit.html', {'this_form': this_form, 'this_user_form': this_user_form})


def edit_user_profile(request, pk):
    this_user_profile = UserProfile.objects.get(pk=pk)
    if request.method == "POST":
        this_form = UserProfileEditForm(request.POST, instance=this_user_profile)
        this_user_form = UserEditForm(request.POST, instance=this_user_profile.user)
        if this_form.is_valid():
            form = this_form.save(commit=False)
            form.save()
        if this_user_form.is_valid():
            user_form = this_user_form.save(commit=False)
            user_form.save()
        return redirect('all_users')

    this_form = UserProfileEditForm(instance=this_user_profile)
    this_user_form = UserEditForm(instance=this_user_profile.user)
    return render(request, 'user_manager/user_edit.html', {'this_form': this_form, 'this_user_form': this_user_form})

def delete_user(request, pk):
    this_user = User.objects.get(pk=pk)
    if request.method == "POST":
        messages.add_message(request, messages.INFO, f" {this_user} has successfully been deleted.")
        this_user.delete()
        return redirect('all_users')
    return render(request, 'user_manager/user_delete.html', {'this_user': this_user})

def register(request):
    if request.method == "GET":
        return render(
            request, "user_manager/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.add_message(request, messages.INFO, "You have been successfully registered!")
            return redirect(reverse("post_list"))
        else:
            print("My form was not valid", form.errors)
            return render(
                request, "user_manager/register.html",
                {"form": CustomUserCreationForm}
            )

def update_weather_view(request):
    get_weather.delay()
    return redirect(request.META.get('HTTP_REFERER'))
