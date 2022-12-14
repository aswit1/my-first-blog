from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from user_manager.forms import CustomUserCreationForm

# Create your views here.
def all_users(request):
    users = User.objects.all()
    return render(request, 'user_manager/all_users.html', {'users': users})

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
