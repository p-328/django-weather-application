from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import AuthForm, CreateForm
from django.urls import reverse


# Create your views here.
def index(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect(reverse('cities-page'))
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request=request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect(reverse('cities-page'))
            else:
                messages.error(
                    request, 'Invalid Credentials!')
                return redirect(reverse('login-screen'))
    else:
        form = AuthForm()
    return render(request, 'login.html', {'form': form})


def create_user(request: HttpRequest):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            existing_users_under_input = User.objects.filter(
                username=form.cleaned_data['new_username'])
            if len(existing_users_under_input) > 0:
                messages.error(request=request, message='Username is taken!')
                return redirect(reverse('creation'))
            else:
                new_user = User(
                    username=form.cleaned_data['new_username'],
                    password=form.cleaned_data['new_password'],
                    email=form.cleaned_data['email'])
                new_user.set_password(form.cleaned_data['new_password'])
                new_user.save()
                return redirect(reverse('login-screen'))
    else:
        form = CreateForm()
    return render(request, 'create.html', {'form': form})


def logout_controller(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('login-screen'))
