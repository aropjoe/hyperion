from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import (
    UserRegistrationForm,
    UserUpdateForm,
    BusinessRegistrationForm,
    BusinessUpdateForm,
)
from .models import User, Business


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("home")
    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register_user.html", {"form": form})


def register_business(request):
    if request.method == "POST":
        form = BusinessRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
            business = authenticate(email=email, password=raw_password)
            login(request, business)
            return redirect("home")
    else:
        form = BusinessRegistrationForm()
    return render(request, "accounts/register_business.html", {"form": form})


@login_required
def update_user(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, "accounts/update_user.html", {"form": form})


@login_required
def update_business(request):
    if request.method == "POST":
        form = BusinessUpdateForm(request.POST, instance=request.user.business)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = BusinessUpdateForm(instance=request.user.business)
    return render(request, "accounts/update_business.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
        return redirect("home")
    else:
        messages.error(request, "Invalid email or password.")
    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)


return redirect("home")
