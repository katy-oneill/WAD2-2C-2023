"""shelves URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from shelves_project import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "shelves"
urlpatterns = [
    path('', views.launch, name='launch'),
    path('admin/', admin.site.urls),
    path('friends/', views.friends, name='friends'),
    path('personal/', views.personal, name='personal'),
    path('social/', views.social, name='social'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]