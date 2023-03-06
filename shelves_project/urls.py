from django.urls import path
from shelves_project import views

app_name = 'shelves'

urlpatterns = [
    path('', views.index, name='index'),
]