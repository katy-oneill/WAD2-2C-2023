from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from shelves import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.launch, name='launch'),
    path('admin/', admin.site.urls),
    path('accounts', include('django.contrib.auth.urls')),
    path('friends/', views.friends, name='friends'),
    path('personal/', views.personal, name='personal'),
    path('social/', views.social, name='social'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='shelves/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('accounts/dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/dashboard/books/', views.books, name="books"),
    path('accounts/dashboard/albums/', views.albums, name="albums"),
    path('accounts/dashboard/shows/', views.shows, name="shows"),
    path('accounts/dashboard/movies/', views.movies, name="movies"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)