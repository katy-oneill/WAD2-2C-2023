from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from shelves import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'shelves'

urlpatterns = [
    path('', views.launch, name='launch'),
    path('admin/', admin.site.urls),
    path('accounts', include('django.contrib.auth.urls')),
    path('friends/', views.friends, name='friends'),
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
    path('profile/<username>/edit/', views.edit_profile, name='edit_profile'),

#--------------------------------------------------------------------------------------------------------
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('media_collection/', views.list_media, name='list_media'),
    path('<str:media_type>/<slug:media_title_slug>/show_media', views.show_media, name='show_media'),
    path('add_media/', views.add_media, name='add_media'),
    path('<str:media_type>/<slug:media_title_slug>/add_details/', views.add_details, name='add_details'),
    path('<str:media_type>/<slug:media_title_slug>/add_post/', views.add_post, name='add_post'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('profiles/', views.ListProfilesView.as_view(), name='list_profiles'),
    path('delete/<username>', views.delete_account, name='delete_account'),
    path('<username>/send_friend_request/', views.send_friend_request, name='send_friend_request'),
    path('<username>/accept_friend_request/', views.accept_friend_request, name='accept_friend_request'),
#--------------------------------------------------------------------------------------------------------

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)