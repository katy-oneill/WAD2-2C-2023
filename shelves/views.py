from django.shortcuts import render, redirect
from django.http import HttpResponse
from shelves.form import RegistrationForm
from django.contrib.auth import login, logout
from shelves.models import UserProfile

def launch(request):
    return render(request, 'shelves/launch.html')

def friends(request):
    return render(request, 'shelves/friends.html')

def personal(request):
    return render(request, 'shelves/personal.html')

def social(request):
    return render(request, 'shelves/social.html')

def login_view(request):
    return render(request, 'shelves/login.html')

def logout_view(request):
    logout(request)
    return redirect('launch')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            picture = form.cleaned_data.get('picture')
            age = form.cleaned_data.get('age')
            UserProfile.objects.create(user=user, picture=picture, age=age)
            login(request, user)
            return redirect('registration_success')
    else:
        form = RegistrationForm()
    return render(request, 'shelves/register.html', {'form': form})

def registration_success(request):
    return HttpResponse("Registration successful! You are now logged in.")

def dashboard(request):
    try:
        user_profile = request.user.UserProfile()
    except UserProfile.DoesNotExist:
        user_profile = None
    return render(request, 'shelves/dashboard.html', {'user_profile': user_profile})