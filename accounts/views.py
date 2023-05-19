from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import (
    UserRegistrationForm,
    UserUpdateForm,
    BusinessRegistrationForm,
    BusinessUpdateForm,
)
from .models import Business
from django.contrib.auth.models import User
from django.contrib import messages


def register_business(request):
    if request.method == "POST":
        form = BusinessRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
            business = authenticate(email=email, password=raw_password)
            login(request, business)
            return redirect("core:home")
    else:
        form = BusinessRegistrationForm()
    return render(request, "accounts/register_business.html", {"form": form})


@login_required
def update_business(request):
    if request.method == "POST":
        form = BusinessUpdateForm(request.POST, instance=request.user.business)
        if form.is_valid():
            form.save()
            return redirect("core:dashboard")
    else:
        form = BusinessUpdateForm(instance=request.user.business)
    return render(request, "accounts/update_business.html", {"form": form})


def register_user(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.create_user(
            first_name=first_name, last_name=last_name, email=email, username=username
        )
        user.set_password(password)
        user.save()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("core:dashboard")
        else:
            messages.error(request, "An error occured")

    return render(request, "accounts/register.html")


@login_required
def update_user(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")

        user = request.user

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        user.save()

        return redirect("core:dashboard")

    else:
        return render(request, "accounts/update_user.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("core:dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("accounts:login")


@login_required
def user_profile(request):
    return render(request, "accounts/user_profile.html")
