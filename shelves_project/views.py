from django.shortcuts import render
from django.http import HttpResponse

def launch(request):
    return render(request, shelves_project/launch.html)

# Create your views here.
