from django.shortcuts import render
from django.http import HttpResponse

def launch(request):
    return render(request, 'shelves/launch.html')

def index(request):
    return HttpResponse("Hey!")
