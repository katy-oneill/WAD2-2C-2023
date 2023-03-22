from django.shortcuts import render
from django.http import HttpResponse

def launch(request):
    return render(request, 'shelves/launch.html')

def index(request):
    return HttpResponse("Hey!")

def friends(request):
    return render(request, 'shelves/friends.html')

def personal(request):
    return render(request, 'shelves/personal.html')

def social(request):
    return render(request, 'shelves/social.html')
