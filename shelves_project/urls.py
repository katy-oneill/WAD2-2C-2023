from django.contrib import admin
from django.urls import path, include
from shelves_project import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.launch, name='launch'),
    path('admin/', admin.site.urls),
    path('friends/', views.friends, name='friends'),
    path('personal/', views.personal, name='personal'),
    path('social/', views.social, name='social'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
