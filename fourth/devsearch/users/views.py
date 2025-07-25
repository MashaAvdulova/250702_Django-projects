from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.exceptions import  ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def profiles(request):
    prof = Profile.objects.all()
    context = {
        'profiles' : prof
    }
    return render(request,'users/index.html', context)


def user_profile(request, pk):
    prof = Profile.objects.get(id=pk)
    top_skills = prof.skill_set.exclude(description__exact="")
    other_skills = prof.skill_set.filter(description__exact="")

    context = {
        'profile': prof,
        'top_skills': top_skills,
        'other_skill': other_skills,

    }

    return render(request, 'users/profile.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request, 'Username not found')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'users/login_register.html')


def logout_user(request):
    logout(request)
    messages.error(request, 'User was logout')
    return redirect('login')

def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created')
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Error registration')

    context = {
        'page': page,
        'form': form,
    }

    return render(request, 'users/login_register.html', context)

@login_required(login_url='login')
def user_account(request):
    prof = request.user.profile
    skills = prof.skill_set.all()
    projects = prof.projects_set.all()

    context = {
        'profile': prof,
        'skills': skills,
        'projects': projects
    }
    return render(request, 'users/account.html', context)