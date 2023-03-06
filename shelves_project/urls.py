from django.contrib import admin
from django.urls import path
from django.urls import include
from shelves_project import views

urlpatterns = [
    path('', views.launch, name='launch'),
    path('admin/', admin.site.urls),
]
